from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import requests # You will need to pip install requests

app = FastAPI()

class VoiceRequest(BaseModel):
    # The tester sends 'audio_url' and 'message'
    audio_url: str 
    message: str

@app.get("/")
def home():
    return {"status": "API is online"}

@app.post("/detect")
async def detect_voice(data: VoiceRequest, authorization: str = Header(None)):
    # 1. Verify API Key (Matches the 'Authorization' header in the tester)
    if authorization != "my_secret_key_123":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 2. Download the audio file from the provided GitHub URL
    try:
        response = requests.get(data.audio_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Could not download audio from URL")
        
        audio_bytes = response.content # This is what you pass to your ML model
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Download failed: {str(e)}")

    # 3. Sample response (Matches what the tester expects)
    return {
        "is_ai_generated": False,
        "confidence": 0.99,
        "processed_message": data.message
    }