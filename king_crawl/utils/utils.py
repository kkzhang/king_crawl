# -*- coding: utf-8 -*-
from lxml import etree
import pytz

__author__ = 'patrickz'


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