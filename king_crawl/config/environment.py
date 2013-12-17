# -*- coding: utf-8 -*-
# from __future__ import absolute_import
import glob
import importlib

import os
from celery import Celery
from redis import Redis
from king_crawl.config import settings

redis_ins = None

_workers= []
workers = importlib.import_module('app.workers')
for f in glob.glob(os.path.dirname(workers.__file__)+"/*.py"):
    if f.find('__init__.py') == -1:
        _workers.append('app.workers.' + os.path.basename(f)[:-3])



app = Celery(settings.CELERY_NAME,
                broker=settings.CELERY_BROKER,
                backend=settings.CELERY_BACKEND,
                include=_workers
                )

for s in settings.__dict__:
    if s.startswith('CELERY_SETTINGS_'):
        app.conf.update({s[16:]:getattr(settings,s)})

app_status = 1 # 1 for normal, 0 for shutdown

mysql_engine = None
DbBase = None
DbSession = None
request_queue = None
downloader = None
raven_client = None
logger = None

env = importlib.import_module('config.environment')
for _e in dir(env):
    globals()[_e] = getattr(env, _e)