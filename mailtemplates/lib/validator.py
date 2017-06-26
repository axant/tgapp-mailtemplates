import formencode
import kajiki
from tg.i18n import ugettext as _


class KajikiTemplateValidator(formencode.FancyValidator):

    def _convert_to_python(self, value, state):
        try:
            kajiki.XMLTemplate(unicode(value))
        except:
            raise formencode.Invalid(_('Template not valid.'), value, state)
        return value
