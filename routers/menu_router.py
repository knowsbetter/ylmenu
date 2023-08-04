from fastapi import APIRouter, HTTPException, Depends

from services.menu_service import MenuService

from routers import menu_router

from schemes import schemes
from repository.database import engine

menu_router = APIRouter()

@menu_router.post(
    path="/api/v1/menus/",
    response_model=schemes.Menu,
    summary="Создать меню",
    status_code=201,
    tags=["Меню"],
)
async def create_menu(menu: schemes.MenuBase, menu_service: MenuService = Depends(MenuService)):
    """Create menu item"""
    res = await menu_service.create_menu(menu)
    if not res:
        raise HTTPException(status_code=400, detail="menu already exists")
    return res


@menu_router.patch(
    path="/api/v1/menus/{menu_id}",
    summary="Обновить меню",
    response_model=schemes.Menu,
    tags=["Меню"],
)
async def update_menu(menu_id: str, menu: schemes.MenuUpdate, menu_service: MenuService = Depends(MenuService)):
    """Update menu item"""
    res = await menu_service.update_menu(menu_id, menu)
    if not res:
        raise HTTPException(status_code=404, detail="menu not found")
    return res


@menu_router.get(
    path="/api/v1/menus/",
    summary="Просмотреть список меню",
    response_model=list[schemes.Menu],
    tags=["Меню"],
)
async def read_menus(menu_service: MenuService = Depends(MenuService)):
    """Read menus list"""
    return await menu_service.read_menus()


@menu_router.get(
    path="/api/v1/menus/{menu_id}",
    summary="Просмотреть конкретное меню",
    response_model=schemes.Menu,
    tags=["Меню"],
)
async def read_menu(menu_id: str, menu_service: MenuService = Depends(MenuService)):
    """Read menu item"""
    res = await menu_service.read_menu(menu_id)
    if not res:
        raise HTTPException(status_code=404, detail="menu not found")
    return res


@menu_router.delete(
    path="/api/v1/menus/{menu_id}",
    summary="Удалить меню",
    response_model=schemes.MenuDelete,
    status_code=200,
    tags=["Меню"],
)
async def delete_menu(menu_id: str, menu_service: MenuService = Depends(MenuService)):
    """Delete menu item"""
    res = await menu_service.delete_menu(menu_id)
    if not res:
        raise HTTPException(status_code=404, detail="menu not found")
    return res

