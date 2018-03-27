import bson
from tgext.asyncjob.queue import AsyncJobQueue
from webtest import TestApp
import transaction

from tg import AppConfig, config
from tg.configuration import milestones
from tg.configuration.auth import TGAuthMetadata
from tgext.pluggable import plug, app_model

from sqlalchemy import Integer, Column, Unicode, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy import event

import ming
from ming import Session
from ming.odm import ThreadLocalODMSession
from ming.odm.declarative import MappedClass
from ming.odm import FieldProperty
from ming import schema as s


class FakeAppPackage(object):
    __file__ = __file__
    __name__ = 'tests'

    class lib(object):
        class helpers(object):
            pass
        helpers = helpers()

        class app_globals(object):
            class Globals():
                asyncjob_queue= AsyncJobQueue()

        app_globals = app_globals()

    class websetup(object):
        def bootstrap(*args, **kwargs):
            pass


class FakeSQLAModel(object):
    def __init__(self):
        self.DeclarativeBase = declarative_base()
        self.DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False,
                                                     extension=ZopeTransactionExtension()))

        class User(self.DeclarativeBase):
            __tablename__ = 'tg_user'

            user_id = Column(Integer, autoincrement=True, primary_key=True)
            user_name = Column(Unicode(16), unique=True, nullable=False)
            email_address = Column(Unicode(255), unique=True, nullable=False)
            display_name = Column(Unicode(255))
            password = Column(Unicode(255), nullable=False)

        self.User = User

    def init_model(self, engine):
        self.DBSession.configure(bind=engine)
        self.DeclarativeBase.metadata.drop_all(engine)
        self.DeclarativeBase.metadata.create_all(bind=engine)


class FakeMingModel(object):
    def __init__(self):
        self.ming_session = Session()
        self.DBSession = ThreadLocalODMSession(self.ming_session)

        class User(MappedClass):
            class __mongometa__:
                session = self.DBSession
                name = 'tg_user'
                unique_indexes = [('user_name',), ('email_address',)]

            _id = FieldProperty(s.ObjectId)
            user_name = FieldProperty(s.String)
            email_address = FieldProperty(s.String)
            display_name = FieldProperty(s.String)
            password = FieldProperty(s.String)

        self.User = User

    def init_model(self, datastore):
        self.ming_session.bind = datastore

        try:
            # On MIM drop all data
            datastore.conn.drop_all()
        except TypeError:
            # On MongoDB drop database
            datastore.conn.drop_database(datastore.db)

        ming.odm.Mapper.compile_all()
        for mapper in ming.odm.Mapper.all_mappers():
            self.ming_session.ensure_indexes(mapper.collection)


class FakeUser(bson.ObjectId):
    """
    Fake user that emulates an users without the need to actually
    query it from the database
    """
    def __int__(self):
        return 1

    def __getattr__(self, item):
        if item == 'user_id':
            return 1
        elif item == '_id':
            return self
        return super(FakeUser, self).__getattr__(item)


class TestAuthMetadata(TGAuthMetadata):
    def authenticate(self, environ, identity):
        return 'manager'

    def get_user(self, identity, userid):
        if userid:
            return FakeUser()

    def get_groups(self, identity, userid):
        if userid:
            return ['managers']
        return []

    def get_permissions(self, identity, userid):
        if userid:
            return ['mailtemplates']
        return []

def configure_app(using):
    # Simulate starting configuration process from scratch
    milestones._reset_all()

    app_cfg = AppConfig(minimal=True)
    app_cfg.renderers = ['kajiki']
    app_cfg.default_renderer = 'kajiki'
    app_cfg.use_dotted_templatenames = True
    app_cfg.package = FakeAppPackage()
    app_cfg.use_toscawidgets2 = True
    app_cfg.sa_auth.authmetadata = TestAuthMetadata()
    app_cfg['beaker.session.secret'] = app_cfg['session.secret'] = 'SECRET'
    app_cfg.auth_backend = 'ming'
    app_cfg['mail.debugmailer'] = "dummy"

    if using == 'sqlalchemy':
        app_cfg.package.model = FakeSQLAModel()
        app_cfg.use_sqlalchemy = True
        app_cfg['sqlalchemy.url'] = 'sqlite://'
        app_cfg.use_transaction_manager = True
        app_cfg.SQLASession = app_cfg.package.model.DBSession
    elif using == 'ming':
        app_cfg.package.model = FakeMingModel()
        app_cfg.use_ming = True
        app_cfg['ming.url'] = 'mim:///mailtemapltes'
        app_cfg.MingSession = app_cfg.package.model.DBSession
    else:
        raise ValueError('Unsupported backend')

    app_cfg.model = app_cfg.package.model
    app_cfg.DBSession = app_cfg.package.model.DBSession

    # Guarantee that the same form is used between multiple
    # configurations of TGApps. Otherwise the validated
    # form would be different from the displayed one.

    plug(app_cfg, 'tgext.mailer', plug_bootstrap=True, debugmailer='dummy')
    plug(app_cfg, 'tgext.asyncjob', plug_bootstrap=True, app_globals=app_cfg['app_globals'])
    # it is important that tgext.mailer and tgext.asyncjob are plugged
    # before mailtemplates or not plugged at all as mailtemplates plugs them
    plug(app_cfg, 'mailtemplates', plug_bootstrap=True, default_language='EN')
    return app_cfg


def create_app(app_config, auth=False):
    app = app_config.make_wsgi_app(skip_authentication=True)

    if auth:
        app = TestApp(app, extra_environ=dict(REMOTE_USER='manager'))
    else:
        app = TestApp(app)

    app.get('/non_existing_url_force_app_config_update', status=404)
    return app


def flush_db_changes():
    app_model.DBSession.flush()
    transaction.commit()
