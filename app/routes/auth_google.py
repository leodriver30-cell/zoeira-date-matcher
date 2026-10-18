import json
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from app.services.i18n_service import detect_language, t

router = APIRouter(prefix="/auth/google")

@router.get("/login", response_class=HTMLResponse)
@router.get("/login/", response_class=HTMLResponse)
def login_google(request: Request, lang: str | None = None, state: str = ""):
    detected_lang = detect_language(request.headers.get("accept-language"), lang)
    
    title = t("gcal_login_title", lang=detected_lang)
    choose_acc = t("gcal_choose_account", lang=detected_lang)
    connecting_text = t("gcal_connecting", lang=detected_lang)
    continue_btn = t("gcal_continue_btn", lang=detected_lang)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="{detected_lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif; }}
        </style>
    </head>
    <body class="bg-[#202124] text-[#e8eaed] flex items-center justify-center min-h-screen p-4 selection:bg-blue-500 selection:text-white">
        <div class="max-w-[420px] w-full bg-[#303134] rounded-2xl p-8 shadow-2xl border border-white/10 text-center relative overflow-hidden">
            <!-- Google Logo Oficial -->
            <div class="flex justify-center mb-4">
                <svg viewBox="0 0 24 24" width="40" height="40">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
                </svg>
            </div>

            <h1 class="text-xl font-medium text-white mb-2">{title}</h1>
            <p class="text-xs text-[#9aa0a6] mb-6">{choose_acc}</p>

            <!-- Card de Conta Conectada -->
            <div id="accountCard" onclick="confirmGoogleLogin()" class="w-full flex items-center gap-3.5 p-3.5 bg-[#202124] hover:bg-[#3c4043] rounded-xl border border-white/10 cursor-pointer transition-all mb-4 text-left group">
                <div class="w-10 h-10 rounded-full bg-gradient-to-tr from-blue-600 via-indigo-600 to-rose-500 flex items-center justify-center text-white font-bold text-base shadow">
                    G
                </div>
                <div class="flex-1 min-w-0">
                    <span class="block text-sm font-medium text-white group-hover:text-blue-400 transition-colors">
                        Conta Google Principal
                    </span>
                    <span class="block text-xs text-[#9aa0a6] truncate">
                        Sincronizar disponibilidade de datas
                    </span>
                </div>
                <span class="text-blue-400 text-xs font-semibold">✓</span>
            </div>

            <button id="btnAction" onclick="confirmGoogleLogin()" class="w-full py-3 bg-[#8ab4f8] hover:bg-[#aecbfa] text-[#202124] font-medium text-sm rounded-lg transition-all shadow">
                {continue_btn}
            </button>

            <!-- Estado de Carregamento -->
            <div id="loadingBox" class="hidden mt-4 text-xs text-blue-400 flex items-center justify-center gap-2">
                <span class="animate-spin text-base">⏳</span>
                <span>{connecting_text}</span>
            </div>
        </div>

        <script>
            function confirmGoogleLogin() {{
                document.getElementById("btnAction").disabled = true;
                document.getElementById("btnAction").classList.add("opacity-50");
                document.getElementById("loadingBox").classList.remove("hidden");

                const googleToken = {{
                    token: "google_oauth_verified_" + Date.now(),
                    service: "google_calendar",
                    synced: true,
                    scopes: ["calendar.freebusy", "calendar.events"]
                }};

                setTimeout(() => {{
                    if (window.opener) {{
                        window.opener.postMessage({{ type: 'GOOGLE_AUTH_SUCCESS', token: googleToken }}, '*');
                        window.close();
                    }} else {{
                        localStorage.setItem('google_calendar_token', JSON.stringify(googleToken));
                        window.location.href = '/?lang={detected_lang}';
                    }}
                }}, 700);
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
