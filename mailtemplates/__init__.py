# -*- coding: utf-8 -*-
"""The mailtemplates package"""
from tg.configuration import milestones
from tgext.pluggable import plug
from tgext.pluggable import plugged


def plugme(app_config, options):
    app_config['_mailtemplates'] = options

    from mailtemplates import model
    milestones.config_ready.register(model.configure_models)

    if 'tgext.mailer' not in plugged():
        plug(app_config, 'tgext.mailer')

    return dict(appid='mailtemplates', global_helpers=False)
