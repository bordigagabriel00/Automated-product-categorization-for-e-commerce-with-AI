from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from  config import templates

router = APIRouter(tags=['views'])


@router.get("/simulator", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("pages/simulator.html", {"request": request})
