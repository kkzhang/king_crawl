# -*- coding: utf-8 -*-
__author__ = 'patrickz'


DEBUG = True


# Celery

CELERY_NAME = 'fiction_scraper'
CELERY_BROKER = 'amqp://guest@localhost//'
CELERY_BACKEND = 'amqp://guest@localhost//'
TASKNAME_PREFIX = 'tasks'


# Database

SQLALCHEMY_INFO = "mysql+oursql://root:123456@127.0.0.1/fiction_fetcher"

# Sentry

SENTRY_CONN_STRING = 'http://25ccfca740cc4899bd7086feb1d5105e:20320aa542e84afeb04fa19dfc26bed2@localhost:9000/2'

# Redis
REDIS_CFG = {
    'host':'localhost'
}

# Downloader Options
CUSTOM_DOWNLOADER = False
ENGINE_QUEUE = CELERY_NAME
ENGINE_REQUEST_CONCURRENCY = 1000
ENGINE_DEFAULT_TIMEOUT = 60
ENGINE_MAX_FAIL = -1
ENGINE_REQUEST_INTERVAL = 3
PROXY_PROVIDER = ['king_crawl.utils.proxy_provider','CustomProxyProvider']
REQUEST_MAX_FAIL = 3
REDIS_REQUESTS_QUEUE = 'usearch_requests'




LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'console': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s %(filename)s:%(funcName)s:%(lineno)d | %(message)s',
            'datefmt': '%H:%M:%S',
            },
        },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
            },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.handlers.logging.SentryHandler',
            'dsn': SENTRY_CONN_STRING,
            },
        },

    'loggers': {
        'requests': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
            },
        CELERY_NAME: {
            'handlers': ['console','sentry'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'celery_scraper2': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
