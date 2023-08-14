from fastapi import BackgroundTasks, Depends
from fastapi.encoders import jsonable_encoder

from cache import redis_cache as cache
from repository.dish_crud import DishCRUD
from schemes import schemes


class DishService:
    def __init__(self, dish_crud: DishCRUD = Depends(DishCRUD)):
        self.dish_crud = dish_crud

    async def create_dish(self, menu_id: str, submenu_id: str, dish: schemes.DishBase):
        dish.price = f'{float(dish.price):.2f}'
        db_dish = await self.dish_crud.get_dish_by_title(dish_title=dish.title)
        if db_dish:
            return None
        await cache.delete_cache(f'/api/v1/menus/{menu_id}')
        return await self.dish_crud.create_dish(dish=dish, menu_id=menu_id, submenu_id=submenu_id)

    async def update_dish(self, menu_id: str, submenu_id: str, dish_id: str, dish: schemes.DishUpdate):
        db_dish = await self.dish_crud.get_dish_by_id(dish_id=dish_id)
        if db_dish:
            db_dish.title = dish.title
            db_dish.description = dish.description
            db_dish.price = dish.price
            await cache.set_cache(
                f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
                jsonable_encoder(db_dish),
            )
            return await self.dish_crud.update_dish(dish_id=dish_id)
        else:
            return None

    async def read_dishes(self, menu_id: str, submenu_id: str):
        dishes = await self.dish_crud.get_dishes(menu_id=menu_id, submenu_id=submenu_id)
        if dishes:
            for dish in dishes:
                await cache.set_cache(
                    f'/api/v1/menus/{menu_id}/submenus/\
                    {submenu_id}/dishes/{dish.id}',
                    jsonable_encoder(dish),
                )
        return dishes

    async def read_dish(self, menu_id: str, submenu_id: str, dish_id: str):
        cached = await cache.get_cache(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
        if cached:
            db_dish = cached
        else:
            db_dish = await self.dish_crud.get_dish_by_id(dish_id=dish_id)
        if db_dish is None:
            return None
        await cache.set_cache(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
            jsonable_encoder(db_dish),
        )
        return db_dish

    async def delete_dish(self, menu_id: str, submenu_id: str, dish_id: str, background_tasks: BackgroundTasks):
        db_dish = await self.dish_crud.delete_dish(
            dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id
        )
        if db_dish is None:
            return None
        background_tasks.add_task(cache.delete_cache, f'/api/v1/menus/{menu_id}')
        return {'status': True, 'message': 'The dish has been deleted'}
