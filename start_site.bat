@echo off
title Zoeiras e Dates - Servidor + Tunel Publico
echo ========================================================
echo   Iniciando Servidor Web e Tunel Publico Cloudflare...
echo ========================================================
start "" "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" run.py
timeout /t 2 >nul
start "" "%~dp0cloudflared.exe" tunnel --url http://localhost:8050
echo.
echo [OK] O servidor e o tunel foram iniciados!
echo O link publico comecando com https://...trycloudflare.com
echo aparecera na janela do Cloudflare.
echo ========================================================
