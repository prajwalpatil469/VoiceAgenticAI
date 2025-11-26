from app.tools.stt_tool import stt_google

async def process_stt_audio(audio_file: bytes) -> str:
    """
    Process the uploaded audio file and return the transcribed text
    by sending it to Gemini Live API for speech-to-text conversion.
    """
    # Call the helper function to process the audio
    transcribed_text = await stt_google(audio_file)
    return transcribed_text
