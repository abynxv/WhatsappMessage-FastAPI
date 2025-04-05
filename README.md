# 📩 WhatsApp Cloud API with FastAPI

This project demonstrates how to send WhatsApp messages using the Meta (Facebook) WhatsApp Cloud API and FastAPI.

---

## 🚀 Features

- FastAPI-based REST endpoint `/send_message`
- Sends WhatsApp message to a given number
- Phone number validation (E.164 format)
- Uses Meta WhatsApp Cloud API
- `.env` support for secure token storage

---

## 📦 Requirements

- Python 3.8+
- A Meta Developer account with WhatsApp Product enabled
- A verified test number in WhatsApp Cloud API
- Access Token and Phone Number ID

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/whatsapp-fastapi.git
cd whatsapp-fastapi
```

## Create a virtual environment

```bash
python -m venv venv
Activate it:
venv\Scripts\activate
On macOS/Linux:
source venv/bin/activate
```
## Install dependencies

pip install -r requirements.txt

## Create a .env file in the root folder

WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here
WHATSAPP_ACCESS_TOKEN=your_access_token_here

## Run the App

uvicorn main:app --reload

## Test the Endpoint
Postman:

    Method: POST

    URL: http://127.0.0.1:8000/send_message

    Query Param: phone_number = +917034654496

    ⚠️ Important Note: If you're testing in a browser or curl, the + sign must be URL-encoded as %2B.
    Example: +917034654496 → %2B917034654496 and make sure you have included .env in .gitignore file to prevent sensitive files from being uploaded to GitHub.

