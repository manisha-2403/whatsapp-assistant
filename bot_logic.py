
import ai_service
import sheets_service

SESSIONS = {}  # phone_number -> {"flow": str|None, "step": int, "data": dict}

MENU_TEXT = (
    "Hi! 👋 How can I help?\n"
    "1️⃣ Place an order\n"
    "2️⃣ Book an appointment\n"
    "3️⃣ Ask a question\n\n"
    "Just reply with 1, 2, or 3 — or ask me anything."
)

GREETINGS = {"hi", "hello", "hey", "menu", "start", "hii", "hola"}


def _session(phone):
    return SESSIONS.setdefault(phone, {"flow": None, "step": 0, "data": {}, "history": []})


def _remember(phone, role, content):
    s = _session(phone)
    s["history"].append({"role": role, "content": content})
    s["history"] = s["history"][-10:]


def handle_message(phone: str, text: str) -> str:
    text = text.strip()
    s = _session(phone)
    _remember(phone, "user", text)

    # Active guided flow takes priority over everything else
    if s["flow"] == "order":
        reply = _continue_order(phone, text)
    elif s["flow"] == "booking":
        reply = _continue_booking(phone, text)
    elif text.lower() in GREETINGS:
        reply = MENU_TEXT
    elif text.strip() == "1" or "order" in text.lower():
        reply = _start_order(phone)
    elif text.strip() == "2" or any(k in text.lower() for k in ["book", "appointment", "reservation", "reserve"]):
        reply = _start_booking(phone)
    elif text.strip() == "3":
        reply = "Sure — what would you like to know?"
    else:
        faqs = sheets_service.get_faqs()
        reply = ai_service.answer_question(text, faqs, history=s["history"])

    _remember(phone, "assistant", reply)
    return reply


# ---------------- Order flow ----------------

def _start_order(phone):
    s = _session(phone)
    s["flow"], s["step"], s["data"] = "order", 1, {}
    return "Great! What would you like to order? (list item names and quantities)"


def _continue_order(phone, text):
    s = _session(phone)
    if s["step"] == 1:
        s["data"]["items"] = text
        s["step"] = 2
        return "Got it. Any notes — delivery address, pickup time, allergies, etc.? (or reply 'none')"
    elif s["step"] == 2:
        s["data"]["notes"] = "" if text.lower() == "none" else text
        sheets_service.log_order(phone, s["data"]["items"], s["data"]["notes"])
        s["flow"], s["step"], s["data"] = None, 0, {}
        return "✅ Order received! We'll confirm shortly. Reply 'menu' anytime for more options."
    return _start_order(phone)  # fallback safety


# ---------------- Booking flow ----------------

def _start_booking(phone):
    s = _session(phone)
    s["flow"], s["step"], s["data"] = "booking", 1, {}
    return "Let's book you in! What's your name?"


def _continue_booking(phone, text):
    s = _session(phone)
    if s["step"] == 1:
        s["data"]["name"] = text
        s["step"] = 2
        return "Thanks! What service are you booking?"
    elif s["step"] == 2:
        s["data"]["service"] = text
        s["step"] = 3
        return "What date works for you? (e.g. 15 Sept)"
    elif s["step"] == 3:
        s["data"]["date"] = text
        s["step"] = 4
        return "And what time?"
    elif s["step"] == 4:
        s["data"]["time"] = text
        sheets_service.log_booking(
            phone, s["data"]["name"], s["data"]["service"], s["data"]["date"], s["data"]["time"]
        )
        s["flow"], s["step"], s["data"] = None, 0, {}
        return "✅ Booking request received! We'll confirm your slot shortly. Reply 'menu' for more options."
    return _start_booking(phone)  # fallback safety
