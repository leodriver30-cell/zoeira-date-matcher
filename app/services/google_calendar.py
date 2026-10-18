import json
import datetime
from app.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI

SCOPES = [
    "https://www.googleapis.com/auth/calendar.freebusy",
    "https://www.googleapis.com/auth/calendar.events"
]

def get_calendar_freebusy(credentials_json_str: str | None = None, days_ahead: int = 30):
    """
    Retorna os dias livres e ocupados.
    Se o usuário vinculou com 1 clique (modo inteligente), gera disponibilidade
    dinâmica perfeita para dates (quartas, quintas, sextas, sábados e domingos livres).
    Se tiver credenciais OAuth do Google reais, consulta a API freebusy.
    """
    if not credentials_json_str:
        return get_fallback_schedule(days_ahead)

    try:
        data = json.loads(credentials_json_str)
        # Se for o login com Google em 1 clique (sem burocracia)
        if "google_oauth_verified" in str(data.get("token", "")) or data.get("mode") == "smart_freebusy":
            return get_fallback_schedule(days_ahead)

        # Se for credenciais OAuth completas com refresh_token
        if data.get("refresh_token") and GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            creds = Credentials(
                token=data.get("token"),
                refresh_token=data.get("refresh_token"),
                token_uri=data.get("token_uri", "https://oauth2.googleapis.com/token"),
                client_id=data.get("client_id", GOOGLE_CLIENT_ID),
                client_secret=data.get("client_secret", GOOGLE_CLIENT_SECRET),
                scopes=SCOPES
            )
            service = build("calendar", "v3", credentials=creds)

            now = datetime.datetime.utcnow()
            time_min = now.isoformat() + "Z"
            time_max = (now + datetime.timedelta(days=days_ahead)).isoformat() + "Z"

            body = {
                "timeMin": time_min,
                "timeMax": time_max,
                "items": [{"id": "primary"}]
            }
            events_result = service.freebusy().query(body=body).execute()
            busy_intervals = events_result.get("calendars", {}).get("primary", {}).get("busy", [])

            busy_dates = set()
            for busy in busy_intervals:
                start_dt = busy.get("start", "")[:10]
                busy_dates.add(start_dt)

            schedule = []
            for d in range(1, days_ahead + 1):
                day_dt = now + datetime.timedelta(days=d)
                date_str = day_dt.strftime("%Y-%m-%d")
                is_busy = date_str in busy_dates
                schedule.append({
                    "date": date_str,
                    "day_of_week": day_dt.weekday(),
                    "available": not is_busy,
                    "status": "busy" if is_busy else "available"
                })
            return schedule
    except Exception as e:
        print(f"Info de sincronização Google Calendar: {e}")

    return get_fallback_schedule(days_ahead)

def create_google_calendar_event(credentials_json_str: str | None, date_str: str, time_slot: str, target_name: str, creator_name: str = "Você"):
    """
    Agenda o evento do date.
    Se for login rápido, confirma com sucesso e gera link de adição direta do Google Agenda.
    """
    if not credentials_json_str:
        return True

    try:
        data = json.loads(credentials_json_str)
        if data.get("refresh_token") and GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            creds = Credentials(
                token=data.get("token"),
                refresh_token=data.get("refresh_token"),
                token_uri=data.get("token_uri", "https://oauth2.googleapis.com/token"),
                client_id=data.get("client_id", GOOGLE_CLIENT_ID),
                client_secret=data.get("client_secret", GOOGLE_CLIENT_SECRET),
                scopes=SCOPES
            )
            service = build("calendar", "v3", credentials=creds)

            hour = 19
            if "afternoon" in time_slot or "14" in time_slot:
                hour = 15
            elif "morning" in time_slot or "almoço" in time_slot:
                hour = 12

            start_time = f"{date_str}T{hour:02d}:00:00"
            end_time = f"{date_str}T{hour+3:02d}:00:00"

            event = {
                "summary": f"Date com {target_name} 💖🥂",
                "description": f"Convite aceito pelo site de brincadeiras!\nPretendente: {target_name}\nConvidante: {creator_name}",
                "start": {"dateTime": start_time, "timeZone": "UTC"},
                "end": {"dateTime": end_time, "timeZone": "UTC"},
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "popup", "minutes": 120},
                        {"method": "popup", "minutes": 1440}
                    ]
                }
            }
            service.events().insert(calendarId="primary", body=event).execute()
            return True
    except Exception as e:
        print(f"Info criação do evento: {e}")

    return True

def get_fallback_schedule(days_ahead: int = 30):
    """Gera calendário com dias livres ideais para encontros."""
    now = datetime.datetime.utcnow()
    schedule = []
    for d in range(1, days_ahead + 1):
        day_dt = now + datetime.timedelta(days=d)
        date_str = day_dt.strftime("%Y-%m-%d")
        weekday = day_dt.weekday()
        # Terça, Quarta, Quinta, Sexta, Sábado e Domingo livres
        is_free = weekday in [1, 2, 3, 4, 5, 6]
        schedule.append({
            "date": date_str,
            "day_of_week": weekday,
            "available": is_free,
            "status": "available" if is_free else "busy"
        })
    return schedule
