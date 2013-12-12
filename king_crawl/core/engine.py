# -*- coding: utf-8 -*-
import glob
import importlib
import logging
import os
from king_downloader.core import RequestEngine, RedisRequestQueue
from king_downloader.utils import UserAgentProvider
from king_crawl.config import settings
from king_crawl.utils.proxy_provider import CustomProxyProvider
import king_crawl.config.environment as env
import king_crawl.core.initialize

logger = logging.getLogger(settings.CELERY_NAME+'.engine')

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
        logger.info('Set up proxy provider')
    else:
        request_engine.setup_proxy_provider(CustomProxyProvider())

    if hasattr(settings,'UA_PROVIDER'):
        ua_provider = getattr(importlib.import_module(settings.UA_PROVIDER[0]), settings.UA_PROVIDER[1])
        request_engine.setup_user_agent_provider(ua_provider())
        logger.info('Set up UA provider')
    else:
        request_engine.setup_user_agent_provider(UserAgentProvider())


    request_engine.setup_request_queue(env.request_queue)
    env.downloader = request_engine


# Processors

processors = importlib.import_module('app.processors')
for f in glob.glob(os.path.dirname(processors.__file__)+"/*.py"):
    __import__('app.processors.'+os.path.basename(f)[:-3])

def start():
    env.downloader.request()