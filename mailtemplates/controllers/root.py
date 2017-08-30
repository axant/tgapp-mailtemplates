# -*- coding: utf-8 -*-
"""Main Controller"""
import tg
from mailtemplates.lib import TemplateFiller, _get_variables_for_template, FakeCollect
from tg import predicates
import kajiki as kj

from mailtemplates.lib import MailTemplatesError
from mailtemplates.lib import _send_email
from tg import TGController
from tg import config
from tg import expose, url, redirect, validate
from tg.decorators import paginate
from tg.i18n import ugettext as _
from mailtemplates.lib.forms import CreateTranslationForm, EditTranslationForm, NewModelForm, TestEmailForm, \
    EditDescriptionForm

from mailtemplates import model


class RootController(TGController):
    allow_only = predicates.has_permission('mailtemplates')

    @expose('kajiki:mailtemplates.templates.index')
    @expose('genshi:mailtemplates.templates.index')
    def index(self):
        __, mail_models = model.provider.query(model.MailModel, filters=dict())
        return dict(mail_models=mail_models)

    @expose('kajiki:mailtemplates.templates.new_translation')
    @expose('genshi:mailtemplates.templates.new_translation')
    def new_translation(self, model_id, **kwargs):
        return dict(form=CreateTranslationForm, values=dict(model_id=model_id))

    @expose('kajiki:mailtemplates.templates.new_translation')
    @expose('genshi:mailtemplates.templates.new_translation')
    def edit_translation(self, translation_id, **kwargs):
        __, translations = model.provider.query(model.TemplateTranslation, filters=dict(_id=translation_id))
        if not translations:
            return tg.abort(404)
        translation = translations[0]
        return dict(form=EditTranslationForm, values=dict(translation_id=translation._id,
                                                            language=translation.language,
                                                            subject=translation.subject,
                                                            body=translation.body,
                                                          model_id=translation.mail_model_id))

    @expose()
    @validate(CreateTranslationForm, error_handler=new_translation)
    def create_translation(self, **kwargs):
        __, mail_models = model.provider.query(model.MailModel, filters=dict(_id=kwargs.get('model_id')))
        if not mail_models:
            return tg.abort(404)
        mail_model = mail_models[0]
        new_translation = model.provider.create(model.TemplateTranslation, dict(language=kwargs.get('language'),
                                                                                mail_model=mail_model,
                                                                                subject=kwargs.get('subject'),
                                                                                body=kwargs.get('body')))
        tg.flash(_('Translation created.'))
        return redirect(url('index'))

    @expose()
    @validate(EditTranslationForm, error_handler=edit_translation)
    def update_translation(self, **kwargs):
        __, translations = model.provider.query(model.TemplateTranslation, filters=dict(_id=kwargs.get('translation_id')))
        if not translations:
            return tg.abort(404)
        translation = translations[0]
        translation.language = kwargs.get('language')
        translation.subject = kwargs.get('subject')
        translation.body = kwargs.get('body')
        model.provider.flush()
        tg.flash(_('Translation edited.'))
        return redirect(url('index'))

    @expose('kajiki:mailtemplates.templates.new_model')
    @expose('genshi:mailtemplates.templates.new_model')
    def new_model(self, **kwargs):
        default_language = config['_mailtemplates']['default_language']
        return dict(form=NewModelForm, values=dict(language=default_language))


    @expose()
    @validate(NewModelForm, error_handler=new_model)
    def create_model(self, **kwargs):
        mail_model = model.provider.create(model.MailModel, dict(name=kwargs.get('name'), usage=kwargs.get('usage')))
        new_translation = model.provider.create(model.TemplateTranslation, dict(language=kwargs.get('language'),
                                                                                mail_model=mail_model,
                                                                                subject=kwargs.get('subject'),
                                                                                body=kwargs.get('body')))
        tg.flash(_('Model created.'))
        return redirect(url('index'))

    @expose('kajiki:mailtemplates.templates.test_email')
    @expose('genshi:mailtemplates.templates.test_email')
    @validate(EditTranslationForm, error_handler=edit_translation)
    def test_email(self, **kwargs):
        return dict(form=TestEmailForm, values=kwargs)

    @expose('kajiki:mailtemplates.templates.new_translation')
    @expose('genshi:mailtemplates.templates.new_translation')
    @validate(TestEmailForm, error_handler=test_email)
    def send_test_email(self, **kwargs):
        if 'kajiki' not in config['render_functions']:
            raise MailTemplatesError('Kajiki must be allowed in your app.')

        body = kwargs.get('body')
        subject = kwargs.get('subject').replace('$', '$$')

        Template = kj.XMLTemplate(body)
        Template.loader = tg.config['render_functions']['kajiki'].loader

        t = Template()
        t.__kj__.collect = FakeCollect(t)
        for v in _get_variables_for_template(t):
            t.__globals__[v] = TemplateFiller(v)
        html = t.render()
        _send_email(recipients=[kwargs.get('email')], sender=tg.config.get('mail.username', 'no-reply@axantweb.com'),
                    subject=subject, html=html)
        tg.flash(_('Test email sent to %s' % kwargs.get('email')))
        return dict(form=EditTranslationForm, values=kwargs)

    @expose('kajiki:mailtemplates.templates.edit_description')
    @expose('genshi:mailtemplates.templates.edit_description')
    def edit_description(self, **kwargs):
        __, mail_models = model.provider.query(model.MailModel, filters=dict(_id=kwargs.get('model_id')))
        if not mail_models:
            return tg.abort(404)
        mail_model = mail_models[0]

        return dict(form=EditDescriptionForm, values={'model_id': kwargs.get('model_id'),
                                                      'description': mail_model.usage})

    @expose()
    @validate(EditDescriptionForm, error_handler=edit_description)
    def update_description(self, **kwargs):
        __, mail_models = model.provider.query(model.MailModel,filters=dict(_id=kwargs.get('model_id')))
        if not mail_models:
            return tg.abort(404)
        mail_model = mail_models[0]
        mail_model.usage = kwargs.get('description')
        model.provider.flush()
        tg.flash(_('Model description edited.'))
        return redirect(url('index'))


    @expose('kajiki:mailtemplates.templates.new_translation')
    @expose('genshi:mailtemplates.templates.new_translation')
    @validate(CreateTranslationForm, error_handler=new_translation)
    def validate_template(self, **kwargs):
        tg.flash("Email template valid.")
        return dict(form=CreateTranslationForm, values=kwargs)

    @expose('kajiki:mailtemplates.templates.new_translation')
    @expose('genshi:mailtemplates.templates.new_translation')
    @validate(EditTranslationForm, error_handler=edit_translation)
    def validate_template_edit(self, **kwargs):
        tg.flash("Email template valid.")
        return dict(form=EditTranslationForm, values=kwargs)

    @expose('kajiki:mailtemplates.templates.new_translation')
    @expose('genshi:mailtemplates.templates.new_translation')
    @validate(NewModelForm, error_handler=new_model)
    def validate_template_model(self, **kwargs):
        tg.flash("Email template valid.")
        return dict(form=NewModelForm, values=kwargs)
