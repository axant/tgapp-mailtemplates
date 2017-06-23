# -*- coding: utf-8 -*-
"""Main Controller"""
import tg
from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate
from tg.decorators import paginate
from tg.i18n import ugettext as _

from mailtemplates import model


class RootController(TGController):

    @expose('kajiki:mailtemplates.templates.index')
    @expose('genshi:mailtemplates.templates.index')
    @paginate('mail_models', items_per_page=tg.config.get('pagination.item_per_page', 20))
    def index(self):
        __, mail_models = model.provider.query(model.MailModel, filters=dict())
        return dict(mail_models=mail_models)

    @expose('kajiki:mailtemplates.templates.index')
    @expose('genshi:mailtemplates.templates.index')
    @paginate('mail_models', items_per_page=tg.config.get('pagination.item_per_page', 20))
    def mail_model(self, id, translation):
        __, mail_models = model.provider.query(model.MailModel, filters=dict())
        return dict(mail_models=mail_models)
