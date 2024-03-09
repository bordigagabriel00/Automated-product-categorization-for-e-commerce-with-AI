from fastapi import APIRouter

from config import settings

category_router = APIRouter(tags=['api'], prefix=f"{settings.base_url}/category")


@category_router.get("")
async def get_all_categories():
    return {"message": "category list"}


@category_router.post("")
async def create_category():
    return {"message": "category create"}


@category_router.get("/{category_id}")
async def get_category_by_id():
    return {"message": "get category by id"}


@category_router.put("/{category_id}")
async def update_category():
    return {"message": "update category by id"}


@category_router.delete("/{category_id}")
async def delete_category():
    return {"message": "update category by id"}
