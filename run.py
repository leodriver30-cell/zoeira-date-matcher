import sys
import uvicorn
from app.config import HOST, PORT

if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    print(f"\n[OK] Servidor de Zoeiras & Dates rodando em: http://localhost:{PORT}\n")
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=False)
