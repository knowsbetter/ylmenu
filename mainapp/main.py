from fastapi import Depends, FastAPI

from routers import menu_router, submenu_router, dish_router

from models import models
from repository.database import start_db

app = FastAPI(title="Приложение для меню")


@app.on_event("startup")
async def startup_event():
    await start_db()

app.include_router(menu_router.menu_router)
app.include_router(submenu_router.submenu_router)
app.include_router(dish_router.dish_router)