import json

import aiofiles
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import models

from .database import get_db

class FillMenu:
    @staticmethod
    async def fill(db: AsyncSession):
        """Fills database with test data from menu.json"""
        async with aiofiles.open("menuapp/menu.json") as f:
            content = await f.read()
        x = json.loads(content)

        for menu in x[0]:
            db_menu = models.Menu(**menu)
            db.add(db_menu)

        for submenu in x[1]:
            db_submenu = models.Submenu(**submenu)
            db.add(db_submenu)

        for dish in x[2]:
            db_dish = models.Dish(**dish)
            db.add(db_dish)
        await db.commit()

        return True
