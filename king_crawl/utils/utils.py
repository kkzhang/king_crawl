# -*- coding: utf-8 -*-
from functools import wraps
import logging
from lxml import etree
import pytz
import time

__author__ = 'patrickz'

logger = logging.getLogger('king_crawl.utils')

def datetime_to_utc(dt, tz='Asia/Shanghai'):
    timezone = pytz.timezone(tz)
    naive = timezone.localize(dt)
    return naive.astimezone(pytz.utc)


def innerHTML(node):
    buildString = ''
    for child in node.iterchildren():
        buildString += etree.tostring(child)
    return buildString

def content_filter(replace_patterns, content):
    _content = content

    for r in replace_patterns.iterkeys():
        _content = r.sub(replace_patterns[r], _content)

    return _content

def retriable_exec(sleep_time = 3):
    def inner(func):
        @wraps(func)
        def _inner2_(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                logger.error('Retry executing function :'+ func.__name__ , exc_info=True)
                time.sleep(sleep_time)
                return inner(func)(*args, **kwargs)
        return _inner2_
    return inner