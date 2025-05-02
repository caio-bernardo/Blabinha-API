from fastapi import FastAPI, status
from src.app.routes import chats, dialogs
from src.app.database import DatabaseConfig
from src.app.dependencies import dbconfig
from src.app.models import *

app_runner = FastAPI()


@app_runner.on_event("startup")
def startup():
    dbconfig.create_tables()


app_runner.include_router(chats.router)
app_runner.include_router(dialogs.router)


@app_runner.get("/health", summary="Check API health", description="Check if API is on-line")
async def health():
    return {"message": "Blabinha api is online"}
