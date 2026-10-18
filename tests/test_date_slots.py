from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from fastapi.testclient import TestClient

from app.main import app
from app.services.i18n_service import resolve_timezone, format_time_range, format_tz_label

client = TestClient(app)


def test_timezone_resolution():
    # Browser timezone wins over language (e.g. Brazilian in Japan)
    assert resolve_timezone("Asia/Tokyo", "pt") == "Asia/Tokyo"
    # Fallback by language when browser timezone is missing or invalid
    assert resolve_timezone(None, "ja") == "Asia/Tokyo"
    assert resolve_timezone("", "en") == "America/New_York"
    assert resolve_timezone("Invalid/Zone", "es") == "Europe/Madrid"
    assert resolve_timezone(None, "pt") == "America/Sao_Paulo"


def test_time_range_and_tz_label():
    assert format_time_range("19:00", 180) == "19:00 – 22:00"
    assert format_time_range("22:30", 180) == "22:30 – 01:30"
    label_pt = format_tz_label("Asia/Tokyo", "pt")
    assert "Tóquio" in label_pt and "UTC+9" in label_pt


def test_create_date_link_and_confirm_flow():
    tz = ZoneInfo("Asia/Tokyo")
    today = datetime.now(tz).date()
    d1 = (today + timedelta(days=1)).strftime("%Y-%m-%d")
    d2 = (today + timedelta(days=2)).strftime("%Y-%m-%d")

    # 1. Create Date link with 2 days and exact times in Asia/Tokyo while using 'pt'
    resp = client.post("/api/links", json={
        "link_type": "date",
        "creator_name": "Leo",
        "target_name": "Yuki",
        "lang": "pt",
        "timezone": "Asia/Tokyo",
        "available_slots": [
            {"date": d1, "times": ["19:00", "20:00"]},
            {"date": d2, "times": ["12:00"]},
        ],
    })
    assert resp.status_code == 200, resp.text
    data = resp.json()
    slug = data["slug"]
    assert data["timezone"] == "Asia/Tokyo"

    # 2. Check date_view HTML renders custom days and locked timezone
    html_resp = client.get(f"/d/{slug}?lang=pt")
    assert html_resp.status_code == 200
    assert "Tóquio, Japão (UTC+9)" in html_resp.text
    assert d1 in html_resp.text
    # Switching language on recipient page keeps Asia/Tokyo timezone locked
    html_ja = client.get(f"/d/{slug}?lang=ja")
    assert html_ja.status_code == 200
    assert "日本・東京 (UTC+9)" in html_ja.text

    # 3. Reject invalid slot not offered by creator
    bad_confirm = client.post(f"/api/links/{slug}/confirm_date", json={
        "selected_date": d1,
        "selected_time": "15:00",
        "dodge_count": 2,
        "lang": "pt",
    })
    assert bad_confirm.status_code == 400

    # 4. Confirm valid slot
    ok_confirm = client.post(f"/api/links/{slug}/confirm_date", json={
        "selected_date": d1,
        "selected_time": "19:00",
        "dodge_count": 2,
        "lang": "pt",
    })
    assert ok_confirm.status_code == 200, ok_confirm.text
    confirm_json = ok_confirm.json()
    assert "19:00 – 22:00" in confirm_json["selected_time_display"]

    # 5. Confirming the exact same slot again returns HTTP 409 Conflict
    dup_confirm = client.post(f"/api/links/{slug}/confirm_date", json={
        "selected_date": d1,
        "selected_time": "19:00",
        "dodge_count": 0,
        "lang": "pt",
    })
    assert dup_confirm.status_code == 409


def test_validation_limits():
    tz = ZoneInfo("America/Sao_Paulo")
    today = datetime.now(tz).date()

    # Empty slots -> 422
    r_empty = client.post("/api/links", json={
        "link_type": "date",
        "creator_name": "Leo",
        "target_name": "Ana",
        "available_slots": [],
    })
    assert r_empty.status_code == 422

    # More than 10 days -> 422
    eleven_days = [
        {"date": (today + timedelta(days=i)).strftime("%Y-%m-%d"), "times": ["19:00"]}
        for i in range(1, 12)
    ]
    r_many = client.post("/api/links", json={
        "link_type": "date",
        "creator_name": "Leo",
        "target_name": "Ana",
        "available_slots": eleven_days,
    })
    assert r_many.status_code == 422

    # Invalid HH:MM format -> 422
    r_bad_time = client.post("/api/links", json={
        "link_type": "date",
        "creator_name": "Leo",
        "target_name": "Ana",
        "available_slots": [
            {"date": (today + timedelta(days=1)).strftime("%Y-%m-%d"), "times": ["25:99"]}
        ],
    })
    assert r_bad_time.status_code == 422

    # Beyond 95 days -> 422
    r_too_far = client.post("/api/links", json={
        "link_type": "date",
        "creator_name": "Leo",
        "target_name": "Ana",
        "available_slots": [
            {"date": (today + timedelta(days=100)).strftime("%Y-%m-%d"), "times": ["19:00"]}
        ],
    })
    assert r_too_far.status_code == 422


def test_expanded_calendar_horizon_two_months():
    tz = ZoneInfo("Asia/Tokyo")
    today = datetime.now(tz).date()
    # 60 days ahead (approx 2 months in advance, typical in Japan)
    d60 = (today + timedelta(days=60)).strftime("%Y-%m-%d")
    d75 = (today + timedelta(days=75)).strftime("%Y-%m-%d")

    resp = client.post("/api/links", json={
        "link_type": "date",
        "creator_name": "Leo",
        "target_name": "Sakura",
        "lang": "ja",
        "timezone": "Asia/Tokyo",
        "available_slots": [
            {"date": d60, "times": ["19:00", "20:00"]},
            {"date": d75, "times": ["18:30"]},
        ],
    })
    assert resp.status_code == 200, resp.text
    data = resp.json()
    slug = data["slug"]

    # Check recipient page renders the 60-day date
    html_resp = client.get(f"/d/{slug}?lang=ja")
    assert html_resp.status_code == 200
    assert d60 in html_resp.text

    # Confirm the 60-day advance date
    confirm_resp = client.post(f"/api/links/{slug}/confirm_date", json={
        "selected_date": d60,
        "selected_time": "19:00",
        "dodge_count": 1,
        "lang": "ja",
    })
    assert confirm_resp.status_code == 200
    assert "19:00 – 22:00" in confirm_resp.json()["selected_time_display"]


def test_creator_contact_isolation():
    tz = ZoneInfo("Asia/Tokyo")
    today = datetime.now(tz).date()
    d1 = (today + timedelta(days=1)).strftime("%Y-%m-%d")

    # 1. Link created without WhatsApp -> creator_whatsapp must be empty/none
    resp_empty = client.post("/api/links", json={
        "link_type": "date",
        "creator_name": "Marcos",
        "target_name": "Elena",
        "creator_whatsapp": "",
        "creator_line": "marcos_tokyo",
        "available_slots": [{"date": d1, "times": ["19:00"]}],
    })
    assert resp_empty.status_code == 200
    slug_empty = resp_empty.json()["slug"]

    # In date view, CREATOR_WHATSAPP must be empty, not any default phone
    html_empty = client.get(f"/d/{slug_empty}")
    assert 'const CREATOR_WHATSAPP = "";' in html_empty.text
    assert 'const CREATOR_LINE = "marcos_tokyo";' in html_empty.text

    # 2. Link created with a friend's phone number
    resp_friend = client.post("/api/links", json={
        "link_type": "date",
        "creator_name": "Carlos",
        "target_name": "Juliana",
        "creator_whatsapp": "5511999998888",
        "available_slots": [{"date": d1, "times": ["19:00"]}],
    })
    assert resp_friend.status_code == 200
    slug_friend = resp_friend.json()["slug"]

    html_friend = client.get(f"/d/{slug_friend}")
    assert 'const CREATOR_WHATSAPP = "5511999998888";' in html_friend.text


if __name__ == "__main__":
    test_timezone_resolution()
    test_time_range_and_tz_label()
    test_create_date_link_and_confirm_flow()
    test_validation_limits()
    test_expanded_calendar_horizon_two_months()
    test_creator_contact_isolation()
    print("ALL TESTS PASSED!")
