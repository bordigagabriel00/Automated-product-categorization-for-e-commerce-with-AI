from fastapi import APIRouter
from config import settings

product_router = APIRouter(tags=['api'], prefix=settings.base_url + "product")


@product_router.get("")
async def get_all_products():
    return {"message": "products lists"}


@product_router.post("")
async def create_product():
    return {"message": "product create"}


@product_router.get("/{product_id}")
async def get_product_by_id():
    return {"message": "get product by id"}


@product_router.put("/{product_id}")
async def update_product():
    return {"message": "update product by id"}


@product_router.delete("/{product_id}")
async def delete_product():
    return {"message": "update product by id"}
