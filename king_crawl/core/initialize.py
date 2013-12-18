# -*- coding: utf-8 -*-
from __future__ import absolute_import
import glob
import importlib

import logging
from logging.config import dictConfig
import os
from king_downloader.core import RedisRequestQueue
from redis import Redis
import king_crawl.config.environment as env
from king_crawl.config import settings
from king_crawl.utils.helper import worker

dictConfig(settings.LOGGING)

env.logger = logging.getLogger(settings.CELERY_NAME)


# Database
#env.mysql_engine = create_engine(settings.SQLALCHEMY_INFO, echo=True)
#
#env.DbBase = declarative_base()
#env.DbBase.metadata.reflect(env.mysql_engine)
#env.DbSession = sessionmaker(bind=env.mysql_engine)


# Redis
env.redis_ins = Redis(**settings.REDIS_CFG)

# Request Queue
env.request_queue = RedisRequestQueue()
env.request_queue.setup_by_redis_instance(env.redis_ins, settings.REDIS_REQUESTS_QUEUE)

# Outline settings

_cfg_outline = '\nSettings Outline:\n-----------------------\n'
for s in settings.__dict__:
    if s==s.upper():
        _cfg_outline +=  ('['+s+"] " + str(getattr(settings,s)) +'\n')

env.logger.info(_cfg_outline)

# @worker('engine')
# def start_engine(*args, **kwargs):
#     env.downloader.request()
#
#
# def init_engine():
#     start_engine.apply_async(queue=settings.ENGINE_QUEUE)

def shutdown_app():
    env.app_status=0

#gevent.signal(signal.SIGINT, handler=shutdown_app)

