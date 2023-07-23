from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from mainapp import crud, schemes
from mainapp.database import SessionLocal


async def get_db():
    """Returns database session"""
    async with SessionLocal() as db:
        yield db


class SubmenuService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_submenu(self, menu_id: int, submenu: schemes.SubmenuBase):
        db_submenu = await crud.SubmenuCRUD.get_submenu_by_title(submenu_title=submenu.title, db=self.session)
        if db_submenu:
            return None
        return await crud.SubmenuCRUD.create_submenu(db=self.session, submenu=submenu, menu_id=menu_id)

    async def update_submenu(self, menu_id: int, submenu_id: int, submenu: schemes.SubmenuUpdate):
        db_submenu = await crud.SubmenuCRUD.get_submenu_by_id(db=self.session, submenu_id=submenu_id)
        if db_submenu:
            db_submenu.title = submenu.title
            db_submenu.description = submenu.description
            return await crud.SubmenuCRUD.update_submenu(db=self.session, submenu_id=submenu_id)
        else:
            return None

    async def read_submenus(self, menu_id: int):
        submenus = await crud.SubmenuCRUD.get_submenus(db=self.session, menu_id=menu_id)
        return submenus

    async def read_submenu(self, menu_id: int, submenu_id: int):
        db_submenu = await crud.SubmenuCRUD.get_submenu_by_id(db=self.session, submenu_id=submenu_id)
        if db_submenu is None:
            return None
        return db_submenu

    async def delete_submenu(self, menu_id: int, submenu_id: int):
        db_submenu = await crud.SubmenuCRUD.delete_submenu(db=self.session, menu_id=menu_id, submenu_id=submenu_id)
        if db_submenu is None:
            return None
        return {"status": True, "message": "The submenu has been deleted"}


def get_submenu_service(session: AsyncSession = Depends(get_db)):
    return SubmenuService(session)
