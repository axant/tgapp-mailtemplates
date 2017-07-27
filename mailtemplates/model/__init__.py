# -*- coding: utf-8 -*-
import logging
import tg
from tgext.pluggable import PluggableSession

log = logging.getLogger('tgapp-mailtemplates')

DBSession = PluggableSession()
provider = None

MailModel = None
TemplateTranslation = None


def init_model(app_session):
    DBSession.configure(app_session)


def configure_models():
    global provider, MailModel, TemplateTranslation

    if tg.config.get('use_sqlalchemy', False):
        log.info('Configuring MailTemplates for SQLAlchemy')
        from mailtemplates.model.sqla.models import MailModel, TemplateTranslation
        from sprox.sa.provider import SAORMProvider
        provider = SAORMProvider(session=DBSession, engine=False)
    elif tg.config.get('use_ming', False):
        log.info('Configuring MailTemplates for Ming')
        from mailtemplates.model.ming.models import MailModel, TemplateTranslation
        from sprox.mg.provider import MingProvider
        provider = MingProvider(DBSession)
    else:
        raise ValueError('MailTemplates should be used with sqlalchemy or ming')
