from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Query
from fastapi.responses import PlainTextResponse
from uuid import uuid4
import os
import whisper

app = FastAPI()
MODEL_SIZE = os.getenv('WHISPER_MODEL', 'large')
print(f"Loading Whisper model: {MODEL_SIZE}")
model = whisper.load_model(MODEL_SIZE)

def transcribe_audio(model, audio_path: str, language: str = None) -> str:
    try:
        # Use provided language or fall back to default English
        lang = language or 'en'
        result = model.transcribe(
            audio_path, 
            language=lang
        )
        return result["text"]
    except Exception as e:
        raise Exception(f"Transcription error: {e}")

@app.post("/transcribe", response_class=PlainTextResponse)
async def transcribe(
    file: UploadFile = File(...),
    language: str = Query(None)  # Änderung: Form -> Query
) -> str:
    if not file or not file.filename:
        raise HTTPException(
            status_code=400, 
            detail="No file received or invalid file upload."
        )

    print(f"Received file: {file.filename}, Content-Type: {file.content_type}, Language: {language}")
    
    audio_path = f"/tmp/{uuid4()}_{file.filename}"
    try:
        with open(audio_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return transcribe_audio(model, audio_path, language)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy"}