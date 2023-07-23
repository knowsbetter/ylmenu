from fastapi import APIRouter, HTTPException, Depends

from services.menu_service import MenuService
from services.menu_service import get_menu_service

from routers import menu_router, submenu_router, dish_router

from mainapp import models, schemes
from mainapp.database import engine

menu_router = APIRouter()

@menu_router.post(
    path="/api/v1/menus/",
    response_model=schemes.Menu,
    summary="Создать меню",
    status_code=201,
    tags=["Меню"],
)
async def create_menu(menu: schemes.MenuBase, menu_service: MenuService = Depends(get_menu_service)):
    """Create menu item"""
    res = await menu_service.create_menu(menu)
    if not res:
        raise HTTPException(status_code=400, detail="menu already exists")
    res.id = str(res.id)
    return res


@menu_router.patch(
    path="/api/v1/menus/{menu_id}",
    summary="Обновить меню",
    response_model=schemes.Menu,
    tags=["Меню"],
)
async def update_menu(menu_id: int, menu: schemes.MenuUpdate, menu_service: MenuService = Depends(get_menu_service)):
    """Update menu item"""
    res = await menu_service.update_menu(menu_id, menu)
    if not res:
        raise HTTPException(status_code=404, detail="menu not found")
    res.id = str(res.id)
    return res


@menu_router.get(
    path="/api/v1/menus/",
    summary="Просмотреть список меню",
    #response_model=list[schemes.Menu],
    tags=["Меню"],
)
async def read_menus(menu_service: MenuService = Depends(get_menu_service)):
    """Read menus list"""
    return await menu_service.read_menus()


@menu_router.get(
    path="/api/v1/menus/{menu_id}",
    summary="Просмотреть конкретное меню",
    response_model=schemes.Menu,
    tags=["Меню"],
)
async def read_menu(menu_id: int, menu_service: MenuService = Depends(get_menu_service)):
    """Read menu item"""
    res = await menu_service.read_menu(menu_id)
    if not res:
        raise HTTPException(status_code=404, detail="menu not found")
    res.id = str(res.id)
    return res


@menu_router.delete(
    path="/api/v1/menus/{menu_id}",
    summary="Удалить меню",
    #response_model=schemes.MenuDelete,
    status_code=200,
    tags=["Меню"],
)
async def delete_menu(menu_id: int, menu_service: MenuService = Depends(get_menu_service)):
    """Delete menu item"""
    res = await menu_service.delete_menu(menu_id)
    if not res:
        raise HTTPException(status_code=404, detail="menu not found")
    return res
