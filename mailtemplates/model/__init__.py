# -*- coding: utf-8 -*-
import logging
import tg
from tgext.pluggable import PluggableSession

log = logging.getLogger('tgapp-mailtemplates')

DBSession = PluggableSession()
provider = None

Template = None
TemplateTranslation = None


def init_model(app_session):
    DBSession.configure(app_session)


def configure_models():
    global provider, Template, TemplateTranslation

    if tg.config.get('use_sqlalchemy', False):
        log.info('Configuring MailTemplates for SQLAlchemy')
        from mailtemplates.model.sqla.models import Template, TemplateTranslation
        from sprox.sa.provider import SAORMProvider
        provider = SAORMProvider(session=DBSession, engine=False)
    elif tg.config.get('use_ming', False):
        log.info('Configuring MailTemplates for Ming')
        from mailtemplates.model.ming.models import Template, TemplateTranslation
        from sprox.mg.provider import MingProvider
        provider = MingProvider(DBSession)
    else:
        raise ValueError('MailTemplates should be used with sqlalchemy or ming')


def configure_provider():
    if tg.config.get('use_sqlalchemy', False):
        provider.engine = DBSession.bind

