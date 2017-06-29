import formencode
import kajiki
from formencode.validators import UnicodeString
from tg.i18n import ugettext as _
from tw2.core import ValidationError
from tw2.core import Validator

from mailtemplates import model


class KajikiTemplateValidator(formencode.FancyValidator):

    def _convert_to_python(self, value, state):
        try:
            kajiki.XMLTemplate(unicode(value))
        except:
            raise formencode.Invalid(_('Template not valid.'), value, state)
        return value


class KajikiTextTemplateValidator(formencode.FancyValidator):

    def _convert_to_python(self, value, state):
        try:
            kajiki.TextTemplate(unicode(value))
        except:
            raise formencode.Invalid(_('Template not valid.'), value, state)
        return value


class UniqueLanguageValidator(Validator):

    def __init__(self, mail_model_id_field_name=None, language_field_name=None, **kw):
        super(UniqueLanguageValidator, self).__init__(**kw)
        self.mail_model_id = mail_model_id_field_name
        self.language = language_field_name

    def _validate_python(self, values, state=None):
        mail_model_id = values.get(self.mail_model_id)
        language = values.get(self.language)
        __, templates = model.provider.query(model.TemplateTranslation, filters=dict(mail_model_id=mail_model_id,
                                                                                     language=unicode(language)))
        if templates:
            raise ValidationError(_('Template for this language already created.'))


class UniqueModelNameValidator(UnicodeString):

    def _convert_to_python(self, value, state):
        __, mail_model = model.provider.query(model.MailModel, filters=dict(name=unicode(value)))
        if mail_model:
            raise formencode.Invalid(_('Model with this name already created.'), value, state)
        return value
