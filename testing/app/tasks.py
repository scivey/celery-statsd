from .conf import test_app, SLEEPY_QUEUE
from celery.utils.log import get_task_logger
import random
import time
import logging

logger = get_task_logger(__name__)

@test_app.task(queue=SLEEPY_QUEUE)
def random_sleep(min_time, max_time):
    sleep_time = random.uniform(min_time, max_time)
    logger.info('random_sleep (%i, %i) : sleeping for %f' % (min_time, max_time, sleep_time))
    time.sleep(sleep_time)
    logger.info('random_sleep: finished sleeping for %s' % sleep_time)


@test_app.task
def kickoff_sleeps(n_cycles, min_time, max_time):
    count = random.randint(1, 10)
    min_time = float(min_time)
    max_time = float(max_time)
    time_interval = float(max_time) - float(min_time)
    mid_time = min_time + (time_interval / 2)
    for _ in xrange(n_cycles):
        current_min = random.uniform(min_time, mid_time)
        current_max = random.uniform(mid_time, max_time)
        for _ in xrange(count):
            random_sleep.apply_async([current_min, current_max])
