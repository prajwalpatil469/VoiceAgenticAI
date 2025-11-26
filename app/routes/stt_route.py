# app/routes/stt_route.py
from fastapi import APIRouter, UploadFile, HTTPException
from app.services.stt_service import process_stt_audio

router = APIRouter()

@router.post("/stt")
async def stt(audio_file: UploadFile):
    try:
        # Process the uploaded audio file and get the transcribed text
        transcribed_text = await process_stt_audio(audio_file)
        return {"transcribed_text": transcribed_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
