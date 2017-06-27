from ming.odm import FieldProperty
from ming.odm import MappedClass
from ming.odm import RelationProperty
from mailtemplates.model import DBSession
from ming import schema as s


class MailModel(MappedClass):
    class __mongometa__:
        name = 'mailtemplates_mail_models'
        session = DBSession
        indexes = [('name',)]

    _id = FieldProperty(s.ObjectId)
    name = FieldProperty(s.String, required=True)
    usage = FieldProperty(s.String, required=True)


class TemplateTranslation(MappedClass):
    class __mongometa__:
        name = 'mailtemplates_template_translations'
        session = DBSession
        indexes = [()]

    _id = FieldProperty(s.ObjectId)
    mail_models = RelationProperty('MailModel')
    language = FieldProperty(s.String, required=True)
    subject = FieldProperty(s.String)
    body = FieldProperty(s.String)

