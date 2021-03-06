# -*- coding: utf-8 -*-
import re
import sys

from .loggers import Log

class Dotable(dict):

    __getattr__ = dict.__getitem__

    def __init__(self, d):
        if sys.version_info[:1] == (3,):
            self.update(**dict((k, self.parse(v)) for k, v in d.items()))  # in py3 use .items
        else:
            self.update(**dict((k, self.parse(v)) for k, v in d.iteritems()))

    @classmethod
    def parse(cls, v):
        if isinstance(v, dict):
            return cls(v)
        elif isinstance(v, list):
            return [cls.parse(i) for i in v]
        else:
            return v
