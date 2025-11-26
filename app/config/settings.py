from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_ID: str | None = None
    LOCATION: str = "us-central1"
    USE_GCP: bool = True

    GEMINI_MODEL: str = "gemini-live-2.5-flash-preview-native-audio-09-2025"
    TTS_VOICE: str = "Aoede"

    class Config:
        env_file = ".env"

settings = Settings()
