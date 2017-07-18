# -*- coding: utf-8 -*-
"""The mailtemplates package"""
from tg.configuration import milestones
from tgext.pluggable import plug
from tgext.pluggable import plugged


def plugme(app_config, options):
    if not 'default_langauge' in options:
        options['default_langauge'] = 'EN'
    app_config['_mailtemplates'] = options

    from mailtemplates import model
    milestones.config_ready.register(model.configure_models)

    if 'tgext.mailer' not in plugged():
        plug(app_config, 'tgext.mailer')

    if 'tgext.asyncjob' not in plugged():
        plug(app_config, 'tgext.asyncjob')

    return dict(appid='mailtemplates', global_helpers=False)
