from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import models
from repository.database import get_db
from schemes import schemes


class MenuCRUD:

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_menu_by_id(self, menu_id: str):
        """Get menu by id"""
        return (await self.db.execute(select(models.Menu).where(models.Menu.id == menu_id))).scalar()

    async def get_menu_by_title(self, menu_title: str):
        'Get menu by title'
        return (await self.db.execute(select(models.Menu).where(models.Menu.title == menu_title))).scalar()

    async def get_menus(self):
        """Get menus list"""
        return (await self.db.execute(select(models.Menu))).scalars().all()

    async def create_menu(self, menu: schemes.MenuBase):
        """Create menu item"""
        db_menu = models.Menu(**menu.model_dump())
        db_menu.dishes_count = 0
        db_menu.submenus_count = 0
        self.db.add(db_menu)
        await self.db.commit()
        return db_menu

    async def delete_menu(self, menu_id: str):
        """Delete menu item"""
        db_menu = await self.get_menu_by_id(menu_id=menu_id)
        if db_menu is None:
            return None
        else:
            await self.db.delete(db_menu)
            await self.db.commit()
            return True

    async def update_menu(self, menu_id: str):
        """Update menu item"""
        await self.db.commit()
        return await self.get_menu_by_id(menu_id=menu_id)
