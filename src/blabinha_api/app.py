"""
Ponto de entrada da API

Rotas são declaradas aqui
"""
from fastapi.applications import FastAPI
from blabinha_api.apps.core import routes as core_routes
from fastapi.middleware.cors import CORSMiddleware
from blabinha_api.config import settings

app_runner = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API para o chatbot Blabinha"
)

app_runner.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_runner.include_router(core_routes.router)
