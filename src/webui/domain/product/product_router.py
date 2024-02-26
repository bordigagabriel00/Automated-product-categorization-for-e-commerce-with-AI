from fastapi import APIRouter
from config import settings

product_router = APIRouter()


@product_router.get(settings.base_url + "product", tags=['admin', '"products'])
async def get_all_products():
    return {"message": "Lista de productos"}
