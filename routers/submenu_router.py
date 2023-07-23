from fastapi import APIRouter, HTTPException, Depends

from services.submenu_service import SubmenuService
from services.submenu_service import get_submenu_service

from routers import menu_router, submenu_router, dish_router

from mainapp import models, schemes
from mainapp.database import engine

submenu_router = APIRouter()

@submenu_router.post(
    path="/api/v1/menus/{menu_id}/submenus",
    summary="Создать подменю",
    response_model=schemes.Submenu,
    status_code=201,
    tags=["Подменю"],
)
async def create_submenu(menu_id: int, submenu: schemes.SubmenuBase, submenu_service: SubmenuService = Depends(get_submenu_service)):
    """Create submenu item"""
    res = await submenu_service.create_submenu(menu_id, submenu)
    if not res:
        raise HTTPException(status_code=400, detail="submenu already exists")
    res.id = str(res.id)
    return res


@submenu_router.patch(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    summary="Обновить подменю",
    response_model=schemes.Submenu,
    tags=["Подменю"],
)
async def update_submenu(
    menu_id: int, submenu_id: int, submenu: schemes.SubmenuUpdate, submenu_service: SubmenuService = Depends(get_submenu_service)
):
    """Update submenu item"""
    res = await submenu_service.update_submenu(menu_id, submenu_id, submenu)
    if not res:
        raise HTTPException(status_code=404, detail="submenu not found")
    res.id = str(res.id)
    return res


@submenu_router.get(
    path="/api/v1/menus/{menu_id}/submenus",
    summary="Просмотреть список подменю",
    #response_model=list[schemes.Submenu],
    tags=["Подменю"],
)
async def read_submenus(menu_id: int, submenu_service: SubmenuService = Depends(get_submenu_service)):
    """Read submenus list"""
    return await submenu_service.read_submenus(menu_id)


@submenu_router.get(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    summary="Просмотреть конкретное подменю",
    response_model=schemes.Submenu,
    tags=["Подменю"],
)
async def read_submenu(menu_id: int, submenu_id: int, submenu_service: SubmenuService = Depends(get_submenu_service)):
    """Read submenu item"""
    res = await submenu_service.read_submenu(menu_id, submenu_id)
    if not res:
        raise HTTPException(status_code=404, detail="submenu not found")
    res.id = str(res.id)
    return res


@submenu_router.delete(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    summary="Удалить подменю",
    #response_model=schemes.SubmenuDelete,
    status_code=200,
    tags=["Подменю"],
)
async def delete_submenu(menu_id: int, submenu_id: int, submenu_service: SubmenuService = Depends(get_submenu_service)):
    """Delete submenu item"""
    res = await submenu_service.delete_submenu(menu_id, submenu_id)
    if not res:
        raise HTTPException(status_code=404, detail="submenu not found")
    return res