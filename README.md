# 💖 Zoeira & Date Matcher (いたずら＆デートプランナー)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/i18n-EN%20%7C%20JA%20%7C%20PT%20%7C%20ES-E11D48?style=for-the-badge" alt="Languages" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License" />
</p>

<p align="center">
  <b>English</b> | <a href="README.ja.md">日本語 (N3レベル・わかりやすい解説)</a>
</p>

---

## 📖 Overview

**Zoeira & Date Matcher** is a full-featured, modern web application designed for playful social interactions and romantic date invitations. Using playful psychological UI patterns, the app makes saying **"NO"** practically impossible through an evasive button, an animated mischievous kitten, and clever hiding mechanics—leaving **"YES"** as the only inevitable choice!

The platform features two distinct interactive modes:
1. **😂 Friend Prank Mode**: Humorous trick links where the "NO" button dodges **7 times** across the screen. On the **8th attempt**, it slides directly behind the "YES" button and disappears completely (invisible, unclickable, zero edges peeking out), forcing the friend to click **"YES"**!
2. **💖 Romantic Date Mode**: Personalized date invitations where the creator selects up to **10 free days** across a **90-day (~3 month) advance calendar** with **exact 3-hour time slots** (e.g., `19:00 – 22:00`), interactive month navigation tabs, locked browser timezone, and 1-click confirmation sharing via **LINE**, **WhatsApp**, and **Facebook Messenger**.

---

## ✨ Key Features

### 😂 1. Modo Zoeira: 7-Dodge & Button Hiding Evasion
- **7 Evasive Dodges**: When the friend tries to click "NO", the button dodges and teleports away across 7 dynamic attempts.
- **Stealth Hide Behind "YES"**: On the 8th dodge, the "NO" button slides smoothly directly behind the "YES" button, scales down (`scale(0.5)`), and is rendered completely invisible and unclickable (`opacity: 0`, `visibility: hidden`, `pointer-events: none`, `disabled = true`), leaving "YES" as the only possible option!
- **Playful Dynamic Hints**: Comic speech bubbles and hints update on every attempt ("Tried clicking No? Don't even try! 😂").

### 🐱 2. Mischievous Cat Button Heist (Date Invitation Phase)
- **The Cat Heist**: In the date invitation phase, a mischievous cartoon cat (`🐈`) pounces onto the button, displays a comic speech bubble (*"That 'NO' is mine now! 😼💨"*), steals the button, and scampers across the screen leaving a trail of paw prints (`🐾🐾🐾`).
- **Irresistible "YES" Highlight**: Once the "NO" button vanishes, the "YES" button expands, pulsates, and glows with romantic hearts.

### 📅 3. 90-Day Advance Calendar with Month Tabs & Exact 3h Slots
- **Up to 90 Days (~3 Months) Ahead**: Built specifically to support scheduling customs in Japan and worldwide where dates are often planned 1 to 2+ months in advance.
- **Interactive Month Navigation Tabs**: Quick filter pills (`[ All Months ]`, `[ October ]`, `[ November ]`, `[ December ]`, etc.) with badges showing how many days are booked in each month.
- **Creator-Controlled Availability**: Creators select up to **10 free days** and define **exact time slots** (e.g., `19:00 – 22:00`, 3-hour standard duration) with presets, custom `<input type="time">`, and a 1-click *"Apply to all days"* button.
- **Automatic Browser Timezone Detection**: Automatically locks the invitation to the creator's browser timezone (`Intl.DateTimeFormat().resolvedOptions().timeZone`), with language-based fallbacks (`ja` → Tokyo, `en` → New York, `es` → Madrid, `pt` → Brasília). Changing `?lang=` on the recipient page translates UI texts without shifting the timezone.
- **1-Click Google Calendar Template**: Generates a pre-filled link (`calendar.google.com/calendar/render?...`) with the exact 3-hour duration, midnight rollover support, and locked timezone parameter (`ctz`).

### 🟢 4. Isolated Creator Contacts (Zero Hardcoded Data)
- **100% Privacy & Isolation**: No personal phone numbers or LINE IDs are hardcoded in the codebase. Each creator uses their own channels:
  - **LINE**: Pre-filled confirmation message with 1-click clipboard copy + deep link to the creator's LINE profile (`line.me/ti/p/~{LINE_ID}`).
  - **WhatsApp**: Click-to-chat link (`wa.me/...`) and optional automated background webhook via CallMeBot.
  - **Facebook Messenger**: Direct link to profile (`m.me/{username}`).
  - **Universal Fallback**: If no social channels are configured, only the **"Copy Ready Message"** and **"Add to Google Calendar"** buttons appear.

### 🌐 4. Full 4-Language Internationalization (i18n)
- Seamless real-time language switching:
  - 🇺🇸 **English** (`en`)
  - 🇯🇵 **日本語** (`ja`)
  - 🇧🇷 **Português** (`pt`)
  - 🇪🇸 **Español** (`es`)
- Automatic language negotiation based on browser headers with persistent query parameter overrides (`?lang=ja`).

### 📊 5. Real-Time Live WebSocket Dashboard
- Creators can monitor link interactions live without manual page reloads:
  - Real-time visitor counters.
  - Dodge attempt counts.
  - Instant live popup alerts when a date/time is selected.

---

## 🛠️ Tech Stack & Architecture

```
┌────────────────────────────────────────────────────────┐
│                      Frontend                          │
│  - HTML5, Jinja2 Templates, Vanilla JavaScript (ES6+) │
│  - Tailwind CSS (Utility-first responsive styling)    │
│  - Canvas Confetti (Celebration effects)               │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTP / WebSockets
┌──────────────────────────▼─────────────────────────────┐
│                   Backend (FastAPI)                    │
│  - Python 3.12 + Uvicorn ASGI Server                   │
│  - RESTful APIs (`/api/links`, `/confirm_date`, etc.)  │
│  - WebSocket Connection Manager (Live Dashboard alerts)│
│  - i18n & Timezone Engine (`i18n_service.py`)          │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│                 Data & Integrations                    │
│  - SQLite Database via SQLAlchemy ORM                  │
│  - Custom Slot & Timezone Availability Engine          │
│  - Cloudflare Tunnels (Zero-Trust HTTPS Public Access) │
└────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
├── app/
│   ├── routes/
│   │   ├── api.py                 # REST endpoints (link generation, dodges, slot validation)
│   │   └── web.py                 # HTML view routes (Home, Prank, Date, Dashboard)
│   ├── services/
│   │   ├── i18n_service.py        # Centralized 4-language dictionary & timezone engine
│   │   └── notification_dispatcher.py  # CallMeBot & Facebook Messenger webhooks
│   ├── static/
│   │   ├── css/                   # Custom styling and keyframe animations
│   │   └── js/                    # Client-side i18n helper
│   ├── templates/
│   │   ├── base.html              # Shared layout, navbar, language selector
│   │   ├── index.html             # Link creation studio with tab selector
│   │   ├── prank_view.html        # Interactive friend prank page
│   │   ├── date_view.html         # Romantic date invitation with cat & calendar
│   │   └── dashboard.html         # Real-time WebSocket monitoring panel
│   ├── config.py                  # Environment variable configuration
│   ├── database.py                # SQLAlchemy engine & session factory
│   └── models.py                  # Database schemas (Link, LinkResponse)
├── .env.example                   # Environment configuration template
├── .gitignore                     # Git ignore rules (secrets, db, binaries)
├── requirements.txt               # Python package dependencies
├── run.py                         # Application launcher (Port 8050)
├── start_site.bat                 # Windows one-click local server + tunnel script
└── README.md                      # Project documentation
```

---

## 🚀 Getting Started (Local Setup)

### Prerequisites
- **Python 3.10+** (Python 3.12 recommended)
- A modern web browser

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/zoeira-date-matcher.git
   cd zoeira-date-matcher
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   # Copy template
   cp .env.example .env
   ```
   *(Edit `.env` if you want to configure CallMeBot or Facebook Messenger bots)*

5. **Run the server**:
   ```bash
   python run.py
   ```
   The application will start on **`http://localhost:8050`**.

---

## 🌐 24/7 Always-Online Deployment Guide

To share links with friends across the world without keeping your personal computer running, you can deploy this project to a cloud platform:

### Method 1: Render.com (Recommended Free/Low-Cost)
1. Fork or push this repository to your GitHub account.
2. Sign in to [Render.com](https://render.com) and click **New Web Service**.
3. Connect your GitHub repository.
4. Set the configuration:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. In the **Environment Variables** tab, add any optional keys from `.env.example`.
6. Click **Deploy Web Service**! Render will provide a free permanent HTTPS domain (e.g., `https://your-app.onrender.com`).

### Method 2: Railway.app / Fly.io
- Simply link your GitHub repository. Railway and Fly automatically detect FastAPI and will run `uvicorn app.main:app` out-of-the-box.

### Method 3: Cloudflare Quick Tunnel (Local Testing)
- If running locally on your computer, use `cloudflared`:
  ```bash
  cloudflared tunnel --url http://localhost:8050
  ```
  This generates a public `https://...trycloudflare.com` URL instantly without any port-forwarding!

---

## 🔒 Security & Privacy Notes

- All sensitive keys (WhatsApp API keys, OAuth secrets, database files) are strictly excluded from version control via `.gitignore`.
- Database files (`data.db`) are created locally on startup and run safely on SQLite.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). Feel free to use, customize, and share!

---

<p align="center">
  Crafted with ❤️ for laughter, dates, and unforgettable memories.
</p>
