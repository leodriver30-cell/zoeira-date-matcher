from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.database import engine, Base
from app.routes.web import router as web_router
from app.routes.api import router as api_router
from app.routes.auth_google import router as auth_google_router

# Cria as tabelas do banco de dados SQLite automaticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Zoeira & Date Matcher",
    description="Plataforma de zoeiras com amigos e agendamento de dates com botão fujão e Google Calendar",
    version="1.0.0"
)

STATIC_DIR = Path(__file__).resolve().parent / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Inclui roteadores
app.include_router(web_router)
app.include_router(api_router)
app.include_router(auth_google_router)
