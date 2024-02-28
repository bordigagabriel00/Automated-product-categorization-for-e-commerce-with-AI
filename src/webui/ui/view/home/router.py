from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import pathlib

# Define la ubicación base para este router
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "ui" / "templates")

home_router = APIRouter(tags=['views'])



@home_router.get("/")
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
