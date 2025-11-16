import os
import uvicorn
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import openai

# ----------------------------
# Configuration
# ----------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Set in Render
openai.api_key = OPENAI_API_KEY

PORT = int(os.getenv("PORT", 10000))

# ----------------------------
# Memory Storage (in-memory for testing)
# ----------------------------
MEMORY_DB = {}

def store_memory(user_id: str, text: str):
    if user_id not in MEMORY_DB:
        MEMORY_DB[user_id] = []
    MEMORY_DB[user_id].append(text)

def get_memory(user_id: str, last_n: int = 5):
    return MEMORY_DB.get(user_id, [])[-last_n:]

# ----------------------------
# FastAPI App & CORS
# ----------------------------
app = FastAPI(title="Simple GPT Chat Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Chat Endpoint
# ----------------------------
@app.post("/chat")
async def chat_endpoint(user_id: str = Form(...), message: str = Form(...)):
    # Store user message
    store_memory(user_id, f"User: {message}")

    # Prepare conversation history
    history = get_memory(user_id)
    conversation = "\n".join(history) + "\nAI:"

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": conversation}
            ],
            temperature=0.7,
            max_tokens=300
        )
        ai_reply = response.choices[0].message.content.strip()
    except Exception as e:
        ai_reply = f"Error: {str(e)}"

    # Store AI reply
    store_memory(user_id, f"AI: {ai_reply}")

    return JSONResponse({"reply": ai_reply})

# ----------------------------
# Basic Homepage
# ----------------------------
@app.get("/")
async def index():
    return {
        "message": "GPT Chat Server Running",
        "endpoints": ["/chat"]
    }

# ----------------------------
# Run Server
# ----------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
