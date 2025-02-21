from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import PlainTextResponse
from uuid import uuid4
import os
import whisper

app = FastAPI()
model = whisper.load_model("large")

def transcribe_audio(model, audio_path: str) -> str:

    try:
        result = model.transcribe(
            audio_path, 
            language=os.getenv('WHISPER_LANGUAGE', 'en')
        )
        return result["text"]
    except Exception as e:
        raise Exception(f"Transcription error: {e}")

@app.post("/transcribe", response_class=PlainTextResponse)
async def transcribe(file: UploadFile = File(...)) -> str:

    if not file or not file.filename:
        raise HTTPException(
            status_code=400, 
            detail="No file received or invalid file upload."
        )

    print(f"Received file: {file.filename}, Content-Type: {file.content_type}")
    
    audio_path = f"/tmp/{uuid4()}_{file.filename}"
    try:
        with open(audio_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return transcribe_audio(model, audio_path)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy"}