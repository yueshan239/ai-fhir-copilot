from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from api.copilot import router as copilot_router
from api.settings import router as settings_router

app = FastAPI(
    title="AI FHIR Integration Copilot",
)

app.include_router(copilot_router)
app.include_router(settings_router)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


@app.get("/")
def root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))
