# -*- coding: utf-8 -*-
from king_downloader.core import RequestItem
from kombu import uuid
import pytz
from king_crawl.config import settings

import king_crawl.config.environment as env

__author__ = 'patrickz'

def processor(name=None):

    def _wrapper(func):
        print "Registering Processor %s" % name

        def _w(*args, **kwargs):
            try:
                return func(processor_name = name, *args, **kwargs)
            except:
                env.logger.error("Error When Processor Run", exc_info = True,
                                 extra={'data':
                                            {
                                                'processor':name,
                                                'request': kwargs['request'].dumps()
                                            }
                                 })
        env.downloader.register_processor(_w,name)
        return _w
    return _wrapper

def worker(name=None, *args, **kwargs):
    specific_name = name
    def _wrapper(func):
        if specific_name is None:
            full_name = settings.TASKNAME_PREFIX +func.__name__
        else:
            full_name = settings.TASKNAME_PREFIX + name
        @env.app.task(name=full_name, *args, **kwargs)
        def _w(*actual_args, **actual_kwargs):
            try:
                return func(worker_name = full_name,*actual_args, **actual_kwargs)
            except Exception as Exc:
                if not isinstance(Exc, SystemExit):
                    env.logger.error("Error Occur When Worker Run", exc_info = True,
                                     extra={'data':
                                                {
                                                    'worker':full_name,
                                                }
                                     })
        return _w
    return _wrapper

def add_request(*args, **kwargs):
    if args and hasattr(args[0],'to_msgpack'):
        req = args[0]
        env.request_queue.push(req)
    else:
        if args and type(args[0]) == str:
            kwargs['url'] = args[0]

        if kwargs and not ('method' in kwargs):
            kwargs['method']='get'

        if kwargs and type(kwargs['processors']) == str:
            kwargs['processors'] = {'after':kwargs['processors']}

        if kwargs and hasattr(kwargs['processors'],'processor_name'):
            kwargs['processors'] = {'after':kwargs['processors'].processor_name}

        if kwargs and ('extra' in kwargs):
            kwargs['raw_info']=kwargs['extra']
            kwargs.pop('extra')

        env.request_queue.push(RequestItem(**kwargs))

def reschedule_request(request, callback=None, *args, **kwargs):
    retry = int(getattr(request.raw_info, '_retry', 0))
    if retry >= settings.REQUEST_MAX_FAIL:
        env.logger.error("Fail to re-schedule request: Reached Max Times", extra={'data':request.raw_info})
    else:
        _retry = retry+1
        env.logger.error("Rescheduling Request (%s)"% _retry, extra={'data':request.raw_info})
        add_request(request, raw_info={'_retry': _retry})
    if callback: callback(retry,request)

def regis(func=None, key=None, value=None, uid=None, expire=600):
    reg_key = None
    if key is not None:
        reg_key = key
    elif uid is not None:
        reg_key = 'regis:'+uid
    else:
        uid = uuid()
        reg_key = 'regis:'+uid

    r = None
    if value is not None:
        if expire is not None:
            r = env.redis_ins.setex(reg_key, value, expire)
        else:
            r = env.redis_ins.set(reg_key, value)
    elif func is not None:
        r = func(reg_key)
    else:
        r = env.redis_ins.get(reg_key)

    return reg_key, r


def resp_valid(response):
    return True if response and response.status_code==200 else False

def run_worker(worker=None, c_args=None, c_kwargs=None, queue=None, *args, **kwargs):
    if queue is None:
        queue = settings.CELERY_NAME
    if type(worker)!= str:
        worker.apply_async(c_args,c_kwargs, queue=queue, *args, **kwargs)
    else:
        worker = settings.TASKNAME_PREFIX + worker
        env.app.send_task(worker,c_args,c_kwargs, queue=queue, *args, **kwargs)