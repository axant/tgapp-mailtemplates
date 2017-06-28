import tg
from tgext.pluggable import app_model

from mailtemplates import model
from pyquery import PyQuery as pq
from .base import configure_app, create_app, flush_db_changes
import re

find_urls = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


class MailTemplatesControllerTests(object):
    def setup(self):
        self.app = create_app(self.app_config, True)

        m1 = model.provider.create(model.MailModel, dict(name=u'Email', usage=u'Usage'))
        model.provider.create(model.TemplateTranslation,
                              dict(language=u'EN', mail_model=m1, subject=u'Subject',
                                   body=u'''Something incredible is waiting to be known! Two ghostly white figures in
                                             coveralls and helmets are soflty dancing kindling the energy hidden in matter?
                                             Cosmos, another world, cosmic ocean! Dream of the mind's eye,Drake Equation,
                                             Orion's sword. Realm of the galaxies, science concept of the number one two ghostly
                                              white figuresin coveralls and helmets are soflty dancing network of wormholes made
                                               in the interiors of collapsing stars, the ash of stellar alchemy billions upon
                                               billions astonishment Tunguska event, finite but unbounded rings of Uranus a very
                                               small stage in a vast cosmic arena? The sky calls to us. White dwarf made in the
                                               interiors of collapsing stars the ash of stellar alchemy, rich in mystery
                                               explorations citizens of distant epochs and billions upon billions upon billions
                                               upon billions upon billions upon billions upon billions.'''))
        flush_db_changes()

    def test_index(self):
        resp = self.app.get('/')
        assert 'HELLO' in resp.text

    def test_mailtemplates(self):
        __, mail_model = model.provider.query(model.MailModel, filter=dict(name=u'Email'))

        mail_model = mail_model[0]

        __, translation = model.provider.query(model.TemplateTranslation, filter=dict(mail_model_id=mail_model._id))
        translation = translation[0]

        resp = self.app.get('/mailtemplates', extra_environ={'REMOTE_USER': 'manager'})

        assert mail_model.name in resp, resp
        assert translation.language in resp, resp
        assert translation.body in resp, resp
        assert translation.subject in resp, resp

    def test_new_translation(self):
        __, mail_model = model.provider.query(model.MailModel, filter=dict(name=u'Email'))

        mail_model = mail_model[0]
        resp = self.app.get('/mailtemplates/new_translation?model_id=' + str(mail_model._id), extra_environ={'REMOTE_USER': 'manager'})
        d = pq(resp.body)
        assert d('#model_id').val() == str(mail_model._id), (d('#model_id').val(), str(mail_model._id))

    def test_edit_translation(self):
        __, mail_model = model.provider.query(model.MailModel, filter=dict(name=u'Email'))

        mail_model = mail_model[0]

        __, translation = model.provider.query(model.TemplateTranslation, filter=dict(mail_model_id=mail_model._id))
        translation = translation[0]

        resp = self.app.get('/mailtemplates/edit_translation?translation_id=' + str(translation._id),
                            extra_environ={'REMOTE_USER': 'manager'})

        d = pq(resp.body)
        assert d('#body').text() == translation.body, (d('#body').text(), translation.body)
        assert d('#subject').val() == translation.subject, (d('#subject').val(), translation.subject)
        assert d('#language').val() == translation.language, (d('#language').val(), translation.language)

    def test_edit_non_existent_translation(self):
        resp = self.app.get('/mailtemplates/edit_translation', params={'translation_id': 2},
                            extra_environ={'REMOTE_USER': 'manager'},
                            status=404)

    def test_create_translation(self):
        __, mail_model = model.provider.query(model.MailModel, filter=dict(name=u'Email'))

        mail_model = mail_model[0]

        resp = self.app.get('/mailtemplates/create_translation', params={'model_id': mail_model._id,
                                                                         'language': 'EN',
                                                                         'body': '<div>This is a body</div>',
                                                                         'subject': 'subject'},
                            extra_environ={'REMOTE_USER': 'manager'},
                            status=302)
        resp = resp.follow(extra_environ={'REMOTE_USER': 'manager'}, status=200)








class TestMailTemplatesControllerSQLA(MailTemplatesControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('sqlalchemy')


class TestMailTemplatesControllerMing(MailTemplatesControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('ming')
