# main.py
import os
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from twilio.twiml.messaging_response import MessagingResponse
from openrouter import OpenRouter

# =====================================================
# Config
# =====================================================
OR_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Set in Render
client = OpenRouter(api_key=OR_API_KEY)

PORT = int(os.getenv("PORT", 8000))

# =====================================================
# FastAPI Setup
# =====================================================
app = FastAPI(title="WhatsApp AI Server")

# -----------------------------
# CORS Middleware
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# OpenRouter GPT Logic
# =====================================================
def generate_reply(user_id: str, message: str):
    """
    Simple function to generate a reply using OpenRouter GPT-3.5-turbo.
    """
    conversation = f"User ({user_id}): {message}"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": conversation}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# =====================================================
# WhatsApp Webhook
# =====================================================
@app.post("/whatsapp")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...)
):
    """
    Receives WhatsApp messages from Twilio sandbox.
    Body = message text
    From = WhatsApp number
    """
    reply_text = generate_reply(From, Body)
    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)

# =====================================================
# Simple Test Endpoint
# =====================================================
@app.get("/")
async def index():
    return {"message": "WhatsApp AI Server Running"}

# =====================================================
# Run Server
# =====================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
