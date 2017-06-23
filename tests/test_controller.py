import tg
from mailtemplates import model
from pyquery import PyQuery as pq
from .base import configure_app, create_app, flush_db_changes
import re

find_urls = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


class MailTemplatesControllerTests(object):
    def setup(self):
        self.app = create_app(self.app_config, False)

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

    # def test_mailtemplates(self):
    #     __, mail_model = model.provider.query(model.MailModel, filter=dict(name=u'Email'))
    #     resp = self.app.get('/mailtemplates')
    #     d = pq(resp.body)
    #     assert d('a').attr.href == '/mail_model?_id=' + str(mail_model[0]._id), d('a').attr.href
    #     assert u'Email' in resp, resp
    #     assert u'Usage' in resp, resp


class TestMailTemplatesControllerSQLA(MailTemplatesControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('sqlalchemy')


class TestMailTemplatesControllerMing(MailTemplatesControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('ming')
