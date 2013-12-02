# -*- coding: utf-8 -*-
from __future__ import absolute_import
import glob
import importlib

import logging
from logging.config import dictConfig
import os
from king_downloader.core import RequestEngine, RedisRequestQueue
from king_downloader.utils import UserAgentProvider
import gevent
from redis import Redis
import signal
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import king_crawl.config.environment as env
from king_crawl.config import settings
from king_crawl.utils.helper import worker
from king_crawl.utils.proxy_provider import CustomProxyProvider

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

# Request Engine

if settings.CUSTOM_DOWNLOADER == False:
    request_engine = RequestEngine(pool_size=settings.ENGINE_REQUEST_CONCURRENCY,
                                       max_empty_retry=-1,
                                       request_interval=settings.ENGINE_REQUEST_INTERVAL,
                                       max_failure_allowed=settings.ENGINE_MAX_FAIL,
                                       request_timeout=settings.ENGINE_DEFAULT_TIMEOUT)

    #Proxy
    if hasattr(settings,'PROXY_PROVIDER'):
        proxy_provider = getattr(importlib.import_module(settings.PROXY_PROVIDER[0]), settings.PROXY_PROVIDER[1])
        request_engine.setup_proxy_provider(proxy_provider(**settings.PROXY_PROVIDER_ARGUMENTS))
        env.logger.info('Set up proxy provider')
    else:
        request_engine.setup_proxy_provider(CustomProxyProvider())

    if hasattr(settings,'UA_PROVIDER'):
        ua_provider = getattr(importlib.import_module(settings.UA_PROVIDER[0]), settings.UA_PROVIDER[1])
        request_engine.setup_user_agent_provider(ua_provider())
    else:
        request_engine.setup_user_agent_provider(UserAgentProvider())

    env.request_queue = RedisRequestQueue()
    env.request_queue.setup_by_redis_instance(env.redis_ins, settings.REDIS_REQUESTS_QUEUE)
    request_engine.setup_request_queue(env.request_queue)
    env.downloader = request_engine


@worker('engine')
def start_engine(*args, **kwargs):
    env.downloader.request()


# Processors

processors = importlib.import_module('app.processors')
for f in glob.glob(os.path.dirname(processors.__file__)+"/*.py"):
    __import__('app.processors.'+os.path.basename(f)[:-3])


def init():
    start_engine.apply_async(queue=settings.ENGINE_QUEUE)

def shutdown_app():
    env.app_status=0

gevent.signal(signal.SIGINT, handler=shutdown_app)

