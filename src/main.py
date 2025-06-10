import sys
from fastapi.applications import FastAPI
import uvicorn
from blabinha_api import database
import blabinha_api.routes as core_routes
import blabinha_api.config as config
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

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("No args detected.")
    else:
        match args[1]:
            case "runserver":
                uvicorn.run(app_runner, host=config.HOST, port=config.PORT)
            case "migrate":
                dbconfig = database.DatabaseConfig()
                dbconfig.migrate()
            case _:
                print("Command not supported")
                sys.exit(1)
