#! /usr/bin/env python

from __future__ import absolute_import
import logging, logtool
from celery import current_app
from qworkerd import retry_handler
from .qstask import QSTask

LOG = logging.getLogger (__name__)

@current_app.task (bind = True, base = QSTask)
@logtool.log_call
def test (self, num1, num2): # pylint: disable=unused-argument
  try:
    rc = num1 + num2
    LOG.info ("Called: %s + %s = %s",num1, num2, rc)
    return rc
  except Exception as e:
    retry_handler (self, e)
    raise

@current_app.task (bind = True, base = QSTask)
@logtool.log_call
def fail (self): # pylint: disable=unused-argument
  raise Exception ("Oh dear")
