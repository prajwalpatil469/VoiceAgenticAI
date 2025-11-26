import base64
from app.config.settings import settings
from google import genai
from google.genai.types import (
    LiveConnectConfig,
    SpeechConfig,
    VoiceConfig,
    PrebuiltVoiceConfig,
)

async def stt_google(audio_file: bytes) -> str:
    """
    Send audio to the Gemini Live API for speech-to-text conversion.
    """
    client = genai.Client(
        vertexai=True,
        project=settings.PROJECT_ID,
        location=settings.LOCATION,
    )

    # Set up the STT configuration
    config = LiveConnectConfig(
        response_modalities=["TEXT"],
        speech_config=SpeechConfig(
            voice_config=VoiceConfig(
                prebuilt_voice_config=PrebuiltVoiceConfig(
                    voice_name=settings.TTS_VOICE  # Use an appropriate voice model for STT if necessary
                )
            )
        ),
    )

    transcribed_text = ""

    # Start a real-time session with the Gemini API
    async with client.aio.live.connect(
        model=settings.GEMINI_MODEL,
        config=config
    ) as session:
        # Send audio to Gemini for STT processing
        await session.send(input=audio_file, end_of_turn=True)

        # Receive the server response containing transcribed text
        async for response in session.receive():
            if hasattr(response, 'server_content') and response.server_content:
                server_content = response.server_content
                if hasattr(server_content, 'model_turn') and server_content.model_turn:
                    model_turn = server_content.model_turn
                    if hasattr(model_turn, 'parts'):
                        for part in model_turn.parts:
                            if hasattr(part, 'inline_data') and part.inline_data:
                                transcribed_text = part.inline_data.data.decode('utf-8')

                # If turn is complete, exit loop
                if hasattr(server_content, 'turn_complete') and server_content.turn_complete:
                    break

    if not transcribed_text:
        raise ValueError("No transcribed text received from Gemini Live API")

    return transcribed_text
