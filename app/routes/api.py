import uuid
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Link, DateResponse
from app.services.google_calendar import get_calendar_freebusy, create_google_calendar_event
from app.services.notification_dispatcher import manager, dispatch_date_confirmation, dispatch_dodge_event
from app.config import CALLMEBOT_API_KEY, DEFAULT_CREATOR_PHONE

router = APIRouter(prefix="/api")

class CreateLinkRequest(BaseModel):
    link_type: str = "prank" # "prank" ou "date"
    question: str | None = None
    target_name: str | None = None
    creator_name: str | None = None
    creator_whatsapp: str | None = None
    creator_callmebot_key: str | None = None
    creator_facebook: str | None = None
    creator_line: str | None = None
    creator_webhook: str | None = None
    google_credentials: str | None = None

class ConfirmDateRequest(BaseModel):
    selected_date: str
    selected_time: str
    dodge_count: int = 0
    notes: str | None = None

@router.post("/links")
def create_link(data: CreateLinkRequest, db: Session = Depends(get_db)):
    # Gera um slug curto e amigável
    short_uuid = str(uuid.uuid4())[:8]
    slug = f"{data.link_type}-{short_uuid}"
    if data.target_name:
        clean_name = "".join(c for c in data.target_name if c.isalnum()).lower()
        slug = f"{clean_name}-{short_uuid[:5]}"

    whatsapp_num = data.creator_whatsapp or DEFAULT_CREATOR_PHONE
    bot_key = data.creator_callmebot_key or CALLMEBOT_API_KEY

    link = Link(
        slug=slug,
        link_type=data.link_type,
        question=data.question,
        target_name=data.target_name,
        creator_name=data.creator_name,
        creator_whatsapp=whatsapp_num,
        creator_callmebot_key=bot_key,
        creator_facebook=data.creator_facebook,
        creator_line=data.creator_line,
        creator_webhook=data.creator_webhook,
        google_credentials=data.google_credentials
    )
    db.add(link)
    db.commit()
    db.refresh(link)

    path_prefix = "d" if data.link_type == "date" else "z"
    return {
        "status": "success",
        "slug": link.slug,
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

    # Dispara alerta em tempo real para o dono no dashboard
    await dispatch_dodge_event(slug, link.total_dodges)

    return {"status": "ok", "total_dodges": link.total_dodges}

@router.get("/links/{slug}/schedule")
def get_schedule(slug: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.slug == slug).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link não encontrado")

    schedule = get_calendar_freebusy(link.google_credentials, days_ahead=30)
    return {"schedule": schedule}

@router.post("/links/{slug}/confirm_date")
async def confirm_date(slug: str, data: ConfirmDateRequest, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.slug == slug).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link não encontrado")

    link.accepted = True
    response = DateResponse(
        link_id=link.id,
        selected_date=data.selected_date,
        selected_time=data.selected_time,
        dodge_count=data.dodge_count,
        notes=data.notes
    )
    db.add(response)
    db.commit()

    # Cria o evento no Google Calendar caso conectado
    gcal_created = False
    if link.google_credentials:
        gcal_created = create_google_calendar_event(
            credentials_json_str=link.google_credentials,
            date_str=data.selected_date,
            time_slot=data.selected_time,
            target_name=link.target_name or "Crush",
            creator_name=link.creator_name or "Você"
        )

    # Dispara notificação automática em segundo plano
    await dispatch_date_confirmation(
        slug=link.slug,
        target_name=link.target_name or "Sua pretendente",
        selected_date=data.selected_date,
        selected_time=data.selected_time,
        creator_whatsapp=link.creator_whatsapp,
        creator_callmebot_key=link.creator_callmebot_key,
        creator_facebook=link.creator_facebook,
        creator_webhook=link.creator_webhook
    )

    return {
        "status": "success",
        "google_calendar_synced": gcal_created,
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
        selected_time="Noite",
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
            # Mantém conexão viva aguardando pings
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(slug, websocket)
