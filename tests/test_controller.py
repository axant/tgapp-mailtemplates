import tg
from tgext.pluggable import app_model

from mailtemplates import model
from pyquery import PyQuery as pq
from .base import configure_app, create_app, flush_db_changes
import re

find_urls = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


class MailTemplatesControllerTests(object):

    def setup(self):
        self.app = create_app(self.app_config, False)

    def test_index(self):
        resp = self.app.get('/')
        assert 'HELLO' in resp.text


class TestMailTemplatesControllerSQLA(MailTemplatesControllerTests):

    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('sqlalchemy')


class TestMailTemplatesControllerMing(MailTemplatesControllerTests):

    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('ming')