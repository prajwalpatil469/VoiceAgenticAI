from fastapi import FastAPI
from app.routes.tts_route import router as tts_router
from app.routes.stt_route import router as stt_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Voice Assistant POC")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # or ["http://10.134.66.2:5500"] if hosting HTML on local server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(tts_router, prefix="/api")
app.include_router(stt_router, prefix="/api")  


