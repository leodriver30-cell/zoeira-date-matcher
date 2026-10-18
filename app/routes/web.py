from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Link
from app.services.i18n_service import detect_language, t, SUPPORTED_LANGUAGES, TRANSLATIONS, TZ_CITY_NAMES, FALLBACK_TIMEZONES
from app.routes.api import build_availability_ViewModel
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
        "tz_city_names": TZ_CITY_NAMES,
        "fallback_timezones": FALLBACK_TIMEZONES,
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
    avail_vm = build_availability_ViewModel(link, display_lang=detected_lang)

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
        "is_legacy": avail_vm["is_legacy"],
        "custom_days": avail_vm["days"],
        "schedule": avail_vm["schedule"],
        "link_timezone": avail_vm["timezone"],
        "tz_label": avail_vm["tz_label"],
        "duration_min": avail_vm["duration_min"],
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
