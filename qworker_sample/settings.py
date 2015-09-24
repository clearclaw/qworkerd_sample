#! /usr/bin/env python

import importlib, logging, logtool, sys
from kombu import Exchange, Queue

LOG = logging.getLogger (__name__)

CELERYD_STATS_PREFIX = "qworker_sample."

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
FAIL_RETRYCOUNT = 5

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

# DESIRED & REQUIRED are used for variables defined outside of the
# Python package/code.
DESIRED_VARIABLES = [
#  "CELERYD_CONCURRENCY",
]
REQUIRED_VARIABLES = [
  "EXAMPLE_VARIABLE1",
  "EXAMPLE_VARIABLE2",
  "EXAMPLE_VARIABLE3",
]
EXPORT_VARS = [
  "CELERYD_STATS_PREFIX",
  "CELERYD_TASK_SOFT_TIME_LIMIT",
  "CELERYD_TASK_TIME_LIMIT",
  "EXAMPLE_VARIABLE1",
  "EXAMPLE_VARIABLE2",
  "EXAMPLE_VARIABLE3",
  "FAIL_RETRYCOUNT",
  "FAIL_WAITTIME",
]

@logtool.log_call
def check_vars (wanted, provided):
  return [var for var in wanted if var not in provided]

missing = check_vars (DESIRED_VARIABLES, vars ())
if missing:
  print >> sys.stderr, "Missing desired configurations: %s" % missing
missing = check_vars (REQUIRED_VARIABLES, vars ())
if missing:
  print >> sys.stderr, "Missing required configurations: %s" % missing
  sys.exit ()

@logtool.log_call
def install ():
  mod = importlib.import_module ("qworkerd.settings")
  mod.INSTALLED_APPS += (
    "qworker_sample",
  )
  mod.CELERY_QUEUES.extend (CELERY_QUEUES)
  for var in EXPORT_VARS:
    setattr (mod, var, globals ()[var])
