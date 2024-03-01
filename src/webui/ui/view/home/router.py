from fastapi import APIRouter
from fastapi.responses import RedirectResponse

home_router = APIRouter(tags=['views'])


@home_router.get("/")
async def get_index():
    return RedirectResponse(url="/simulator")
