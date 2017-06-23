from sqlalchemy import ForeignKey, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import backref, relation

from tgext.pluggable import app_model, primary_key

DeclarativeBase = declarative_base()


class Template(DeclarativeBase):
    __tablename__ = 'mailtemplates_templates'

    uid = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(16))
    usage = Column(Unicode())



class TemplateTranslation(DeclarativeBase):
    __tablename__ = 'mailtemplates_translations'

    uid = Column(Integer, autoincrement=True, primary_key=True)

    template_id = Column(Integer, ForeignKey(primary_key(Template)))
    template = relation(Template, backref=backref('translations'))

    language = Column(Unicode())

    subject = Column(Unicode())
    body = Column(Unicode())



