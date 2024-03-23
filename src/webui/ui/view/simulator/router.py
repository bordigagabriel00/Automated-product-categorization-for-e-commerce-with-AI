from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse

from config import templates

router = APIRouter(tags=['views'])


@router.get("/simulator", response_class=HTMLResponse)
async def get_simulator_view(request: Request):
    return templates.TemplateResponse("pages/simulator.html", {"request": request})


@router.get("/bert-ft", response_class=HTMLResponse)
async def get_bert_ft_view(request: Request):
    return templates.TemplateResponse("pages/bert-ft.html", {"request": request})
