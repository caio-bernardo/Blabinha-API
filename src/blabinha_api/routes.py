from fastapi import status
from fastapi.routing import APIRouter


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def checkhealth():
    return {"detail": "API is on air."}
