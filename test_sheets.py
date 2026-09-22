"""
Run this directly to see the REAL reason the Google Sheets connection is
failing (gspread was hiding it behind a JSONDecodeError). Delete this file
once things are working -- it's just for debugging.
"""
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
import requests
import config

print("Service account file:", config.GOOGLE_SERVICE_ACCOUNT_FILE)
print("Sheet ID from .env:  ", config.GOOGLE_SHEET_ID)
print()

creds = Credentials.from_service_account_file(
    config.GOOGLE_SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/spreadsheets"],
)
creds.refresh(Request())
print("Service account email:", creds.service_account_email)
print()

url = f"https://sheets.googleapis.com/v4/spreadsheets/{config.GOOGLE_SHEET_ID}"
resp = requests.get(url, headers={"Authorization": f"Bearer {creds.token}"})

print("HTTP status code:", resp.status_code)
print("Response body:")
print(resp.text[:1000])
