from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import models

from schemes import schemes
from .database import get_db

from fastapi import Depends

class MenuCRUD:
    @staticmethod
    async def get_menu_by_id(menu_id: str, db: AsyncSession):
        """Get menu by id"""
        return (await db.execute(select(models.Menu).where(models.Menu.id == menu_id))).scalar()

    @staticmethod
    async def get_menu_by_title(menu_title: str, db: AsyncSession):
        "Get menu by title"
        return (await db.execute(select(models.Menu).where(models.Menu.title == menu_title))).scalar()

    @staticmethod
    async def get_menus(db: AsyncSession):
        """Get menus list"""
        return (await db.execute(select(models.Menu))).scalars().all()

    @staticmethod
    async def create_menu(menu: schemes.MenuBase, db: AsyncSession):
        """Create menu item"""
        db_menu = models.Menu(**menu.model_dump())
        db_menu.dishes_count = 0
        db_menu.submenus_count = 0
        db.add(db_menu)
        await db.commit()
        return db_menu

    @staticmethod
    async def delete_menu(menu_id: str, db: AsyncSession):
        """Delete menu item"""
        db_menu = await MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id)
        if db_menu is None:
            return None
        else:
            await db.delete(db_menu)
            await db.commit()
            return True

    @staticmethod
    async def update_menu(menu_id: str, db: AsyncSession):
        """Update menu item"""
        await db.commit()
        return await MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id)