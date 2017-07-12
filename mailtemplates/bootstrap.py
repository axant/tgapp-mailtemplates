# -*- coding: utf-8 -*-
"""Setup the mailtemplates application"""
from __future__ import print_function

from mailtemplates import model
from tgext.pluggable import app_model


def bootstrap(command, conf, vars):
    print('Bootstrapping mailtemplates...')