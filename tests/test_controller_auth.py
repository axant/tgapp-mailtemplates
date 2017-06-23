from .base import configure_app, create_app
import re

find_urls = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


class MailTemplatesAuthControllerTests(object):
    def setup(self):
        self.app = create_app(self.app_config, True)

class TestMailTemplatesAuthControllerSQLA(MailTemplatesAuthControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('sqlalchemy')


class TestMailTemplatesAuthControllerMing(MailTemplatesAuthControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('ming')

