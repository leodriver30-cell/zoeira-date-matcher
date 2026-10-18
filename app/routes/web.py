from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Link
from app.services.i18n_service import detect_language, t, SUPPORTED_LANGUAGES, TRANSLATIONS
from app.services.google_calendar import get_calendar_freebusy
from pathlib import Path

router = APIRouter()
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/", response_class=HTMLResponse)
async def index_page(request: Request, lang: str | None = None):
    detected_lang = detect_language(request.headers.get("accept-language"), lang)
    context = {
        "request": request,
        "lang": detected_lang,
        "supported_languages": SUPPORTED_LANGUAGES,
        "translations": TRANSLATIONS,
        "t": lambda k, **kw: t(k, lang=detected_lang, **kw)
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)

@router.get("/z/{slug}", response_class=HTMLResponse)
async def prank_view_page(slug: str, request: Request, lang: str | None = None, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.slug == slug).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link não encontrado")

    link.views += 1
    db.commit()

    detected_lang = detect_language(request.headers.get("accept-language"), lang)
    context = {
        "request": request,
        "link": link,
        "lang": detected_lang,
        "supported_languages": SUPPORTED_LANGUAGES,
        "translations": TRANSLATIONS,
        "t": lambda k, **kw: t(k, lang=detected_lang, **kw)
    }
    return templates.TemplateResponse(request=request, name="prank_view.html", context=context)

@router.get("/d/{slug}", response_class=HTMLResponse)
async def date_view_page(slug: str, request: Request, lang: str | None = None, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.slug == slug).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link não encontrado")

    link.views += 1
    db.commit()

    detected_lang = detect_language(request.headers.get("accept-language"), lang)
    schedule = get_calendar_freebusy(link.google_credentials, days_ahead=30)

    # Formata a pergunta romântica personalizada com o nome
    target_name = link.target_name or ("você" if detected_lang == "pt" else "you")
    personalized_question = t("default_date_question", lang=detected_lang, name=target_name)
    if link.question:
        personalized_question = link.question.replace("{name}", target_name)

    context = {
        "request": request,
        "link": link,
        "target_name": target_name,
        "creator_name": link.creator_name or "Ele",
        "question": personalized_question,
        "schedule": schedule,
        "lang": detected_lang,
        "supported_languages": SUPPORTED_LANGUAGES,
        "translations": TRANSLATIONS,
        "t": lambda k, **kw: t(k, lang=detected_lang, **kw)
    }
    return templates.TemplateResponse(request=request, name="date_view.html", context=context)

@router.get("/dash/{slug}", response_class=HTMLResponse)
async def dashboard_page(slug: str, request: Request, lang: str | None = None, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.slug == slug).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link não encontrado")

    detected_lang = detect_language(request.headers.get("accept-language"), lang)
    context = {
        "request": request,
        "link": link,
        "responses": link.responses,
        "lang": detected_lang,
        "supported_languages": SUPPORTED_LANGUAGES,
        "translations": TRANSLATIONS,
        "t": lambda k, **kw: t(k, lang=detected_lang, **kw)
    }
    return templates.TemplateResponse(request=request, name="dashboard.html", context=context)
