from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64

app = FastAPI()

class VoiceRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64: str
    message: str

@app.get("/")
def home():
    return {"status": "API is online"}

@app.post("/detect")
async def detect_voice(data: VoiceRequest, x_api_key: str = Header(None)):
    # Verify the API key you will use in the tester
    if x_api_key != "my_secret_key_123":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Decode the audio (this is where you'd send 'audio_bytes' to your ML model)
    try:
        audio_bytes = base64.b64decode(data.audio_base64)
    except:
        raise HTTPException(status_code=400, detail="Invalid Base64")

    # Sample response for the tester
    return {
        "is_ai_generated": False,
        "confidence": 0.99,
        "processed_message": data.message
    }