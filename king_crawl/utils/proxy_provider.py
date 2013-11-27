# -*- coding: utf-8 -*-
import random
from king_downloader.utils import ProxyProvider, ProxyProvideResult
import requests

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
            resp = requests.get('http://localhost:3000/api/v1/proxies?fail_allow=3')
            d = resp.json()
            _r = ProxyProvideResult(d['id'],'http://'+str(d['address'])+':'+str(d['port']))
            return _r

    def callback(self, proxy, result, *args, **kwargs):
        if result:
            r = 1
        else:
            r = -1
        requests.post('http://localhost:3000/api/v1/proxies/'+str(proxy.id)+"?status="+str(r))