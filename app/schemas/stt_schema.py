from pydantic import BaseModel
from fastapi import UploadFile, File
from fastapi import UploadFile

class STTRequest(BaseModel):
    audio_file: UploadFile  

