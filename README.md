## 📱 WhatsApp Messaging Project with FastAPI

This project demonstrates how to send and receive WhatsApp messages using the Meta (Facebook) WhatsApp Cloud API and FastAPI.
🔧 What the Project Does

    ✅ Send WhatsApp Messages: A FastAPI endpoint sends messages using httpx.AsyncClient to the Meta Cloud API.

    📩 Receive Messages: Another endpoint acts as a webhook to receive incoming messages sent to your WhatsApp Business test number.

    🔁 Webhook Verification: The project includes a verification step that allows Meta to confirm your callback URL when setting up the webhook.

🔐 What is hub.verify_token and Why Do We Need It?

When you set up a webhook in Meta's developer dashboard, Meta needs to verify that the URL you're providing is actually yours. So it sends a GET request to your webhook endpoint with these parameters:

    hub.mode

    hub.verify_token → you define this value (like a secret password)

    hub.challenge → a random number you need to return

How to Use It:

    In your FastAPI code (GET /webhook), you check if:

        hub.mode == "subscribe"

        hub.verify_token matches your secret (e.g., "my_custom_token")

    If yes → return the value of hub.challenge

    This proves to Meta that the webhook URL is yours and it's safe to start sending you message data.

🛠 Technologies Used

    FastAPI: High-performance Python web framework for building APIs.

    httpx.AsyncClient: Asynchronous HTTP client used to send POST requests to the WhatsApp Cloud API.

    Uvicorn: ASGI server to run FastAPI apps.

    Ngrok: Tunnels your local FastAPI server to the internet, so Meta can send webhook requests.

    Pydantic: For input validation (optional in this project).
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

🚀 API Documentation for WhatsApp Messaging Project
✅ 1. Send a WhatsApp Message

Send a test message to a verified phone number using the WhatsApp Cloud API.

    Method: POST
    URL: http://127.0.0.1:8000/send_message

Query Parameters:

    phone_number (required): Phone number in E.164 format (e.g., +917034654496)

    ⚠️ If you're testing in a browser or curl, encode the + as %2B
    Example: +917034654496 → %2B917034654496

Example Request (Postman):

    POST http://127.0.0.1:8000/send_message?phone_number=+917034654496
    Response (Success):
    {
      "status": "success",
      "message_id": "wamid.HBgLMjQ5..."
    }

🔁 2. Webhook Verification (For Receiving Messages)

This endpoint is used by Meta to verify your webhook URL when you register it.

Method: GET
URL: http://<your-ngrok-url>/webhook

Query Parameters (sent by Meta):

    hub.mode
    hub.challenge
    hub.verify_token (you set this)

Example URL received from Meta:

    GET /webhook?hub.mode=subscribe&hub.challenge=1234567890&hub.verify_token=your_token

What it does:
Returns the hub.challenge if the token is valid.
📩 3. Receive Incoming WhatsApp Messages

This endpoint is triggered when someone replies to your WhatsApp message.

    Method: POST
    URL: http://<your-ngrok-url>/webhook
    Request Body (example from Meta):

    {
          "entry": [
            {
              "changes": [
                {
                  "value": {
                    "messages": [
                      {
                        "from": "whatsapp_number",
                        "text": {
                        "body": "Hello!"
                      }
                      }
                    ]
                }
            }
        ]
    }
    ]
    }

What it does:

    Logs the sender's number and message text in your terminal.

    Returns a confirmation JSON like:

    {
          "status": "received"
    }

🧪 Testing Tips

    Use ngrok http 8000 to expose your local server.

    Register your webhook callback URL in Meta Developer Portal.

    In Meta dashboard, set:

        Callback URL: https://your-ngrok-url/webhook

        Verify Token: Same one in your FastAPI GET /webhook

