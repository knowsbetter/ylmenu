from celery.result import AsyncResult

from taskworker.main import app
from taskworker.utils import works


@app.task
def get_status(task_id):
    return AsyncResult(task_id).status


@app.task
def check_changes():
    works.find_changes()
