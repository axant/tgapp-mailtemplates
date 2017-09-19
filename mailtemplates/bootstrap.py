# -*- coding: utf-8 -*-
"""Setup the mailtemplates application"""
from __future__ import print_function

import transaction

from mailtemplates import model
from tgext.pluggable import app_model


def bootstrap(command, conf, vars):
    print('Bootstrapping mailtemplates...')
    p = app_model.Permission()
    p.permission_name = 'mailtemplates'
    p.description = 'This permission give the mailtemplates admin right'
    __, managers = model.provider.query(app_model.Group, filters=dict(group_name='Managers'))
    if managers:
        p.groups.append(managers[0])
    model.DBSession.add(p)
    app_model.DBSession.flush()
    transaction.commit()
