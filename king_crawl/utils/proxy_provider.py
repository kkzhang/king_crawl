# -*- coding: utf-8 -*-
import random
from king_downloader.utils import ProxyProvider, ProxyProvideResult
import requests
from king_crawl.config import settings

__author__ = 'patrickz'

class CustomProxyProvider(ProxyProvider):
    def __init__(self, **kwargs):
        if 'noproxy_rate' in kwargs:
            self.proxy_rate = kwargs['proxy_rate']

    def provide(self):
        rd = random.randint(1,10)
        if rd > getattr(self,'proxy_rate', 0.9)*10:
            return None
        else:
            proxy_url = settings.PROXY_SERVICES_BASE_URL
            resp = requests.get(proxy_url+'/api/v1/proxies/get_one?key='+settings.PROXY_SERVICES_AUTHKEY)
            d = resp.json()['data']
            _r = ProxyProvideResult(d['id'],'http://'+str(d['address'])+':'+str(d['port']))
            return _r

    def callback(self, proxy, result, *args, **kwargs):
        if result:
            r = 1
        else:
            r = -1
        requests.post(settings.PROXY_SERVICES_BASE_URL+'/api/v1/proxies/'+str(proxy.id)+'/rate?key='+settings.PROXY_SERVICES_AUTHKEY,data={'result':str(r)})