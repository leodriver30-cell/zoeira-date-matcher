import json
import re
import uuid
import datetime
from zoneinfo import ZoneInfo
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Link, DateResponse
from app.services.i18n_service import (
    DATE_DURATION_MIN,
    resolve_timezone,
    format_tz_label,
    format_time_range,
    t,
)
from app.services.notification_dispatcher import manager, dispatch_date_confirmation, dispatch_dodge_event
from app.config import CALLMEBOT_API_KEY, DEFAULT_CREATOR_PHONE

router = APIRouter(prefix="/api")

TIME_RE = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")


class DaySlotInput(BaseModel):
    date: str
    times: list[str]


class CreateLinkRequest(BaseModel):
    link_type: str = "prank"  # "prank" ou "date"
    question: str | None = None
    target_name: str | None = None
    creator_name: str | None = None
    creator_whatsapp: str | None = None
    creator_callmebot_key: str | None = None
    creator_facebook: str | None = None
    creator_line: str | None = None
    creator_webhook: str | None = None
    available_slots: list[DaySlotInput] | None = None
    timezone: str | None = None
    lang: str | None = "pt"


class ConfirmDateRequest(BaseModel):
    selected_date: str
    selected_time: str
    dodge_count: int = 0
    notes: str | None = None
    lang: str | None = "pt"


def get_legacy_fallback_schedule(days_ahead: int = 90) -> list[dict]:
    """Mantém compatibilidade com links antigos criados antes do seletor de dias/horários."""
    now = datetime.datetime.now(datetime.timezone.utc)
    schedule = []
    for d in range(1, days_ahead + 1):
        day_dt = now + datetime.timedelta(days=d)
        date_str = day_dt.strftime("%Y-%m-%d")
        weekday = day_dt.weekday()
        is_free = weekday in [1, 2, 3, 4, 5, 6]
        schedule.append({
            "date": date_str,
            "day_of_week": weekday,
            "available": is_free,
            "status": "available" if is_free else "busy"
        })
    return schedule


def build_availability_ViewModel(link: Link, display_lang: str = "pt") -> dict:
    """Extrai e formata os dias, horários exatos (3h) e fuso horário congelado no link."""
    if not link.available_days:
        return {
            "is_legacy": True,
            "timezone": resolve_timezone(None, display_lang),
            "tz_label": format_tz_label(None, display_lang),
            "duration_min": DATE_DURATION_MIN,
            "days": [],
            "schedule": get_legacy_fallback_schedule(30),
        }

    try:
        raw = json.loads(link.available_days)
    except Exception:
        raw = {}

    tz_name = raw.get("timezone") or resolve_timezone(None, display_lang)
    duration_min = int(raw.get("duration_min") or DATE_DURATION_MIN)
    taken_set = set(raw.get("taken") or [])
    weekdays = t("weekdays_short", lang=display_lang)
    if not isinstance(weekdays, list) or len(weekdays) < 7:
        weekdays = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    enriched_days = []
    for item in raw.get("days", []):
        d_str = item.get("date", "")
        try:
            d_obj = datetime.date.fromisoformat(d_str)
            wd_label = weekdays[d_obj.weekday()]
            short_date = f"{d_obj.day:02d}/{d_obj.month:02d}"
        except Exception:
            wd_label = ""
            short_date = d_str[-5:]

        slot_items = []
        free_count = 0
        for tm in item.get("times", []):
            key = f"{d_str}|{tm}"
            is_free = key not in taken_set
            if is_free:
                free_count += 1
            slot_items.append({
                "time": tm,
                "range": format_time_range(tm, duration_min),
                "available": is_free,
            })

        if slot_items:
            enriched_days.append({
                "date": d_str,
                "short_date": short_date,
                "weekday": wd_label,
                "available": free_count > 0,
                "times": slot_items,
            })

    return {
        "is_legacy": False,
        "timezone": tz_name,
        "tz_label": format_tz_label(tz_name, display_lang),
        "duration_min": duration_min,
        "days": enriched_days,
        "schedule": [],
    }


def validate_and_serialize_slots(slots: list[DaySlotInput] | None, tz_name: str, lang: str = "pt") -> str:
    if not slots or len(slots) == 0:
        raise HTTPException(status_code=422, detail=t("error_select_at_least_one_day", lang=lang))
    if len(slots) > 10:
        raise HTTPException(status_code=422, detail=t("max_days_reached", lang=lang))

    try:
        today_tz = datetime.datetime.now(ZoneInfo(tz_name)).date()
    except Exception:
        today_tz = datetime.date.today()

    max_date = today_tz + datetime.timedelta(days=95)
    seen_dates = set()
    cleaned_days = []

    for item in slots:
        d_str = (item.date or "").strip()
        try:
            d_obj = datetime.date.fromisoformat(d_str)
        except Exception:
            raise HTTPException(status_code=422, detail=f"Data inválida: {d_str}")

        if d_obj < today_tz or d_obj > max_date:
            raise HTTPException(status_code=422, detail=f"Data fora do período permitido: {d_str}")

        if d_str in seen_dates:
            raise HTTPException(status_code=422, detail=f"Data duplicada: {d_str}")
        seen_dates.add(d_str)

        if not item.times or len(item.times) == 0:
            raise HTTPException(status_code=422, detail=t("error_day_without_time", lang=lang, date=d_str))
        if len(item.times) > 8:
            raise HTTPException(status_code=422, detail=f"Máximo de 8 horários por dia ({d_str}).")

        clean_times = []
        seen_times = set()
        for raw_t in item.times:
            t_str = (raw_t or "").strip()
            if not TIME_RE.match(t_str):
                raise HTTPException(status_code=422, detail=f"Horário inválido: {t_str}")
            if t_str not in seen_times:
                seen_times.add(t_str)
                clean_times.append(t_str)

        clean_times.sort()
        cleaned_days.append({"date": d_str, "times": clean_times})

    cleaned_days.sort(key=lambda x: x["date"])
    return json.dumps({
        "timezone": tz_name,
        "duration_min": DATE_DURATION_MIN,
        "days": cleaned_days,
        "taken": []
    })


@router.post("/links")
def create_link(data: CreateLinkRequest, db: Session = Depends(get_db)):
    lang = (data.lang or "pt").lower()
    tz_name = resolve_timezone(data.timezone, lang)

    available_days_json = None
    if data.link_type == "date":
        available_days_json = validate_and_serialize_slots(data.available_slots, tz_name, lang)

    short_uuid = str(uuid.uuid4())[:8]
    slug = f"{data.link_type}-{short_uuid}"
    if data.target_name:
        clean_name = "".join(c for c in data.target_name if c.isalnum()).lower()
        if clean_name:
            slug = f"{clean_name}-{short_uuid[:5]}"

    whatsapp_num = (data.creator_whatsapp or "").strip() or None
    bot_key = (data.creator_callmebot_key or "").strip() or None
    fb_val = (data.creator_facebook or "").strip() or None
    line_val = (data.creator_line or "").strip() or None

    link = Link(
        slug=slug,
        link_type=data.link_type,
        question=data.question,
        target_name=data.target_name,
        creator_name=data.creator_name,
        creator_whatsapp=whatsapp_num,
        creator_callmebot_key=bot_key,
        creator_facebook=fb_val,
        creator_line=line_val,
        creator_webhook=data.creator_webhook,
        available_days=available_days_json,
    )
    db.add(link)
    db.commit()
    db.refresh(link)

    path_prefix = "d" if data.link_type == "date" else "z"
    return {
        "status": "success",
        "slug": link.slug,
        "timezone": tz_name,
        "url": f"/{path_prefix}/{link.slug}",
        "dashboard_url": f"/dash/{link.slug}"
    }


@router.post("/links/{slug}/dodge")
async def record_dodge(slug: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.slug == slug).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link não encontrado")

    link.total_dodges += 1
    db.commit()

    await dispatch_dodge_event(slug, link.total_dodges)
    return {"status": "ok", "total_dodges": link.total_dodges}


@router.get("/links/{slug}/schedule")
def get_schedule(slug: str, lang: str = "pt", db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.slug == slug).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link não encontrado")

    vm = build_availability_ViewModel(link, display_lang=lang)
    return vm


@router.post("/links/{slug}/confirm_date")
async def confirm_date(slug: str, data: ConfirmDateRequest, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.slug == slug).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link não encontrado")

    lang = (data.lang or "pt").lower()
    display_time_str = data.selected_time

    if link.available_days:
        try:
            avail = json.loads(link.available_days)
        except Exception:
            avail = {}

        days_map = {d["date"]: d.get("times", []) for d in avail.get("days", [])}
        if data.selected_date not in days_map or data.selected_time not in days_map[data.selected_date]:
            raise HTTPException(status_code=400, detail="Data ou horário inválido para este convite.")

        slot_key = f"{data.selected_date}|{data.selected_time}"
        taken_list = avail.get("taken") or []
        if slot_key in taken_list:
            raise HTTPException(status_code=409, detail=t("slot_already_taken", lang=lang))

        taken_list.append(slot_key)
        avail["taken"] = taken_list
        link.available_days = json.dumps(avail)

        tz_name = avail.get("timezone") or "Asia/Tokyo"
        duration_min = int(avail.get("duration_min") or DATE_DURATION_MIN)
        time_range = format_time_range(data.selected_time, duration_min)
        tz_label = format_tz_label(tz_name, lang)
        display_time_str = f"{time_range} ({tz_label})"

    link.accepted = True
    response = DateResponse(
        link_id=link.id,
        selected_date=data.selected_date,
        selected_time=display_time_str,
        dodge_count=data.dodge_count,
        notes=data.notes
    )
    db.add(response)
    db.commit()

    await dispatch_date_confirmation(
        slug=link.slug,
        target_name=link.target_name or "Sua pretendente",
        selected_date=data.selected_date,
        selected_time=display_time_str,
        creator_whatsapp=link.creator_whatsapp,
        creator_callmebot_key=link.creator_callmebot_key,
        creator_facebook=link.creator_facebook,
        creator_webhook=link.creator_webhook
    )

    return {
        "status": "success",
        "selected_date": data.selected_date,
        "selected_time_display": display_time_str,
        "message": "Date confirmado com sucesso!"
    }


@router.post("/links/{slug}/test_bot")
async def test_bot_notification(slug: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.slug == slug).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link não encontrado")

    result = await dispatch_date_confirmation(
        slug=link.slug,
        target_name=link.target_name or "Teste Crush",
        selected_date="2026-10-31",
        selected_time="19:00 – 22:00",
        creator_whatsapp=link.creator_whatsapp,
        creator_callmebot_key=link.creator_callmebot_key,
        creator_facebook=link.creator_facebook,
        creator_webhook=link.creator_webhook
    )
    return {"status": "ok", "result": result}


@router.websocket("/ws/{slug}")
async def websocket_dashboard(websocket: WebSocket, slug: str):
    await manager.connect(slug, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(slug, websocket)
