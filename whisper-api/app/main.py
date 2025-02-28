from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import PlainTextResponse
from uuid import uuid4
import os
import whisper
import gc

app = FastAPI()

# Don't load the model at startup
model = None
current_model_name = None

def load_model(model_name: str):
    global model, current_model_name
    
    # If the requested model is already loaded, don't reload it
    if current_model_name == model_name and model is not None:
        return model
    
    # If a different model is loaded, unload it first
    if model is not None:
        print(f"Unloading current model: {current_model_name}")
        del model
        gc.collect()  # Force garbage collection
    
    # Load the requested model
    print(f"Loading Whisper model: {model_name}")
    model = whisper.load_model(model_name)
    current_model_name = model_name
    return model

def transcribe_audio(audio_path: str, model_name: str, language: str = None) -> str:
    try:
        # Load the model (or use already loaded one)
        current_model = load_model(model_name)
        
        # Use provided language or fall back to default English
        lang = language or 'en'
        result = current_model.transcribe(
            audio_path, 
            language=lang
        )
        return result["text"]
    except Exception as e:
        raise Exception(f"Transcription error: {e}")

@app.post("/transcribe", response_class=PlainTextResponse)
async def transcribe(
    file: UploadFile = File(...),
    language: str = Query(None),
    model_name: str = Query("tiny")  # Default to tiny for faster processing
) -> str:
    if not file or not file.filename:
        raise HTTPException(
            status_code=400, 
            detail="No file received or invalid file upload."
        )

    print(f"Received file: {file.filename}, Content-Type: {file.content_type}, Language: {language}, Model: {model_name}")
    
    audio_path = f"/tmp/{uuid4()}_{file.filename}"
    try:
        with open(audio_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return transcribe_audio(audio_path, model_name, language)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

@app.get("/model-info")
async def model_info() -> dict:
    return {
        "current_model": current_model_name,
        "is_loaded": model is not None,
        "available_models": ["tiny", "base", "small", "medium", "large"]
    }

@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy"}