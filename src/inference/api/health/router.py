from fastapi import APIRouter

from core.eventbus import topic_health, nats_provider as nats

health_router = APIRouter()


@health_router.get("/health", tags=['api'])
async def get_health():
    await nats.publish(topic_health, " Send Message from api health")
    return {"message": "UP"}
