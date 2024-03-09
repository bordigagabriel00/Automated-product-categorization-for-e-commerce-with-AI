from fastapi import APIRouter

from api.monitor.consumer import topic_health
from core.eventbus import nats_provider as nats

health_router = APIRouter()


@health_router.get("/health", tags=['api'])
async def get_health():
    await nats.publish(topic_health, " Send Message from api health")
    return {"message": "UP"}
