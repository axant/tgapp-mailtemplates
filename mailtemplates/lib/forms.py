from formencode.validators import UnicodeString
from mailtemplates.lib.validator import KajikiTemplateValidator
from tg import lurl
from tw2.forms import HiddenField, ListForm, TextField, TextArea, SubmitButton
from tg.i18n import lazy_ugettext as l_
import tw2.forms as twf

from tw2.core import Validator
from tw2.forms.widgets import Form, BaseLayout, TextField, TextArea, SubmitButton



class CreateTranslationForm(Form):
    action = 'create_translation'

    class child(BaseLayout):
        inline_engine_name = 'kajiki'

        template = '''
<div py:strip="">
    <py:for each="c in w.children_hidden">
        ${c.display()}
    </py:for>

    <div class="form form-horizontal">
     <div class="mail-templates-title">New mail translation</div>
        <div class="form-group">
            <div class="col-md-12">
                <div py:with="c=w.children.language"
                     class="form-group ${c.error_msg and 'has-error' or ''}">
                    <label for="${c.compound_id}" class="col-md-3 control-label">${c.label}</label>
                    <div class="col-md-2">
                        ${c.display()}
                        <span class="help-block" py:content="c.error_msg"/>
                    </div>
                </div>
                <div py:with="c=w.children.subject"
                     class="form-group ${c.error_msg and 'has-error' or ''}">
                    <label for="${c.compound_id}" class="col-md-3 control-label">${c.label}</label>
                    <div class="col-md-9">
                        ${c.display()}
                        <span class="help-block" py:content="c.error_msg"/>
                    </div>
                </div>
                <div py:with="c=w.children.body"
                     class="form-group ${c.error_msg and 'has-error' or ''}">
                    <label for="${c.compound_id}" class="col-md-3 control-label">${c.label}</label>
                    <div class="col-md-9">
                        ${c.display()}
                        <span class="help-block" py:content="c.error_msg"/>
                    </div>
                </div>

            </div>
        </div>

    </div>
     <input type="submit" class="btn btn-warning col-md-1 col-md-push-10" formaction="validate_template" value="Validate"></input>

</div>
'''
        model_id = HiddenField()
        language = TextField(label='Language', css_class='form-control',
                             validator=UnicodeString(not_empty=True, outputEncoding=None))
        subject = TextField(label='Subject', css_class='form-control',
                            validator=UnicodeString(outputEncoding=None))

        body = TextArea(label='Email content', rows=10, css_class='form-control',
                        validator=KajikiTemplateValidator())

    submit = SubmitButton(css_class='btn btn-primary pull-right', value=l_('Create'))


class EditTranslationForm(Form):
    action = 'update_translation'

    class child(BaseLayout):
        inline_engine_name = 'kajiki'

        template = '''

<div py:strip="">
    <py:for each="c in w.children_hidden">
        ${c.display()}
    </py:for>

    <div class="form form-horizontal">
        <div class="form-group">
        <div class="mail-templates-title">Edit mail translation</div>
            <div class="col-md-12">
                <div py:with="c=w.children.language"
                     class="form-group ${c.error_msg and 'has-error' or ''}">
                    <label for="${c.compound_id}" class="col-md-3 control-label">${c.label}</label>
                    <div class="col-md-2">
                        ${c.display()}
                        <span class="help-block" py:content="c.error_msg"/>
                    </div>
                </div>
                <div py:with="c=w.children.subject"
                     class="form-group ${c.error_msg and 'has-error' or ''}">
                    <label for="${c.compound_id}" class="col-md-3 control-label">${c.label}</label>
                    <div class="col-md-9">
                        ${c.display()}
                        <span class="help-block" py:content="c.error_msg"/>
                    </div>
                </div>
                <div py:with="c=w.children.body"
                     class="form-group ${c.error_msg and 'has-error' or ''}">
                    <label for="${c.compound_id}" class="col-md-3 control-label">${c.label}</label>
                    <div class="col-md-9">
                        ${c.display()}
                        <span class="help-block" py:content="c.error_msg"/>
                    </div>
                </div>

            </div>
        </div>

    </div>
     <input type="submit" class="btn btn-warning col-md-1 col-md-push-10" formaction="validate_template_edit    " value="Validate"></input>

</div>
'''
        translation_id = HiddenField()
        language = TextField(label='Language', css_class='form-control',
                             validator=UnicodeString(not_empty=True, outputEncoding=None))
        subject = TextField(label='Subject', css_class='form-control',
                            validator=UnicodeString(outputEncoding=None))

        body = TextArea(label='Email content', rows=10, css_class='form-control',
                        validator=KajikiTemplateValidator())

    submit = SubmitButton(css_class='btn btn-primary pull-right btn-edit-translation', value=l_('Edit'))