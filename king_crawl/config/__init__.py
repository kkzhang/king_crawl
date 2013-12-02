# -*- coding: utf-8 -*-
import os

__author__ = 'patrickz'

import importlib
from king_crawl.config import global_settings


class Settings(object):
    def __init__(self):
        for setting in dir(global_settings):
            if setting == setting.upper():
                setattr(self, setting, getattr(global_settings, setting))
        self.load_settings('config.settings')

        extra_settings = os.getenv('KING_CRAWL_SETTINGS')
        if extra_settings:
            self.load_settings(extra_settings)

    def load_settings(self, module):
        mod = importlib.import_module(module)

        for setting in dir(mod):
            if setting == setting.upper():
                setting_value = getattr(mod, setting)
                setattr(self, setting, setting_value)

settings = Settings()