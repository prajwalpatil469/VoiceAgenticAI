import base64
from app.config.settings import settings
from google import genai
from google.genai.types import (
    LiveConnectConfig,
    SpeechConfig,
    VoiceConfig,
    PrebuiltVoiceConfig,
)

async def tts_google(text: str) -> bytes:
    """
    Real Text-to-Speech using the Gemini Live API.
    """
    # Initialize Vertex AI Live API client
    client = genai.Client(
        vertexai=True,
        project=settings.PROJECT_ID,
        location=settings.LOCATION,
    )

    # Set up the TTS configuration
    config = LiveConnectConfig(
        response_modalities=["AUDIO"],
        speech_config=SpeechConfig(
            voice_config=VoiceConfig(
                prebuilt_voice_config=PrebuiltVoiceConfig(
                    voice_name=settings.TTS_VOICE
                )
            )
        ),
    )

    audio_chunks: list[bytes] = []

    # Start real-time voice generation session
    async with client.aio.live.connect(
        model=settings.GEMINI_MODEL,
        config=config
    ) as session:
        # Send text for TTS using input keyword argument
        await session.send(input=text, end_of_turn=True)

        # Receive server response containing audio data
        async for response in session.receive():
            # The audio data comes directly in response.data
            if response.data is not None:
                audio_chunks.append(response.data)
            
            # Check if turn is complete
            if (hasattr(response, 'server_content') and 
                response.server_content and 
                hasattr(response.server_content, 'turn_complete') and 
                response.server_content.turn_complete):
                break

    # Concatenate and return audio chunks
    if not audio_chunks:
        raise ValueError("No audio data received from Gemini Live API")
    
    return b"".join(audio_chunks)


async def generate_speech(text: str) -> bytes:
    """
    Public wrapper for TTS function.
    Uses the real Gemini Live API for TTS.
    """
    return await tts_google(text)