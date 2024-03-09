from fastapi import APIRouter
from core.eventbus import nats_provider as nats
from api.monitor.consumer import topic_health

health_router = APIRouter()


@health_router.get("/health", tags=['api'])
async def get_health():

    await nats.publish(topic_health, " Send Message from api health")
    return {"message": "UP"}
