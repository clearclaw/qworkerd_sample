#! /usr/bin/env python

import logging
from kombu import Exchange, Queue

LOG = logging.getLogger (__name__)

# Task soft time limit in seconds.
# The SoftTimeLimitExceeded exception will be raised when this is
# exceeded. The task can catch this to e.g. clean up before the hard
# time limit comes.
# http://celery.readthedocs.org/en/latest/configuration.html#celeryd-task-soft-time-limit
CELERYD_TASK_SOFT_TIME_LIMIT = 30

# Task hard time limit in seconds. The worker processing the task will
# be killed and replaced with a new one when this is exceeded.
CELERYD_TASK_TIME_LIMIT = 36

# How long to wait before trying a job again
FAIL_WAITTIME = 60

# How many times to retry failed jobs
FAIL_RETRYCOUNT = 1

# CELERY_QUEUES is a list of Queue instances. If you don't set the
# exchange or exchange type values for a key, these will be taken from
# the CELERY_DEFAULT_EXCHANGE and CELERY_DEFAULT_EXCHANGE_TYPE
# settings.
CELERY_QUEUES = [
  Queue ("qworker_sample", Exchange ("qworker_sample"),
         routing_key = "qworker_sample"),
]

EXTERNAL_CONFIG = "/etc/qworkerd/qworker_sample.conf"
execfile (EXTERNAL_CONFIG)

EXTEND_VARS = ["CELERY_QUEUES",]
