import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DB_PATH = BASE_DIR / "data.db"

# Porta e Host
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8050))

# Chaves pré-configuradas dos Robôs
CALLMEBOT_API_KEY = os.getenv("CALLMEBOT_API_KEY", "")
DEFAULT_CREATOR_PHONE = os.getenv("DEFAULT_CREATOR_PHONE", "")

# Facebook Messenger Bot (Meta Graph API / Webhook)
FACEBOOK_PAGE_TOKEN = os.getenv("FACEBOOK_PAGE_TOKEN", "")
FACEBOOK_WEBHOOK_URL = os.getenv("FACEBOOK_WEBHOOK_URL", "")

# Webhook genérico de notificações
DEFAULT_WEBHOOK_URL = os.getenv("DEFAULT_WEBHOOK_URL", "")

# Chave secreta para sessões
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-zoeira-key-1234567890")
