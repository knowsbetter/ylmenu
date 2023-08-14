from fastapi import APIRouter, Depends

from services.task_service import TaskService

task_router = APIRouter()


@task_router.post(
    path='/api/v1/admin/fill_db_from_json/',
    summary='Заполнить базу из excel-файла',
    status_code=200,
    tags=['Панель администратора'],
)
async def fill_db_from_json(task_service: TaskService = Depends(TaskService)):
    """Create test menu"""
    return await task_service.fill_db_from_json()
