from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/health", tags=['api'])
async def get_health():
    return {"message": "UP"}
