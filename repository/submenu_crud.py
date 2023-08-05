from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import models
from schemes import schemes

from .database import get_db
from .menu_crud import MenuCRUD


class SubmenuCRUD:

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_submenu_by_id(self, submenu_id: str):
        """Get submenu by id"""
        return (await self.db.execute(select(models.Submenu).where(models.Submenu.id == submenu_id))).scalar()

    async def get_submenu_by_title(self, submenu_title: str):
        """Get submenu by title"""
        return (await self.db.execute(select(models.Submenu).where(models.Submenu.title == submenu_title))).scalar()

    async def get_submenus(self, menu_id: str):
        """Get submenus list"""
        return (await self.db.execute(select(models.Submenu).where(models.Submenu.menu_id == menu_id))).scalars().all()

    async def create_submenu(self, submenu: schemes.SubmenuBase, menu_id: str):
        """Create submenu item"""
        db_submenu = models.Submenu(**submenu.model_dump())
        db_submenu.menu_id = menu_id
        db_submenu.dishes_count = 0
        menu_crud = MenuCRUD(db=self.db)
        (await menu_crud.get_menu_by_id(menu_id=menu_id)).submenus_count += 1
        self.db.add(db_submenu)
        await self.db.commit()
        return db_submenu

    async def delete_submenu(self, menu_id: str, submenu_id: str):
        """Delete submenu item"""
        db_submenu = await self.get_submenu_by_id(submenu_id=submenu_id)
        if db_submenu is None:
            return None
        else:
            menu_crud = MenuCRUD(db=self.db)
            db_menu = await menu_crud.get_menu_by_id(menu_id=menu_id)
            db_menu.submenus_count -= 1
            db_menu.dishes_count -= db_submenu.dishes_count
            await self.db.delete(db_submenu)
            await self.db.commit()
            return True

    async def update_submenu(self, submenu_id: str):
        """Update submenu item"""
        await self.db.commit()
        return await self.get_submenu_by_id(submenu_id=submenu_id)
