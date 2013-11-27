# -*- coding: utf-8 -*-
__author__ = 'patrickz'

import importlib
from king_crawl.config import global_settings


class Settings(object):
    def __init__(self):
        for setting in dir(global_settings):
            if setting == setting.upper():
                setattr(self, setting, getattr(global_settings, setting))

        mod = importlib.import_module('config.settings')

        for setting in dir(mod):
            if setting == setting.upper():
                setting_value = getattr(mod, setting)
                setattr(self, setting, setting_value)

settings = Settings()