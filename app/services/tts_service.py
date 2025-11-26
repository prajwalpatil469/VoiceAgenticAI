# app/services/tts_service.py
import wave
import io
from app.tools.tts_tool import generate_speech
from app.config.settings import settings

async def synthesize_audio(text: str) -> bytes:
    pcm_or_wav = await generate_speech(text)

    if settings.USE_GCP:
        # Wrap PCM as WAV container
        rate = 24000
        out = io.BytesIO()
        wf = wave.open(out, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(pcm_or_wav)
        wf.close()
        return out.getvalue()
    else:
        return pcm_or_wav
