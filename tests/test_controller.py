import tg
import time

from mailtemplates.lib import MailTemplatesError
from mailtemplates.lib import TemplateFiller
from mailtemplates.lib import send_email
from tg.util.webtest import test_context
from tgext.asyncjob.queue import AsyncJobQueue
from tgext.mailer import get_mailer
from tgext.pluggable import app_model

from mailtemplates import model
from pyquery import PyQuery as pq
from .base import configure_app, create_app, flush_db_changes
import re
import mock

find_urls = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


class MailTemplatesControllerTests(object):
    def setup(self):
        self.app = create_app(self.app_config, False)

        m1 = model.provider.create(model.MailModel, dict(name=u'Email', usage=u'Usage'))
        model.provider.create(model.TemplateTranslation, dict(language=u'EN', mail_model=m1, subject=u'Subject',
                                                              body=u'''<div>${body}</div>'''))

        m2 = model.provider.create(model.MailModel, dict(name=u'TranslateEmail', usage=u'Usage'))
        model.provider.create(model.TemplateTranslation, dict(language=u'IT', mail_model=m2, subject=u'Subject',
                                                              body=u'''<py:extends href="mailtemplates.templates.md_rich_email_base">
                                                              <py:block name="a">${mail_title}</py:block>
                                                              altro testo qui dentro
                                                              </py:extends>'''))
        model.provider.create(model.TemplateTranslation, dict(language=u'EN', mail_model=m2, subject=u'soggetto',
                                                              body=u'''<div><py:block name="a">${mail_title}</py:block>
                                                              other text
                                                              </div>'''))

        flush_db_changes()
        self.body_formatted = "&lt;div&gt;${body}&lt;/div&gt;"

    def test_index(self):
        resp = self.app.get('/')
        assert 'HELLO' in resp.text

    def test_mailtemplates(self):
        __, mail_model = model.provider.query(model.MailModel, filters=dict(name=u'Email'))
        mail_model = mail_model[0]
        __, translation = model.provider.query(model.TemplateTranslation,
                                               filters=dict(mail_model_id=mail_model._id))
        translation = translation[0]
        resp = self.app.get('/mailtemplates', extra_environ={'REMOTE_USER': 'manager'})
        assert mail_model.name in resp, resp
        assert translation.language in resp, resp
        assert self.body_formatted in resp, resp
        assert translation.subject in resp, resp

    def test_new_translation(self):
        __, mail_model = model.provider.query(model.MailModel, filters=dict(name=u'Email'))
        mail_model = mail_model[0]
        resp = self.app.get('/mailtemplates/new_translation?model_id=' + str(mail_model._id),
                            extra_environ={'REMOTE_USER': 'manager'})
        d = pq(resp.body)
        assert d('#model_id').val() == str(mail_model._id), (d('#model_id').val(), str(mail_model._id))

    def test_edit_translation(self):
        __, mail_model = model.provider.query(model.MailModel, filters=dict(name=u'Email'))
        mail_model = mail_model[0]
        __, translation = model.provider.query(model.TemplateTranslation,
                                               filters=dict(mail_model_id=mail_model._id))
        translation = translation[0]
        resp = self.app.get('/mailtemplates/edit_translation?translation_id=' + str(translation._id),
                            extra_environ={'REMOTE_USER': 'manager'})

        d = pq(resp.body)
        assert d('#body').text() == translation.body, (d('#body').text(), translation.body)

        assert d('#subject').val() == translation.subject, (d('#subject').val(), translation.subject)

        assert d('#language').val() == translation.language, (d('#language').val(), translation.language)

    def test_edit_non_existent_translation(self):
        resp = self.app.get('/mailtemplates/edit_translation', params={'translation_id': 999},
                            extra_environ={'REMOTE_USER': 'manager'},
                            status=404)

    def test_create_translation(self):
        __, mail_model = model.provider.query(model.MailModel, filters=dict(name=u'Email'))

        mail_model = mail_model[0]

        resp = self.app.get('/mailtemplates/create_translation', params={'model_id': mail_model._id,
                                                                         'language': 'IT',
                                                                         'body': '<div>This is a body</div>',
                                                                         'subject': 'my_subject'},
                            extra_environ={
                                'REMOTE_USER': 'manager'}, status=302)
        resp = resp.follow(extra_environ={'REMOTE_USER': 'manager'}, status=200)

        __, translation = model.provider.query(model.TemplateTranslation, filters={'subject': 'my_subject'})

        assert translation, translation

    def test_create_translation_no_model(self):
        resp = self.app.get('/mailtemplates/create_translation', params={'model_id': 100,
                                                                         'language': 'JR',
                                                                         'body': '<div>This is a body</div>',
                                                                         'subject': 'subject'},
                            extra_environ={
                                'REMOTE_USER': 'manager'}, status=404)

    def test_update_translation(self):
        __, translation = model.provider.query(model.TemplateTranslation,
                                               filters=dict(subject=u'Subject'))

        translation = translation[0]

        resp = self.app.get('/mailtemplates/update_translation', params={'translation_id': translation._id,
                                                                         'language': 'EN',
                                                                         'subject': 'Subject'},
                            extra_environ={
                                'REMOTE_USER': 'manager'}, status=302)
        resp = resp.follow(extra_environ={'REMOTE_USER': 'manager'}, status=200)
        __, translation = model.provider.query(model.TemplateTranslation, filters={'_id': translation._id})

        assert translation, translation

    def test_update_translation_no_translation(self):
        resp = self.app.get('/mailtemplates/update_translation', params={'translation_id': 200},
                            extra_environ={
                                'REMOTE_USER': 'manager'}, status=404)

    def test_update_translation_already_in(self):
        __, mail_model = model.provider.query(model.MailModel, filters=dict(name=u'Email'))

        mail_model = mail_model[0]
        model.provider.create(model.TemplateTranslation,
                              dict(language=u'FR',
                                   mail_model=mail_model,
                                   subject=u'sub',
                                   body=u'''<div></div>'''))
        flush_db_changes()

        __, translation = model.provider.query(model.TemplateTranslation,
                                               filters=dict(subject=u'Subject'))
        translation = translation[0]

        resp = self.app.get('/mailtemplates/update_translation',
                            params={'translation_id': translation._id,
                                    'body': '<div>This is a body</div>',
                                    'language': 'FR',
                                    'subject': 'Subject'},
                            extra_environ={
                                'REMOTE_USER': 'manager'}, status=302)
        resp = resp.follow(extra_environ={'REMOTE_USER': 'manager'})

    def test_new_model(self):
        resp = self.app.get('/mailtemplates/new_model', extra_environ={'REMOTE_USER': 'manager'},
                            status=200)

        assert tg.config['_mailtemplates']['default_language'] in resp, resp

    def test_create_model(self):
        resp = self.app.get('/mailtemplates/create_model', params={'name': u'Model', 'usage': 'usage1',
                                                                   'language': 'IT',
                                                                   'body': '<div>This is a body</div>',
                                                                   'subject': 'subject'},
                            extra_environ={'REMOTE_USER': 'manager'}, status=302)
        resp = resp.follow(extra_environ={'REMOTE_USER': 'manager'}, status=200)

        __, mail_model = model.provider.query(model.MailModel, filters={'name': u'Model', 'usage': 'usage1'})

        assert mail_model[0].name == 'Model', mail_model[0].name

    def test_test_email(self):
        __, translation = model.provider.query(model.TemplateTranslation,
                                               filters=dict(language='EN'))
        translation = translation[0]
        resp = self.app.get('/mailtemplates/test_email', params=dict(translation_id=translation._id, language='EN'),
                            extra_environ={'REMOTE_USER': 'manager'}, status=200)
        assert 'Send Test Email' in resp, resp

    def test_send_test_email(self):
        with test_context(self.app):
            app_globals = tg.app_globals._current_obj()

            __, translation = model.provider.query(model.TemplateTranslation,
                                                   filters=dict(language='EN'))
            translation = translation[0]

            resp = self.app.get('/mailtemplates/send_test_email',
                                params=dict(translation_id=translation._id, language=translation.language,
                                            body=translation.body, subject=translation.subject,
                                            email='marco.bosio@axant.it'),
                                extra_environ={'REMOTE_USER': 'manager'}, status=200)
            assert 'Test email sent to marco.bosio@axant.it' in resp, resp
            assert app_globals.asyncjob_queue.queue.qsize() > 0, app_globals.asyncjob_queue.queue.qsize()

    def test_edit_description(self):
        __, mail_model = model.provider.query(model.MailModel, filters=dict(name=u'Email'))
        mail_model = mail_model[0]
        resp = self.app.get('/mailtemplates/edit_description', params={'model_id': mail_model._id},
                            extra_environ={'REMOTE_USER': 'manager'}, status=200)

    def test_edit_description_no_model(self):
        resp = self.app.get('/mailtemplates/edit_description', params={'model_id': 200},
                            extra_environ={'REMOTE_USER': 'manager'}, status=404)

    def test_update_description(self):
        __, mail_model = model.provider.query(model.MailModel, filters=dict(name=u'Email'))
        mail_model = mail_model[0]
        resp = self.app.get('/mailtemplates/update_description', params={'model_id': mail_model._id,
                                                                         'description': 'new description'},
                            extra_environ={'REMOTE_USER': 'manager'}, status=302)
        resp = resp.follow(extra_environ={'REMOTE_USER': 'manager'}, status=200)
        assert 'Model description edited.' in resp, resp
        __, mail_model = model.provider.query(model.MailModel, filters=dict(name=u'Email'))
        mail_model = mail_model[0]
        assert mail_model.usage == 'new description', mail_model.usage

    def test_update_description_no_desc(self):
        resp = self.app.get('/mailtemplates/update_description', params={'model_id': 200,
                                                                         'description': 'new description'},
                            extra_environ={'REMOTE_USER': 'manager'}, status=404)

    def test_validate_template(self):
        resp = self.app.get('/mailtemplates/validate_template', params={'language': 'EN',
                                                                        'body': '<div>${body}</div>'},
                            extra_environ={'REMOTE_USER': 'manager'}, status=200)

    def test_validate_template_edit(self):
        resp = self.app.get('/mailtemplates/validate_template_edit', params={'language': 'EN',
                                                                             'body': '<div>${body}</div>'},
                            extra_environ={'REMOTE_USER': 'manager'}, status=200)

    def test_validate_template_model(self):
        resp = self.app.get('/mailtemplates/validate_template_model', params={'language': 'EN',
                                                                              'body': '<div>${body}</div>',
                                                                              'name': 'name',
                                                                              'usage': 'usage'},
                            extra_environ={'REMOTE_USER': 'manager'}, status=200)

    def test_send_email_async(self):
        with test_context(self.app):
            app_globals = tg.app_globals._current_obj()

            __, mail_model = model.provider.query(model.MailModel, filters=dict(name=u'Email'))
            mail_model = mail_model[0]
            send_email(recipients=['marco.bosio@axant.it'], sender='Marco Bosio <mbosioke@gmail.com>',
                       mail_model_name=mail_model.name, data=dict(body='body'), send_async=True
                       )
            assert app_globals.asyncjob_queue.queue.qsize() > 0, app_globals.asyncjob_queue.queue.qsize()

    @mock.patch('mailtemplates.lib._get_request', return_value=None)
    def test_send_email(self, _):
        with test_context(self.app):
            app_globals = tg.app_globals._current_obj()
            mailer = get_mailer(app_globals)

            __, mail_model = model.provider.query(model.MailModel, filters=dict(name=u'Email'))
            mail_model = mail_model[0]
            send_email(recipients=['marco.bosio@axant.it'], sender='Marco Bosio <mbosioke@gmail.com>',
                       mail_model_name=mail_model.name, data=dict(body='body'))
            assert len(mailer.outbox) > 0, mailer.outbox

    @mock.patch('mailtemplates.lib._get_request', return_value=None)
    def test_send_email_recipients_not_list(self, _):
        with test_context(self.app):
            app_globals = tg.app_globals._current_obj()
            mailer = get_mailer(app_globals)

            __, mail_model = model.provider.query(model.MailModel, filters=dict(name=u'Email'))
            mail_model = mail_model[0]
            send_email(recipients='marco.bosio@axant.it', sender='Marco Bosio <mbosioke@gmail.com>',
                       mail_model_name=mail_model.name, data=dict(body='body'))
            assert len(mailer.outbox) > 0, mailer.outbox

    def test_send_email_no_model(self):
        try:
            send_email(recipients=['marco.bosio@axant.it'], sender='Marco Bosio <mbosioke@gmail.com>',
                       mail_model_name='No model', data=dict(body='body'))
        except MailTemplatesError as e:
            assert 'Mail model \'No model\' not found' in str(e)

    def test_send_email_no_translation(self):
        try:
            __, mail_model = model.provider.query(model.MailModel, filters=dict(name=u'Email'))
            mail_model = mail_model[0]
            send_email(recipients=['marco.bosio@axant.it'], sender='Marco Bosio <mbosioke@gmail.com>',
                       mail_model_name=mail_model.name, translation='RU', data=dict(body='body'))
        except MailTemplatesError as e:
            assert 'Translation for this mail model not found' in str(e)

    def test_template_filler(self):
        t = TemplateFiller(name='name')
        assert str(t.prop) == 'prop', t.prop
        assert str(t['attr']) == 'attr', t['attr']

    @mock.patch('mailtemplates.lib._get_request', return_value=None)
    def test_kajiki_with_context(self, _):
        with test_context(self.app):
            send_email(
                recipients=['marco.bosio@axant.it'],
                sender='Marco Bosio <mbosioke@gmail.com>',
                translation='IT',
                mail_model_name=u'TranslateEmail',
                data=dict(body='body', mail_title='titolo mail'),
              send_async=False,
            )

    def test_kajiki_with_context_async(self):
        # tgext.asyncjob can't start an asyncjob without a context.
        with test_context(self.app):
            send_email(
                recipients=['marco.bosio@axant.it'],
                sender='Marco Bosio <mbosioke@gmail.com>',
                translation='IT',
                mail_model_name=u'TranslateEmail',
                data=dict(body='body', mail_title='titolo mail'),
              send_async=True
            )

    # TODO: test tgext.celery integration:


class TestMailTemplatesControllerSQLA(MailTemplatesControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('sqlalchemy')


class TestMailTemplatesControllerMing(MailTemplatesControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('ming')
