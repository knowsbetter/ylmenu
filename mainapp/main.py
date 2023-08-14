from fastapi import FastAPI

from repository.database import start_db
from routers import dish_router, menu_router, submenu_router, task_router

app = FastAPI(title='Приложение для меню')


@app.on_event('startup')
async def startup_event():
    await start_db()

app.include_router(menu_router.menu_router)
app.include_router(submenu_router.submenu_router)
app.include_router(dish_router.dish_router)
app.include_router(task_router.task_router)
