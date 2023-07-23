from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from mainapp import crud, schemes
from mainapp.database import SessionLocal


async def get_db():
    """Returns database session"""
    async with SessionLocal() as db:
        yield db


class DishService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_dish(self, menu_id: str, submenu_id: str, dish: schemes.DishBase):
        db_dish = await crud.DishCRUD.get_dish_by_title(db=self.session, dish_title=dish.title)
        if db_dish:
            return None
        return await crud.DishCRUD.create_dish(db=self.session, dish=dish, menu_id=menu_id, submenu_id=submenu_id)

    async def update_dish(self, menu_id: str, submenu_id: str, dish_id: str, dish: schemes.DishUpdate):
        db_dish = await crud.DishCRUD.get_dish_by_id(db=self.session, dish_id=dish_id)
        if db_dish:
            db_dish.title = dish.title
            db_dish.description = dish.description
            db_dish.price = dish.price
            return await crud.DishCRUD.update_dish(db=self.session, dish_id=dish_id)
        else:
            return None

    async def read_dishes(self, menu_id: str, submenu_id: str):
        dishes = await crud.DishCRUD.get_dishes(db=self.session, menu_id=menu_id, submenu_id=submenu_id)
        return dishes

    async def read_dish(self, menu_id: str, submenu_id: str, dish_id: str):
        db_dish = await crud.DishCRUD.get_dish_by_id(db=self.session, dish_id=dish_id)
        if db_dish is None:
            return None
        return db_dish

    async def delete_dish(self, menu_id: str, submenu_id: str, dish_id: str):
        db_dish = await crud.DishCRUD.delete_dish(
            db=self.session, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id
        )
        if db_dish is None:
            return None
        return {"status": True, "message": "The dish has been deleted"}


def get_dish_service(session: AsyncSession = Depends(get_db)):
    return DishService(session)
