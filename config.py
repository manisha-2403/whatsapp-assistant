
import os
from dotenv import load_dotenv

load_dotenv()

# --- Groq (free-tier AI for natural FAQ answers) ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# --- Google Sheets ---
GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "google_credentials.json")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# --- Your business info (fed to the AI so it answers in your context) ---
BUSINESS_NAME = os.getenv("BUSINESS_NAME", "Our Business")
BUSINESS_CONTEXT = os.getenv(
    "BUSINESS_CONTEXT",
    "A small business that takes orders and booking requests over WhatsApp."
)

# Note: Twilio's WhatsApp Sandbox doesn't need any credentials in this file —
# app.py replies directly via TwiML in the webhook response. If you later
# move off the Sandbox to a paid Twilio WhatsApp sender, you'd add
# TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN here for outbound REST calls.
