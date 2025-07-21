from fastapi.applications import FastAPI
import core.routes as core_routes
from fastapi.middleware.cors import CORSMiddleware

app_runner = FastAPI(title="Blabinha API")

app_runner.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_runner.include_router(core_routes.router)
