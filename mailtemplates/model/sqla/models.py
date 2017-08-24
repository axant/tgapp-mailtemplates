from sqlalchemy import ForeignKey, Column, UnicodeText
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import backref, relation

from tgext.pluggable import app_model, primary_key

DeclarativeBase = declarative_base()


class MailModel(DeclarativeBase):
    __tablename__ = 'mailtemplates_mail_models'

    _id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(128), unique=True, nullable=False)
    usage = Column(UnicodeText(), nullable=False)


class TemplateTranslation(DeclarativeBase):
    __tablename__ = 'mailtemplates_template_translations'

    _id = Column(Integer, autoincrement=True, primary_key=True)

    mail_model_id = Column(Integer, ForeignKey(primary_key(MailModel)))
    mail_model = relation(MailModel, backref=backref('template_translations'))

    language = Column(Unicode(128), nullable=False)

    subject = Column(Unicode(500))
    body = Column(UnicodeText())



