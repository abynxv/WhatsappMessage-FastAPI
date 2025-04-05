from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import httpx
import re
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Get credentials from environment
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

# WhatsApp Cloud API endpoint
META_API_URL = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

# Required headers for sending messages
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Function to validate international phone numbers (e.g., +919876543210)
def validate_phone_number(number: str) -> bool:
    pattern = r"^\+\d{10,15}$"  # E.164 format
    return re.match(pattern, number) is not None


@app.post("/send_message")
async def send_message(phone_number: str = Query(..., description="Phone number in E.164 format like +919876543210")):
    # Check if phone number format is valid
    if not validate_phone_number(phone_number):
        raise HTTPException(status_code=400, detail="Invalid phone number format. Use format like +919876543210.")

    # Message payload to be sent via WhatsApp Cloud API
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {
            "body": "Hello, this is a test message from our TMBC bot!"
        }
    }

    try:
        # Use an async HTTP client to send the request
        async with httpx.AsyncClient() as client:
            response = await client.post(META_API_URL, json=payload, headers=HEADERS)

        # Parse the response from WhatsApp API
        response_data = response.json()

        # If success, return message ID
        if response.status_code == 200:
            return {
                "status": "success",
                "message_id": response_data.get("messages", [{}])[0].get("id", "No message ID returned")
            }
        else:
            # If WhatsApp API returns an error, return the full error response
            return JSONResponse(status_code=response.status_code, content=response_data)

    except Exception as e:
        # Catch any unexpected errors (like network issues)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")