from fastapi import APIRouter, Response
from app.schemas.tts_schema import TTSRequest
from app.services.tts_service import synthesize_audio

router = APIRouter()

@router.post("/tts")
async def tts(req: TTSRequest):
    audio_bytes = await synthesize_audio(req.text)
    return Response(content=audio_bytes, media_type="audio/wav")
