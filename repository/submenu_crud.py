from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import models

from schemes import schemes
from .database import get_db

from fastapi import Depends

from .menu_crud import MenuCRUD

class SubmenuCRUD:
    @staticmethod
    async def get_submenu_by_id(submenu_id: str, db: AsyncSession):
        """Get submenu by id"""
        return (await db.execute(select(models.Submenu).where(models.Submenu.id == submenu_id))).scalar()

    @staticmethod
    async def get_submenu_by_title(submenu_title: str, db: AsyncSession):
        """Get submenu by title"""
        return (await db.execute(select(models.Submenu).where(models.Submenu.title == submenu_title))).scalar()

    @staticmethod
    async def get_submenus(menu_id: str, db: AsyncSession):
        """Get submenus list"""
        return (await db.execute(select(models.Submenu).where(models.Submenu.menu_id == menu_id))).scalars().all()

    @staticmethod
    async def create_submenu(submenu: schemes.SubmenuBase, menu_id: str, db: AsyncSession):
        """Create submenu item"""
        db_submenu = models.Submenu(**submenu.model_dump())
        db_submenu.menu_id = menu_id
        db_submenu.dishes_count = 0
        (await MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id)).submenus_count += 1
        db.add(db_submenu)
        await db.commit()
        return db_submenu

    @staticmethod
    async def delete_submenu(menu_id: str, submenu_id: str, db: AsyncSession):
        """Delete submenu item"""
        db_submenu = await SubmenuCRUD.get_submenu_by_id(db=db, submenu_id=submenu_id)
        if db_submenu is None:
            return None
        else:
            db_menu = await MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id)
            db_menu.submenus_count -= 1
            db_menu.dishes_count -= db_submenu.dishes_count
            await db.delete(db_submenu)
            await db.commit()
            return True

    @staticmethod
    async def update_submenu(submenu_id: str, db: AsyncSession):
        """Update submenu item"""
        await db.commit()
        return await SubmenuCRUD.get_submenu_by_id(db=db, submenu_id=submenu_id)