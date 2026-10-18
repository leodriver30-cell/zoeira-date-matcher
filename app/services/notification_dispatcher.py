import json
import urllib.parse
import httpx
from typing import Set
from fastapi import WebSocket
from app.config import (
    CALLMEBOT_API_KEY, 
    DEFAULT_CREATOR_PHONE, 
    FACEBOOK_PAGE_TOKEN, 
    FACEBOOK_WEBHOOK_URL, 
    DEFAULT_WEBHOOK_URL
)

# Gerenciador de conexões WebSocket para o painel em tempo real
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, Set[WebSocket]] = {}

    async def connect(self, slug: str, websocket: WebSocket):
        await websocket.accept()
        if slug not in self.active_connections:
            self.active_connections[slug] = set()
        self.active_connections[slug].add(websocket)

    def disconnect(self, slug: str, websocket: WebSocket):
        if slug in self.active_connections:
            self.active_connections[slug].discard(websocket)

    async def broadcast_to_slug(self, slug: str, message: dict):
        if slug in self.active_connections:
            for connection in list(self.active_connections[slug]):
                try:
                    await connection.send_text(json.dumps(message))
                except Exception:
                    self.disconnect(slug, connection)

manager = ConnectionManager()

def normalize_phone(phone: str | None) -> str:
    """Normaliza o número de telefone removendo pontuação e corrigindo códigos internacionais."""
    if not phone:
        return ""
    digits = "".join(c for c in phone if c.isdigit())
    
    # Caso Japão (+81): se digitarem 81070... ou 81080..., remove o zero pós-código
    if digits.startswith("810") and len(digits) >= 12:
        digits = "81" + digits[3:]
    # Se digitarem número japonês local iniciando com 070, 080 ou 090 (11 dígitos)
    elif digits.startswith("0") and len(digits) == 11 and digits[1] in ("7", "8", "9"):
        digits = "81" + digits[1:]
    # Caso Brasil (+55): remove zero após o 55 se digitado 55011...
    elif digits.startswith("550") and len(digits) >= 13:
        digits = "55" + digits[3:]
        
    return digits

async def dispatch_date_confirmation(
    slug: str,
    target_name: str,
    selected_date: str,
    selected_time: str,
    creator_whatsapp: str | None = None,
    creator_callmebot_key: str | None = None,
    creator_facebook: str | None = None,
    creator_webhook: str | None = None
):
    """
    Dispara notificação automática em segundo plano para o dono do convite:
    1. Painel em Tempo Real (WebSocket com som/alerta)
    2. WhatsApp Automático via Robô CallMeBot
    3. Facebook Messenger Bot (Meta Graph API / Webhook)
    4. Push Instantâneo gratuito (ntfy.sh)
    5. Webhook externo personalizado
    """
    message_text = (
        f"NOVO DATE CONFIRMADO! {target_name} acabou de aceitar seu convite para o date! "
        f"Data escolhida: {selected_date} ({selected_time}). O evento ja foi agendado!"
    )

    # 1. Notifica o painel em tempo real via WebSocket
    await manager.broadcast_to_slug(slug, {
        "type": "date_accepted",
        "target_name": target_name,
        "selected_date": selected_date,
        "selected_time": selected_time,
        "message": message_text
    })

    # 2. Disparo Automático via Robô no WhatsApp (CallMeBot)
    whatsapp_bot_sent = False
    raw_phone = creator_whatsapp or DEFAULT_CREATOR_PHONE
    clean_phone = normalize_phone(raw_phone)
    bot_key = (creator_callmebot_key or "").strip() or CALLMEBOT_API_KEY.strip()

    if clean_phone and bot_key:
        try:
            encoded_msg = urllib.parse.quote(message_text)
            callmebot_url = f"https://api.callmebot.com/whatsapp.php?phone={clean_phone}&text={encoded_msg}&apikey={bot_key}"
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(callmebot_url)
                if resp.status_code == 200:
                    whatsapp_bot_sent = True
                    print(f"[OK] Notificacao WhatsApp enviada com sucesso para +{clean_phone} via CallMeBot!")
                else:
                    safe_resp = resp.text[:120].encode('ascii', 'ignore').decode('ascii')
                    print(f"[WARN] CallMeBot resposta ({resp.status_code}): {safe_resp}")
        except Exception as e:
            print(f"[WARN] Erro ao enviar WhatsApp automatico via CallMeBot: {e}")
    elif clean_phone and not bot_key:
        print(f"[INFO] WhatsApp +{clean_phone} informado, mas chave do robo (CallMeBot) nao esta configurada ainda.")

    # 3. Disparo Automático via Robô no Facebook Messenger
    facebook_bot_sent = False
    if creator_facebook:
        clean_fb = creator_facebook.replace("https://", "").replace("http://", "").replace("m.me/", "").replace("facebook.com/", "").strip()
        # Se houver token de página do Facebook configurado, usa a Meta Graph API
        if FACEBOOK_PAGE_TOKEN:
            try:
                graph_url = "https://graph.facebook.com/v19.0/me/messages"
                headers = {
                    "Authorization": f"Bearer {FACEBOOK_PAGE_TOKEN}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "recipient": {"id": clean_fb},
                    "message": {"text": message_text}
                }
                async with httpx.AsyncClient(timeout=8.0) as client:
                    resp = await client.post(graph_url, headers=headers, json=payload)
                    if resp.status_code == 200:
                        facebook_bot_sent = True
                        print(f"[OK] Notificacao Facebook Messenger enviada para {clean_fb}!")
                    else:
                        print(f"[WARN] Facebook Graph API status: {resp.status_code}")
            except Exception as e:
                print(f"[WARN] Erro ao enviar Facebook Messenger via API: {e}")

    # 4. Disparo Push Instantâneo gratuito via ntfy.sh (Aparece no celular sem precisar de cadastro)
    try:
        topic_name = f"zoeira-date-{slug}"
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(
                f"https://ntfy.sh/{topic_name}",
                data=message_text.encode("utf-8"),
                headers={
                    "Title": f"Date Aceito por {target_name}!",
                    "Priority": "high",
                    "Tags": "heart,champagne"
                }
            )
            print(f"[OK] Notificacao Push enviada para ntfy.sh/{topic_name}")
    except Exception as e:
        print(f"[INFO] ntfy push: {e}")

    # 5. Disparo via Webhooks Externos (se configurado no link ou no servidor)
    target_webhook = creator_webhook or FACEBOOK_WEBHOOK_URL or DEFAULT_WEBHOOK_URL
    if target_webhook:
        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                await client.post(target_webhook, json={
                    "event": "date_accepted",
                    "slug": slug,
                    "target_name": target_name,
                    "date": selected_date,
                    "time": selected_time,
                    "whatsapp": clean_phone,
                    "facebook": creator_facebook,
                    "message": message_text
                })
                print(f"[OK] Webhook disparado com sucesso para {target_webhook}")
        except Exception as e:
            print(f"[WARN] Erro ao disparar webhook: {e}")

    return {
        "status": "dispatched",
        "whatsapp_bot_sent": whatsapp_bot_sent,
        "facebook_bot_sent": facebook_bot_sent,
        "message": message_text
    }

async def dispatch_dodge_event(slug: str, current_count: int):
    """Notifica o painel quando o amigo ou pretendente tenta clicar no 'Não'."""
    await manager.broadcast_to_slug(slug, {
        "type": "dodge_attempt",
        "count": current_count
    })
