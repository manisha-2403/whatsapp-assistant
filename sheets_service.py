
import datetime
import gspread
from google.oauth2.service_account import Credentials
import config

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

_client = None
_sheet = None


def _get_sheet():
    """Lazily connect so the app doesn't crash on import if creds aren't set yet."""
    global _client, _sheet
    if _sheet is None:
        creds = Credentials.from_service_account_file(
            config.GOOGLE_SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        _client = gspread.authorize(creds)
        _sheet = _client.open_by_key(config.GOOGLE_SHEET_ID)
    return _sheet


def get_faqs():
    """Returns a list of {"question": ..., "answer": ...} dicts from the FAQs tab."""
    ws = _get_sheet().worksheet("FAQs")
    rows = ws.get_all_records()  # uses row 1 as headers
    return [
        {"question": r.get("Question", ""), "answer": r.get("Answer", "")}
        for r in rows
        if r.get("Question")
    ]


def log_order(phone: str, items: str, notes: str = ""):
    ws = _get_sheet().worksheet("Orders")
    ws.append_row([
        datetime.datetime.now().isoformat(timespec="seconds"),
        phone,
        items,
        notes,
        "New",
    ])


def log_booking(phone: str, name: str, service: str, date: str, time: str):
    ws = _get_sheet().worksheet("Bookings")
    ws.append_row([
        datetime.datetime.now().isoformat(timespec="seconds"),
        phone,
        name,
        service,
        date,
        time,
        "Pending",
    ])
