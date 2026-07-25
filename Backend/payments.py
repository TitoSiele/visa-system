import os
import base64
import requests
from datetime import datetime

MPESA_ENV = os.getenv("MPESA_ENV", "sandbox")  # "sandbox" or "production"
MPESA_BASE_URL = (
    "https://sandbox.safaricom.co.ke" if MPESA_ENV == "sandbox"
    else "https://api.safaricom.co.ke"
)

CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")
SHORTCODE = os.getenv("MPESA_SHORTCODE", "174379")  # 174379 is the standard sandbox test shortcode
PASSKEY = os.getenv("MPESA_PASSKEY")
CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL")  # must be a public HTTPS URL — use ngrok in dev


def get_access_token() -> str:
    url = f"{MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    resp = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET), timeout=10)
    resp.raise_for_status()
    return resp.json()["access_token"]


def _password_and_timestamp():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    raw = f"{SHORTCODE}{PASSKEY}{timestamp}"
    password = base64.b64encode(raw.encode()).decode()
    return password, timestamp


def normalize_phone(phone: str) -> str:
    """Convert 07xxxxxxxx or +2547xxxxxxxx to 2547xxxxxxxx, which Daraja requires."""
    phone = phone.strip().replace(" ", "")
    if phone.startswith("+"):
        phone = phone[1:]
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    if not phone.startswith("254"):
        raise ValueError("Enter a Kenyan phone number, e.g. 0712345678")
    return phone


def initiate_stk_push(phone_number: str, amount: int, account_reference: str, description: str = "Visa Application Fee"):
    token = get_access_token()
    password, timestamp = _password_and_timestamp()
    phone = normalize_phone(phone_number)

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": account_reference[:12],
        "TransactionDesc": description,
    }
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(
        f"{MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest",
        json=payload, headers=headers, timeout=15,
    )
    print(f"MPESA RAW RESPONSE ({resp.status_code}): {resp.text}")
    resp.raise_for_status()
    return resp.json()