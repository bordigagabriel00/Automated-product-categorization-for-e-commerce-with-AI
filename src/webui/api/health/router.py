from fastapi import APIRouter
from config import settings

health_router = APIRouter()


@health_router.get("/health", tags=['api'])
async def get_health():
    return {"message": "UP"}
