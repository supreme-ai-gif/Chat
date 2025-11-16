# main.py
import os
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import openai

# -----------------------------
# OpenAI API Key
# -----------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure to set this in Render

# -----------------------------
# FastAPI Setup
# -----------------------------
app = FastAPI(title="Simple GPT Chat Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Chat Endpoint
# -----------------------------
@app.post("/chat")
async def chat_endpoint(user_id: str = Form(...), message: str = Form(...)):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=300
        )
        ai_reply = response.choices[0].message['content'].strip()
        return JSONResponse({"reply": ai_reply})
    except Exception as e:
        return JSONResponse({"reply": f"Error: {str(e)}"})

# -----------------------------
# Basic Homepage
# -----------------------------
@app.get("/")
async def index():
    return {
        "message": "GPT chat server running",
        "endpoints": ["/chat"]
    }

# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
