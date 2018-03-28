# -*- coding: utf-8 -*-

""""
@author: vladdos
@contact: https://vk.com/cryptobot64
@license Apache License, Version 2.0, see LICENSE file
Copyright (C) 2018
"""


from .base import BaseConfig


class MemoryConfig(BaseConfig):
    def load(self, settings=None, **kwargs):
        return {} if settings is None else settings

    def save(self):
        pass