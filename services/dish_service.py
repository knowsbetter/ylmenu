from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from schemes import schemes
from repository.dish_crud import DishCRUD


class DishService:
    def __init__(self, dish_crud: DishCRUD = Depends(DishCRUD)):
        self.dish_crud = dish_crud

    async def create_dish(self, menu_id: str, submenu_id: str, dish: schemes.DishBase):
        dish.price = "{:.2f}".format(float(dish.price))
        db_dish = await self.dish_crud.get_dish_by_title(dish_title=dish.title)
        if db_dish:
            return None
        return await self.dish_crud.create_dish(dish=dish, menu_id=menu_id, submenu_id=submenu_id)

    async def update_dish(self, menu_id: str, submenu_id: str, dish_id: str, dish: schemes.DishUpdate):
        db_dish = await self.dish_crud.get_dish_by_id(dish_id=dish_id)
        if db_dish:
            db_dish.title = dish.title
            db_dish.description = dish.description
            db_dish.price = dish.price
            return await self.dish_crud.update_dish(dish_id=dish_id)
        else:
            return None

    async def read_dishes(self, menu_id: str, submenu_id: str):
        dishes = await self.dish_crud.get_dishes(menu_id=menu_id, submenu_id=submenu_id)
        return dishes

    async def read_dish(self, menu_id: str, submenu_id: str, dish_id: str):
        db_dish = await self.dish_crud.get_dish_by_id(dish_id=dish_id)
        if db_dish is None:
            return None
        return db_dish

    async def delete_dish(self, menu_id: str, submenu_id: str, dish_id: str):
        db_dish = await self.dish_crud.delete_dish(
            dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id
        )
        if db_dish is None:
            return None
        return {"status": True, "message": "The dish has been deleted"}
