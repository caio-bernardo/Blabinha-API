from fastapi import status
from fastapi.routing import APIRouter
from blabinha_api.chats import routes as chats_routes
from blabinha_api.dialogs import routes as dialogs_routes
from blabinha_api.accounts import routes as accounts_routes

router = APIRouter()

router.include_router(chats_routes.router)
router.include_router(dialogs_routes.router)
router.include_router(accounts_routes.router)

@router.get("/", status_code=status.HTTP_200_OK)
async def checkhealth():
    return {"detail": "API is on air."}
