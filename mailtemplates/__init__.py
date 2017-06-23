# -*- coding: utf-8 -*-
"""The mailtemplates package"""
from tg.configuration import milestones


def plugme(app_config, options):
    app_config['_mailtemplates'] = options

    from mailtemplates import model
    milestones.config_ready.register(model.configure_models)
    milestones.environment_loaded.register(model.configure_provider)
    return dict(appid='mailtemplates', global_helpers=False)
