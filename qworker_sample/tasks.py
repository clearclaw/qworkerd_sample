#! /usr/bin/env python

from __future__ import absolute_import
import datetime, logging, logtool, raven, sys
from celery import current_app
from celery.exceptions import Retry
from django.conf import settings

LOG = logging.getLogger (__name__)

@logtool.log_call
def sentry_exception (e, request, message = None):
  sentry_tags = {"component": "qworker_sample"}
  try:
    sentry = raven.Client (settings.RAVEN_CONFIG["dsn"],
                           auto_log_stacks = True)
    logtool.log_fault (e, message = message)
    data = {
      "job": request,
    }
    if message:
      data["message"] = message
    sentry.extra_context (data)
    if e is not None:
      einfo = sys.exc_info ()
      rc = sentry.captureException (einfo, **sentry_tags)
      del einfo
    else:
      rc = sentry.capture (**sentry_tags)
    LOG.error ("Sentry filed: %s", rc)
  except Exception as ee:
    logtool.log_fault (ee, message = "FAULT: Problem logging exception.")

@logtool.log_call
def retry_handler (task, e, typ, key, time_dt):
  try:
    LOG.info ("Retrying.  Attempt: #%s", task.request.retries)
    raise task.retry (exc = e, max_retries = settings.FAIL_RETRYCOUNT,
                      countdown = (settings.FAIL_WAITTIME
                                   * (task.request.retries + 1)))
  except Retry: # Why yes, we're retrying
    raise
  except: # pylint: disable=W0702
    LOG.error ("Max retries reached: %s  GIVING UP!", task.request.retries)
    sentry_exception (e, task.request)
    raise

@current_app.task (bind = True)
@logtool.log_call
def test (self, num1, num2):
  rc = num1 + num2
  LOG.info ("Called: %s + %s = %s" % (num1, num2, rc))
  return rc
