from fastapi import status
from fastapi.routing import APIRouter
import blabinha_api.chats.routes as chats_routes
import blabinha_api.dialogs.routes as dialogs_routes

router = APIRouter()

router.include_router(chats_routes.router)
router.include_router(dialogs_routes.router)

@router.get("/", status_code=status.HTTP_200_OK)
async def checkhealth():
    return {"detail": "API is on air."}
