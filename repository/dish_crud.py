from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import models

from schemes import schemes
from .database import get_db

from fastapi import Depends

from .menu_crud import MenuCRUD
from .submenu_crud import SubmenuCRUD

class DishCRUD:
    @staticmethod
    async def get_dish_by_id(dish_id: str, db: AsyncSession):
        """Get dish by id"""
        return (await db.execute(select(models.Dish).where(models.Dish.id == dish_id))).scalar()

    @staticmethod
    async def get_dish_by_title(dish_title: str, db: AsyncSession):
        """Get dish by title"""
        return (await db.execute(select(models.Dish).where(models.Dish.title == dish_title))).scalar()

    @staticmethod
    async def get_dishes(menu_id: str, submenu_id: str, db: AsyncSession):
        """Get dishes list"""
        return (
            (
                await db.execute(
                    select(models.Dish)
                    .where(models.Dish.menu_id == menu_id)
                    .where(models.Dish.submenu_id == submenu_id)
                )
            )
            .scalars()
            .all()
        )

    @staticmethod
    async def create_dish(dish: schemes.DishBase, menu_id: str, submenu_id: str, db: AsyncSession):
        """Create dish item"""
        db_dish = models.Dish(**dish.model_dump())
        db_dish.menu_id = menu_id
        db_dish.submenu_id = submenu_id
        (await MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id)).dishes_count += 1
        (await SubmenuCRUD.get_submenu_by_id(db=db, submenu_id=submenu_id)).dishes_count += 1
        db.add(db_dish)
        await db.commit()
        return db_dish

    @staticmethod
    async def delete_dish(dish_id: str, menu_id: str, submenu_id: str, db: AsyncSession):
        """Delete dish item"""
        db_dish = await DishCRUD.get_dish_by_id(db=db, dish_id=dish_id)
        if db_dish is None:
            return None
        else:
            (await MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id)).dishes_count -= 1
            (await SubmenuCRUD.get_submenu_by_id(db=db, submenu_id=submenu_id)).dishes_count -= 1
            await db.delete(db_dish)
            await db.commit()
            return True

    @staticmethod
    async def update_dish(dish_id: str, db: AsyncSession):
        """Update dish item"""
        await db.commit()
        return await DishCRUD.get_dish_by_id(db=db, dish_id=dish_id)