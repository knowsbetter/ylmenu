import os

from celery import Celery

from taskworker import config
from taskworker.utils import works

# celery -A taskworker.main worker --loglevel=INFO --pool=solo
# celery -A taskworker.main beat --loglevel=INFO
# celery -A taskworker.main worker -B --loglevel=INFO --pool=solo
# celery -A taskworker.main flower

app = Celery('taskworker',
             broker=config.RABBIT_BROKER,
             backend=config.RABBIT_BACKEND,
             include=['taskworker.tasks'])

app.conf.beat_schedule = {
    'every-15-seconds':
    {
        'task': 'taskworker.tasks.check_changes',
        'schedule': 15.0,
    },
}


def start_update():
    if os.path.exists('taskworker/output/menu.json'):
        return
    works.write_to_json(works.excel_to_json())
    works.signal_to_update_db()


start_update()

# if __name__ == "__main__":
#     app.start()
#     start_update()
