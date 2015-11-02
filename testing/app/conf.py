from celery import Celery
from datetime import datetime, timedelta

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 10

REDIS = 'redis://%s:%s/%s' % (REDIS_HOST, REDIS_PORT, REDIS_DB)

test_app = Celery('test_app',
    broker=REDIS,
    include=['app.tasks']
)

SLEEPY_QUEUE = 'sleepy'

def get_sleeper_task():
    return {
        'task': 'app.tasks.random_sleep',
        'schedule': timedelta(seconds=1),
        'args': (5, 10)
    }

test_app.conf.update(
    BROKER_TRANSPORT_OPTIONS={'visibility_timeout': 60*5},
    CELERY_RESULT_BACKEND=REDIS,
    CELERY_TASK_RESULT_EXPIRES=timedelta(minutes=5),
    CELERYD_TASK_SOFT_TIME_LIMIT=60*3,
    CELERYD_TASK_TIME_LIMIT=60*5,
    CELERYD_MAX_TASKS_PER_CHILD=20,
    CELERY_CREATE_MISSING_QUEUES=True,
    CELERY_RESULT_PERSISTENT=True,
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['pickle', 'json'],
    CELERY_SEND_TASK_SENT_EVENT=True,
    # CELERYD_HIJACK_ROOT_LOGGER = False,
    CELERYBEAT_SCHEDULE={
        'kickoff-sleeps': {
            'task': 'app.tasks.kickoff_sleeps',
            'schedule': timedelta(seconds=5),
            'args': (3, 5, 20)
        }
    }
)

