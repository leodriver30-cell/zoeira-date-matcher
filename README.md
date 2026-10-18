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

**Zoeira & Date Matcher** is a full-featured, modern web application designed for playful social interactions and romantic date invitations. Using playful psychological UI patterns, the app makes saying **"NO"** practically impossible through an evasive button and a mischievous animated kitten—leaving **"YES"** as the only inevitable choice!

The platform features two distinct interactive modes:
1. **😂 Friend Prank Mode**: Humorous trick links where the "NO" button flees indefinitely, tracking dodge attempts before presenting a hilarious celebration card.
2. **💖 Romantic Date Mode**: Personalized date invitation pages featuring interactive availability calendars, time slot selection (Evening, Afternoon, Morning), Google Calendar synchronization, and automated 1-click confirmation sharing via **LINE**, **WhatsApp**, and **Facebook Messenger**.

---

## ✨ Key Features

### 🐱 1. Responsive Mischievous Cat Button Evasion System
- **Dual-Phase Evasion**:
  - *Phase 1*: The "NO" button dodges to another corner within safe card boundaries.
  - *Phase 2 (The Cat Heist)*: A mischievous cartoon cat (`🐈`) pounces onto the button, displays a comic speech bubble (*"That 'NO' is mine now! 😼💨"*), steals the button, and scampers across the screen leaving a trail of paw prints (`🐾🐾🐾`).
- **Mobile Touch Debouncing**: Built-in 350ms touch debounce lock preventing mobile browsers from skipping straight to the end due to concurrent `pointerdown`, `touchstart`, and `click` triggers.
- **Dynamic Viewport Scaling**: Scampers are calculated relative to `window.innerWidth`, ensuring optimal theatrical visibility on both 375px mobile screens and ultra-wide desktop monitors.
- **Irresistible "YES" Highlight**: Once the "NO" button is stolen, the "YES" button automatically expands, pulsates, and glows with romantic hearts.

### 📅 2. Interactive Calendar & Date Scheduling
- **Visual Availability Grid**: Shows selectable open dates vs. occupied dates across the upcoming 30 days.
- **Time Slot Preferences**: Allows selecting preferred periods (🌙 Evening, ☀️ Afternoon, ☕ Morning / Lunch).
- **1-Click Google Calendar Generator**: Automatically builds pre-filled Google Calendar event URLs (`calendar.google.com/calendar/render?...`) with custom title, date ranges, and event details.

### 🟢 3. Smart Multi-Platform Messaging Pipeline
- **Single Smart LINE Button**:
  - Automatically copies the localized confirmation message to the recipient's clipboard:
    > *"Hey Leo! I'd love to go on a date with you! I picked 2026-10-25 (Evening)! 🥂✨"*
  - Displays an animated toast notification (*"Message copied! Add on LINE and paste into chat!"*).
  - Deep-links directly to the creator's LINE profile card (`https://line.me/ti/p/~{LINE_ID}`) where the crush can simply tap **Add Friend (友だち追加)** and paste the message into chat.
- **WhatsApp Click-to-Chat & Bot Support**:
  - Pre-filled direct message links (`wa.me/...`).
  - Automated hands-free background webhook notifications via **CallMeBot** API.
- **Facebook Messenger Integration**: Direct routing to creator profiles (`m.me/{username}`).

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
  - Instant live popup alerts when a date date/time is selected.

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
│  - i18n Translation Engine (`i18n_service.py`)         │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│                 Data & Integrations                    │
│  - SQLite Database via SQLAlchemy ORM                  │
│  - Google Calendar API (OAuth 2.0 FreeBusy API)        │
│  - Cloudflare Tunnels (Zero-Trust HTTPS Public Access) │
└────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
├── app/
│   ├── routes/
│   │   ├── api.py                 # REST endpoints (link generation, dodges, confirmations)
│   │   ├── web.py                 # HTML view routes (Home, Prank, Date, Dashboard)
│   │   └── auth_google.py         # Google OAuth 2.0 authentication endpoints
│   ├── services/
│   │   ├── i18n_service.py        # Centralized 4-language dictionary & detection
│   │   ├── notification_dispatcher.py  # CallMeBot & Facebook Messenger webhooks
│   │   └── google_calendar.py     # Calendar FreeBusy query helper
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
   *(Edit `.env` if you want to configure CallMeBot or Google Calendar OAuth)*

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
