from fastapi import BackgroundTasks, Depends
from fastapi.encoders import jsonable_encoder

from cache import redis_cache as cache
from repository.submenu_crud import SubmenuCRUD
from schemes import schemes


class SubmenuService:
    def __init__(self, submenu_crud: SubmenuCRUD = Depends(SubmenuCRUD)):
        self.submenu_crud = submenu_crud

    async def create_submenu(self, menu_id: str, submenu: schemes.SubmenuBase):
        db_submenu = await self.submenu_crud.get_submenu_by_title(submenu_title=submenu.title)
        if db_submenu:
            return None
        await cache.delete_cache(f'/api/v1/menus/{menu_id}')
        return await self.submenu_crud.create_submenu(submenu=submenu, menu_id=menu_id)

    async def update_submenu(self, menu_id: str, submenu_id: str, submenu: schemes.SubmenuUpdate):
        db_submenu = await self.submenu_crud.get_submenu_by_id(submenu_id=submenu_id)
        if db_submenu:
            db_submenu.title = submenu.title
            db_submenu.description = submenu.description
            await cache.set_cache(
                f'/api/v1/menus/{menu_id}/submenus/{submenu_id}',
                jsonable_encoder(db_submenu),
            )
            return await self.submenu_crud.update_submenu(submenu_id=submenu_id)
        else:
            return None

    async def read_submenus(self, menu_id: str):
        submenus = await self.submenu_crud.get_submenus(menu_id=menu_id)
        if submenus:
            for submenu in submenus:
                await cache.set_cache(
                    f'/api/v1/menus/{menu_id}/submenus/{submenu.id}',
                    jsonable_encoder(submenu),
                )
        return submenus

    async def read_submenu(self, menu_id: str, submenu_id: str):
        cached = await cache.get_cache(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
        if cached:
            db_submenu = cached
        else:
            db_submenu = await self.submenu_crud.get_submenu_by_id(submenu_id=submenu_id)
        if db_submenu is None:
            return None
        await cache.set_cache(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}',
            jsonable_encoder(db_submenu),
        )
        return db_submenu

    async def delete_submenu(self, menu_id: str, submenu_id: str, background_tasks: BackgroundTasks):
        db_submenu = await self.submenu_crud.delete_submenu(menu_id=menu_id, submenu_id=submenu_id)
        if db_submenu is None:
            return None
        background_tasks.add_task(cache.delete_cache, f'/api/v1/menus/{menu_id}')
        return {'status': True, 'message': 'The submenu has been deleted'}
