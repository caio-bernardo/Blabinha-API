from fastapi.applications import FastAPI
import uvicorn
import blabinha_api.chats.routes as chats_routes
from blabinha_api.database import DatabaseConfig
import blabinha_api.dialogs.routes as dialogs_routes

app_runner = FastAPI(title="Blabinha API")

app_runner.include_router(chats_routes.router)
app_runner.include_router(dialogs_routes.router)

if __name__ == '__main__':
    db = DatabaseConfig()
    db.create_tables()
    uvicorn.run(app_runner)
