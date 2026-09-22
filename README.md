# WhatsApp Business Assistant (Python, $0 cost)

Handles FAQs (via a free AI API grounded in your own answers), guided order
collection, and guided booking requests — all logged to a Google Sheet.

**Stack:** Python + Flask · Twilio Sandbox for WhatsApp (free, no Meta/Facebook
account needed) · Groq free-tier AI · Google Sheets as your database (free)

---

## Before you start: an honest note on "free" and on limits

- **Twilio's WhatsApp Sandbox is free**, no credit card needed, and — unlike
  Meta's Cloud API — doesn't require a Facebook account at all. The
  trade-off: it only works with phone numbers that have explicitly
  "joined" your sandbox by sending a join code first. It's built for
  testing/demos, not for messaging arbitrary real customers yet.
- To go live with real customers later, you'd eventually apply for a
  proper Twilio WhatsApp sender, which — like every official WhatsApp
  route — ultimately requires Meta Business verification behind the
  scenes. That's a bridge to cross later, not something you need today.
- Groq's API is free with no card required as of this writing, but free-tier
  limits on any AI provider can change. If you hit limits, check
  [console.groq.com](https://console.groq.com).

---

## What you need (all free accounts)

- A Twilio account (email signup only — no Facebook, no card for the Sandbox)
- A Google account
- A Groq account (console.groq.com)
- Python 3.10+ and VS Code
- [ngrok](https://ngrok.com) (free) — lets Twilio reach your laptop while you develop

---

## Step 1 — Twilio WhatsApp Sandbox setup

1. Sign up at [twilio.com](https://www.twilio.com/try-twilio) (free trial, no card needed for the Sandbox).
2. In the Twilio Console, go to **Messaging → Try it out → Send a WhatsApp message**.
3. You'll see a Sandbox number and a join code, like `join happy-lion`. From your own WhatsApp, send that exact phrase to the Sandbox number (or scan the QR code shown) — this "joins" your number as a tester.
4. Leave this page open — you'll set the webhook URL here after Step 4.

## Step 2 — Google Sheet + service account

1. Create a new Google Sheet. Add 3 tabs (exact names):
   - `FAQs` with headers `Question | Answer` — fill in a few rows
   - `Orders` with headers `Timestamp | Phone | Items | Notes | Status`
   - `Bookings` with headers `Timestamp | Phone | Name | Service | Date | Time | Status`
2. Copy the Sheet ID from its URL: `docs.google.com/spreadsheets/d/THIS_PART/edit`
3. Go to [console.cloud.google.com](https://console.cloud.google.com) → create a project → enable **Google Sheets API** and **Google Drive API**. Skip any "activate billing" prompt — it's not needed for this.
4. Go to **IAM & Admin → Service Accounts → Create Service Account**. Then **Keys → Add Key → JSON** — this downloads a file; rename it `google_credentials.json` and put it in the project folder.
5. Open the JSON file, copy the `client_email` address, and **share your Google Sheet** with that email as **Editor**.

## Step 3 — Groq free API key

1. Go to [console.groq.com](https://console.groq.com), sign up, and create an API key.

## Step 4 — Run it locally in VS Code

```bash
# in VS Code's terminal, inside the project folder
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
cp .env.example .env         # then fill in every value in .env
```

Fill in `.env` with your Groq key and Google Sheet ID from Steps 2-3.
(No Twilio credentials needed in `.env` — see Step 1's note below.)

Start the server:
```bash
python app.py
```

## Step 5 — Expose it with ngrok and connect the webhook

```bash
ngrok http 5000
```
Copy the `https://xxxx.ngrok-free.app` URL it gives you.

Back in the Twilio Console page from Step 1, under **Sandbox Configuration**,
in the **"When a message comes in"** field, enter:
```
https://xxxx.ngrok-free.app/webhook
```
Make sure the method is set to **HTTP POST**, then click **Save**.

## Step 6 — Test it

From the WhatsApp number you joined the sandbox with, message the Sandbox
number: "hi". You should get the menu back, and orders/bookings should
appear as new rows in your Google Sheet within a few seconds.

If your sandbox session goes quiet, Twilio may ask you to re-send the join
code after a period of inactivity — this is a known Sandbox limitation, not
a bug in your code. [Medium confidence on the exact timing — check the
Sandbox page in your Twilio Console if messages stop getting replies.]

---

## Going from "test" to "real business"

- The Sandbox can only talk to numbers that joined with your code — it's
  not reachable by the general public.
- To message real customers, you'd apply for a proper Twilio WhatsApp
  sender ("Twilio Senders" in the Console), which involves the same kind
  of Meta Business verification that the official Cloud API needs — so
  you may end up needing a Facebook account eventually if you scale this
  up. That's a later problem, not a blocker today.
- ngrok's free URL changes every restart — re-paste it into Twilio's
  Sandbox Configuration each time, or for a real deployment, host `app.py`
  somewhere always-on (check current free-tier terms on providers like
  Render or Railway, they change often).
- Conversation state currently lives in memory and resets if the app
  restarts — fine at low volume, but move it into a Sheet tab or SQLite
  file if that becomes a problem.

## File overview

| File | Purpose |
|---|---|
| `app.py` | Flask webhook — receives WhatsApp messages, replies via TwiML |
| `bot_logic.py` | Menu, order flow, booking flow, FAQ fallback |
| `ai_service.py` | Calls Groq's free API for natural FAQ answers |
| `sheets_service.py` | Reads FAQs / writes Orders & Bookings to Google Sheets |
| `config.py` | Loads all settings from `.env` |
