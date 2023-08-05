from fastapi import Depends

from schemes import schemes
from repository.submenu_crud import SubmenuCRUD


class SubmenuService:
    def __init__(self, submenu_crud: SubmenuCRUD = Depends(SubmenuCRUD)):
        self.submenu_crud = submenu_crud

    async def create_submenu(self, menu_id: str, submenu: schemes.SubmenuBase):
        db_submenu = await self.submenu_crud.get_submenu_by_title(submenu_title=submenu.title)
        if db_submenu:
            return None
        return await self.submenu_crud.create_submenu(submenu=submenu, menu_id=menu_id)

    async def update_submenu(self, menu_id: str, submenu_id: str, submenu: schemes.SubmenuUpdate):
        db_submenu = await self.submenu_crud.get_submenu_by_id(submenu_id=submenu_id)
        if db_submenu:
            db_submenu.title = submenu.title
            db_submenu.description = submenu.description
            return await self.submenu_crud.update_submenu(submenu_id=submenu_id)
        else:
            return None

    async def read_submenus(self, menu_id: str):
        submenus = await self.submenu_crud.get_submenus(menu_id=menu_id)
        return submenus

    async def read_submenu(self, menu_id: str, submenu_id: str):
        db_submenu = await self.submenu_crud.get_submenu_by_id(submenu_id=submenu_id)
        if db_submenu is None:
            return None
        return db_submenu

    async def delete_submenu(self, menu_id: str, submenu_id: str):
        db_submenu = await self.submenu_crud.delete_submenu(menu_id=menu_id, submenu_id=submenu_id)
        if db_submenu is None:
            return None
        return {"status": True, "message": "The submenu has been deleted"}
