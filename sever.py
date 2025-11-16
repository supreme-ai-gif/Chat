# server.py
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="Test AI Server")

# -----------------------------
# Enable CORS for all origins
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Simple in-memory memory
# -----------------------------
CHAT_MEMORY = {}

def store_memory(user_id: str, message: str):
    if user_id not in CHAT_MEMORY:
        CHAT_MEMORY[user_id] = []
    CHAT_MEMORY[user_id].append(message)

def get_memory(user_id: str):
    return CHAT_MEMORY.get(user_id, [])

# -----------------------------
# Chat logic
# -----------------------------
def process_chat(user_id: str, message: str):
    # Store user message
    store_memory(user_id, f"User: {message}")

    # For testing, just echo the message with AI prefix
    ai_reply = f"AI: Echoing '{message}' for {user_id}"

    # Store AI reply
    store_memory(user_id, ai_reply)
    return ai_reply

# -----------------------------
# Chat endpoint
# -----------------------------
@app.post("/chat")
async def chat_endpoint(user_id: str = Form(...), message: str = Form(...)):
    reply = process_chat(user_id, message)
    return JSONResponse(content={"reply": reply})

# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
