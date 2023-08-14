import json

import aiofiles
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models import models
from repository.database import get_db


class TaskRepository:

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def fill_db_from_json(self):
        """Fills database with data from menu.json"""
        # async with engine.begin() as conn:
        #    await conn.run_sync(Base.metadata.drop_all)
        #    await conn.run_sync(Base.metadata.create_all)
        async with aiofiles.open('taskworker/output/menu.json') as f:
            content = await f.read()
        x = json.loads(content)

        for menu in x[0]:
            db_menu = models.Menu(**menu)
            self.db.add(db_menu)

        for submenu in x[1]:
            db_submenu = models.Submenu(**submenu)
            self.db.add(db_submenu)

        for dish in x[2]:
            db_dish = models.Dish(**dish)
            self.db.add(db_dish)
        await self.db.commit()

    #    from taskworker.tasks import set_ready_to_check_changes
    #    set_ready_to_check_changes.delay(True)

        return True
