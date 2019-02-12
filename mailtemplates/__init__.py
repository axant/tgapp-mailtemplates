# -*- coding: utf-8 -*-
"""The mailtemplates package"""
import tg
from tg.configuration import milestones
from tgext.pluggable import plug
from tgext.pluggable import plugged


def plugme(app_config, options):
    if 'default_language' not in options:
        options['default_language'] = 'EN'
    if 'async_sender' not in options:
        options.update({'async_sender': 'tgext.asyncjob'})

    try:
        # TG2.3
        app_config['_mailtemplates'] = options
    except TypeError:
        # TG2.4
        app_config.update_blueprint({
            '_mailtemplates': options
        })

    from mailtemplates import model
    milestones.config_ready.register(model.configure_models)

    if 'tgext.mailer' not in plugged(app_config):
        plug(app_config, 'tgext.mailer')

    if options['async_sender'] is None:
        pass
    elif options['async_sender'] == 'tgext.asyncjob':
        if 'tgext.asyncjob' not in plugged(app_config):
            plug(app_config, 'tgext.asyncjob')
    elif options['async_sender'] == 'tgext.celery':
        if 'tgext.celery' not in plugged(app_config):
            raise Exception('please plug and CONFIGURE tgext.celery by yourself')
    else:
        raise Exception('async_sender unknown')

    return dict(appid='mailtemplates', global_helpers=False)
