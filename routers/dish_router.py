from fastapi import APIRouter, HTTPException, Depends

from services.dish_service import DishService
from services.dish_service import get_dish_service

from routers import dish_router

from schemes import schemes
from repository.database import engine

dish_router = APIRouter()

@dish_router.post(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    summary="Создать блюдо",
    response_model=schemes.Dish,
    status_code=201,
    tags=["Блюда"],
)
async def create_dish(
    menu_id: str,
    submenu_id: str,
    dish: schemes.DishBase,
    dish_service: DishService = Depends(get_dish_service),
):
    """Create dish item"""
    res = await dish_service.create_dish(menu_id, submenu_id, dish)
    if not res:
        raise HTTPException(status_code=400, detail="dish already exists")
    return res


@dish_router.patch(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    summary="Обновить блюдо",
    response_model=schemes.Dish,
    tags=["Блюда"],
)
async def update_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    dish: schemes.DishUpdate,
    dish_service: DishService = Depends(get_dish_service),
):
    """Update dish item"""
    res = await dish_service.update_dish(menu_id, submenu_id, dish_id, dish)
    if not res:
        raise HTTPException(status_code=404, detail="dish not found")
    return res


@dish_router.get(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    summary="Просмотреть список блюд",
    response_model=list[schemes.Dish],
    tags=["Блюда"],
)
async def read_dishes(
    menu_id: str,
    submenu_id: str,
    dish_service: DishService = Depends(get_dish_service),
):
    """Read dishes list"""
    return await dish_service.read_dishes(menu_id, submenu_id)


@dish_router.get(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    summary="Просмотреть конкретное блюдо",
    response_model=schemes.Dish,
    tags=["Блюда"],
)
async def read_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    dish_service: DishService = Depends(get_dish_service),
):
    """Read dish item"""
    res = await dish_service.read_dish(menu_id, submenu_id, dish_id)
    if not res:
        raise HTTPException(status_code=404, detail="dish not found")
    return res


@dish_router.delete(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    summary="Удалить блюдо",
    response_model=schemes.DishDelete,
    status_code=200,
    tags=["Блюда"],
)
async def delete_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    dish_service: DishService = Depends(get_dish_service),
):
    """Delete dish item"""
    res = await dish_service.delete_dish(menu_id, submenu_id, dish_id)
    if not res:
        raise HTTPException(status_code=404, detail="dish not found")
    return res