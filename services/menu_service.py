from fastapi import Depends

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
            return await self.menu_crud.update_menu(menu_id=menu_id)
        else:
            return None

    async def read_menus(self):
        menus = await self.menu_crud.get_menus()
        return menus

    async def read_menu(self, menu_id: str):
        db_menu = await self.menu_crud.get_menu_by_id(menu_id=menu_id)
        if db_menu is None:
            return None
        return db_menu

    async def delete_menu(self, menu_id: str):
        db_menu = await self.menu_crud.delete_menu(menu_id=menu_id)
        if db_menu is None:
            return None
        return {'status': True, 'message': 'The menu has been deleted'}
