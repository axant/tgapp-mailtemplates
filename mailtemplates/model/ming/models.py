from ming.odm import FieldProperty
from ming.odm import ForeignIdProperty
from ming.odm import MappedClass
from ming.odm import RelationProperty
from mailtemplates.model import DBSession
from ming import schema as s


class MailModel(MappedClass):
    class __mongometa__:
        name = 'mailtemplates_mail_models'
        session = DBSession
        unique_indexes = [('name',)]

    _id = FieldProperty(s.ObjectId)
    name = FieldProperty(s.String, required=True)
    usage = FieldProperty(s.String, required=True)
    template_translations = RelationProperty('TemplateTranslation')


class TemplateTranslation(MappedClass):
    class __mongometa__:
        name = 'mailtemplates_template_translations'
        session = DBSession

    _id = FieldProperty(s.ObjectId)
    mail_model_id = ForeignIdProperty('MailModel')
    mail_model = RelationProperty('MailModel')
    language = FieldProperty(s.String, required=True)
    subject = FieldProperty(s.String)
    body = FieldProperty(s.String)
