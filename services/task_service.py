from fastapi import Depends

from repository.task_rep import TaskRepository


class TaskService:
    def __init__(self, task_rep: TaskRepository = Depends(TaskRepository)):
        self.task_rep = task_rep

    async def fill_db_from_json(self):
        return await self.task_rep.fill_db_from_json()
