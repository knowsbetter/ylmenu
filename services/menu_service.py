from fastapi import BackgroundTasks, Depends
from fastapi.encoders import jsonable_encoder

from cache import redis_cache as cache
from repository.menu_crud import MenuCRUD
from schemes import schemes


class MenuService:
    def __init__(self, menu_crud: MenuCRUD = Depends(MenuCRUD)):
        self.menu_crud = menu_crud

    async def create_menu(self, menu: schemes.MenuBase):
        db_menu = await self.menu_crud.get_menu_by_title(menu_title=menu.title)
        if db_menu:
            return None
        return await self.menu_crud.create_menu(menu=menu)

    async def update_menu(self, menu_id: str, menu: schemes.MenuUpdate):
        db_menu = await self.menu_crud.get_menu_by_id(menu_id=menu_id)
        if db_menu:
            db_menu.title = menu.title
            db_menu.description = menu.description
            await cache.set_cache(f'/api/v1/menus/{menu_id}', jsonable_encoder(db_menu))
            return await self.menu_crud.update_menu(menu_id=menu_id)
        else:
            return None

    async def read_menus(self):
        menus = await self.menu_crud.get_menus()
        if menus:
            for menu in menus:
                await cache.set_cache(f'/api/v1/menus/{menu.id}', jsonable_encoder(menu))
        return menus

    async def read_menu(self, menu_id: str):
        cached = await cache.get_cache(f'/api/v1/menus/{menu_id}')
        if cached:
            db_menu = cached
        else:
            db_menu = await self.menu_crud.get_menu_by_id(menu_id=menu_id)
        if db_menu is None:
            return None
        await cache.set_cache(f'/api/v1/menus/{menu_id}', jsonable_encoder(db_menu))
        return db_menu

    async def delete_menu(self, menu_id: str, background_tasks: BackgroundTasks):
        db_menu = await self.menu_crud.delete_menu(menu_id=menu_id)
        if db_menu is None:
            return None
        background_tasks.add_task(cache.delete_cache, f'/api/v1/menus/{menu_id}')
        return {'status': True, 'message': 'The menu has been deleted'}
