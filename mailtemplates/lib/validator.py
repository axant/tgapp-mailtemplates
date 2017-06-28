import formencode
import kajiki
from formencode.validators import UnicodeString
from tg.i18n import ugettext as _

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


class UniqueLanguageValidator(UnicodeString):

    def _convert_to_python(self, value, state):
        __, templates = model.provider.query(model.TemplateTranslation, filters=dict(language=unicode(value)))
        if templates:
            raise formencode.Invalid(_('Template for this language already created.'), value, state)
        return value