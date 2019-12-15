#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Package wasn't maintained anymore, so it was cloned for this project to
deal with bugs.

Original repo:
https://github.com/divijbindlish/parse-torrent-name

All credits from PTN go to __author__ below.
"""
from .parse import PTN

__author__ = 'Divij Bindlish'
__email__ = 'dvjbndlsh93@gmail.com'
__version__ = '1.1.1'
__license__ = 'MIT'

ptn = PTN()


def parse(name):
    return ptn.parse(name)
