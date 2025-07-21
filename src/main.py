import sys
import uvicorn
from blabinha_api import database

from blabinha_api.app import app_runner

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("No args detected.")
    else:
        match args[1]:
            case "runserver":
                uvicorn.run(app_runner, host="0.0.0.0", port=8000)
            case "migrate":
                dbconfig = database.DatabaseConfig()
                dbconfig.migrate()
            case _:
                print("Command not supported")
                sys.exit(1)
