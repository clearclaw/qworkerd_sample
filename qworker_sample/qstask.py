#! /usr/bin/env python

from qworkerd.qwtask import QWTask
from . import settings

class QSTask (QWTask): # pylint: disable=abstract-method
  abstract = True
  max_retries = settings.FAIL_RETRYCOUNT
  default_retry_period = settings.FAIL_WAITTIME
  time_limit = settings.CELERYD_TASK_TIME_LIMIT
  soft_time_limit = settings.CELERYD_TASK_SOFT_TIME_LIMIT
