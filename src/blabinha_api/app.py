from fastapi.applications import FastAPI
from blabinha_api.core import routes as core_routes
from fastapi.middleware.cors import CORSMiddleware
from blabinha_api.config import config

app_runner = FastAPI(title=config.app_name)

app_runner.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_runner.include_router(core_routes.router)
