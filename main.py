from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
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
VERIFY_TOKEN = "your_custom_verify_token"

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
    
    
@app.get("/webhook")
async def verify_webhook(request: Request):
    """
    This GET method is called by Meta to verify your webhook URL.
    """
    params = dict(request.query_params)
    if (
        params.get("hub.mode") == "subscribe"
        and params.get("hub.verify_token") == "your_custom_verify_token"
    ):
        return int(params.get("hub.challenge"))
    raise HTTPException(status_code=403, detail="Verification failed")
    

@app.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()
    print("Received message:", body)

    try:
        # Navigate to the actual message (this is just a structure example)
        entry = body["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        messages = value.get("messages")

        if messages:
            from_number = messages[0]["from"]
            message_text = messages[0]["text"]["body"]
            print(f"New message from {from_number}: {message_text}")

        return {"status": "received"}

    except Exception as e:
        print("Error while parsing message:", e)
        return {"status": "error"}