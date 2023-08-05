from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import models
from schemes import schemes

from .database import get_db
from .menu_crud import MenuCRUD
from .submenu_crud import SubmenuCRUD


class DishCRUD:

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_dish_by_id(self, dish_id: str):
        """Get dish by id"""
        return (await self.db.execute(select(models.Dish).where(models.Dish.id == dish_id))).scalar()

    async def get_dish_by_title(self, dish_title: str):
        """Get dish by title"""
        return (await self.db.execute(select(models.Dish).where(models.Dish.title == dish_title))).scalar()

    async def get_dishes(self, menu_id: str, submenu_id: str):
        """Get dishes list"""
        return (
            (
                await self.db.execute(
                    select(models.Dish)
                    .where(models.Dish.menu_id == menu_id)
                    .where(models.Dish.submenu_id == submenu_id)
                )
            )
            .scalars()
            .all()
        )

    async def create_dish(self, dish: schemes.DishBase, menu_id: str, submenu_id: str):
        """Create dish item"""
        db_dish = models.Dish(**dish.model_dump())
        db_dish.menu_id = menu_id
        db_dish.submenu_id = submenu_id
        menu_crud = MenuCRUD(db=self.db)
        submenu_crud = SubmenuCRUD(db=self.db)
        (await menu_crud.get_menu_by_id(menu_id=menu_id)).dishes_count += 1
        (await submenu_crud.get_submenu_by_id(submenu_id=submenu_id)).dishes_count += 1
        self.db.add(db_dish)
        await self.db.commit()
        return db_dish

    async def delete_dish(self, dish_id: str, menu_id: str, submenu_id: str):
        """Delete dish item"""
        db_dish = await self.get_dish_by_id(dish_id=dish_id)
        if db_dish is None:
            return None
        else:
            menu_crud = MenuCRUD(db=self.db)
            submenu_crud = SubmenuCRUD(db=self.db)
            (await menu_crud.get_menu_by_id(menu_id=menu_id)).dishes_count -= 1
            (await submenu_crud.get_submenu_by_id(submenu_id=submenu_id)).dishes_count -= 1
            await self.db.delete(db_dish)
            await self.db.commit()
            return True

    async def update_dish(self, dish_id: str):
        """Update dish item"""
        await self.db.commit()
        return await self.get_dish_by_id(dish_id=dish_id)
