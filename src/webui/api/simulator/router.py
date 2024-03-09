from fastapi import APIRouter

import config
import main

health_router = APIRouter()


@health_router.get(config.settings.base_url + "predict", tags=['api'])
async def get_health():
    main.app.state
    return {"message": "UP"}
