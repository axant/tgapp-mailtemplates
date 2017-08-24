from formencode.validators import UnicodeString
from mailtemplates.lib.validator import KajikiTemplateValidator, KajikiTextTemplateValidator, UniqueLanguageValidator, \
    UniqueModelNameValidator
from tw2.forms import HiddenField
from tg.i18n import lazy_ugettext as l_
import tw2.core as twc
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
                    <label for="${c.compound_id}" class="col-md-2 control-label">${c.label}</label>
                    <div class="col-md-2">
                        ${c.display()}
                        <span class="help-block" py:content="c.error_msg"/>
                    </div>
                     <span class="alert alert-danger" py:for="error in w.rollup_errors"> ${error}</span>
                </div>

                <div py:with="c=w.children.subject"
                     class="form-group ${c.error_msg and 'has-error' or ''}">
                    <label for="${c.compound_id}" class="col-md-2 control-label">${c.label}</label>
                    <div class="col-md-10">
                        ${c.display()}
                        <span class="help-block" py:content="c.error_msg"/>
                    </div>
                </div>
                <div py:with="c=w.children.body"
                     class="form-group ${c.error_msg and 'has-error' or ''}">
                    <label for="${c.compound_id}" class="col-md-2 control-label">${c.label}</label>
                    <div class="col-md-10">
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
                            validator=KajikiTextTemplateValidator())

        body = TextArea(label='Email content', rows=10, css_class='form-control',
                        validator=KajikiTemplateValidator())

    validator = UniqueLanguageValidator('model_id', 'language')
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
                    <label for="${c.compound_id}" class="col-md-2 control-label">${c.label}</label>
                    <div class="col-md-2">
                        ${c.display()}
                        <span class="help-block" py:content="c.error_msg"/>
                    </div>
                    <span class="alert alert-danger" py:for="error in w.rollup_errors"> ${error}</span>
                </div>
                <div py:with="c=w.children.subject"
                     class="form-group ${c.error_msg and 'has-error' or ''}">
                    <label for="${c.compound_id}" class="col-md-2 control-label">${c.label}</label>
                    <div class="col-md-10">
                        ${c.display()}
                        <span class="help-block" py:content="c.error_msg"/>
                    </div>
                </div>
                <div py:with="c=w.children.body"
                     class="form-group ${c.error_msg and 'has-error' or ''}">
                    <label for="${c.compound_id}" class="col-md-2 control-label">${c.label}</label>
                    <div class="col-md-10">
                        ${c.display()}
                        <span class="help-block" py:content="c.error_msg"/>
                    </div>
                </div>

            </div>
        </div>

    </div>
     <input type="submit" class="btn btn-warning col-md-1 col-md-push-10" formaction="validate_template_edit" value="Validate"></input>
     <input type="submit" class="btn btn-default" formaction="test_email" value="Send test email"></input>
</div>
'''
        translation_id = HiddenField()
        model_id = HiddenField()
        language = TextField(label='Language', css_class='form-control',
                             validator=UnicodeString(not_empty=True, outputEncoding=None))
        subject = TextField(label='Subject', css_class='form-control',
                            validator=KajikiTextTemplateValidator())

        body = TextArea(label='Email content', rows=10, css_class='form-control',
                        validator=KajikiTemplateValidator())

    validator = UniqueLanguageValidator('model_id', 'language', 'translation_id')
    submit = SubmitButton(css_class='btn btn-primary pull-right btn-edit-translation', value=l_('Save'))


class NewModelForm(Form):
    action = 'create_model'

    class child(BaseLayout):
        inline_engine_name = 'kajiki'

        template = '''

<div py:strip="">
    <py:for each="c in w.children_hidden">
        ${c.display()}
    </py:for>

    <div class="form form-horizontal">
        <div class="form-group">
        <div class="mail-templates-title">New Mail Model</div>
            <div class="col-md-12">
             <div py:with="c=w.children.name"
                     class="form-group ${c.error_msg and 'has-error' or ''}">
                        <label for="${c.compound_id}" class="col-md-2 control-label">${c.label}</label>
                    <div class="col-md-10">
                        ${c.display()}
                        <span class="help-block" py:content="c.error_msg"/>
                    </div>
                </div>
                <div py:with="c=w.children.usage"
                     class="form-group ${c.error_msg and 'has-error' or ''}">
                    <label for="${c.compound_id}" class="col-md-2 control-label">${c.label}</label>
                    <div class="col-md-10">
                        ${c.display()}
                         <span class="help-block" py:content="c.error_msg"/>
                         <span class="help-block"> This is the description of the usage of this new email,
                         including the context of usage. Use this field to explain where and when this mail will be
                            sent in your app. </span>

                    </div>
                </div>
                <div py:with="c=w.children.language"
                     class="form-group ${c.error_msg and 'has-error' or ''}">
                    <label for="${c.compound_id}" class="col-md-2 control-label">${c.label}</label>
                    <div class="col-md-2">
                        ${c.display()}
                        <span class="help-block" py:content="c.error_msg"/>

                    </div>
                </div>
                <div py:with="c=w.children.subject"
                     class="form-group ${c.error_msg and 'has-error' or ''}">
                    <label for="${c.compound_id}" class="col-md-2 control-label">${c.label}</label>
                    <div class="col-md-10">
                        ${c.display()}
                        <span class="help-block" py:content="c.error_msg"/>
                    </div>
                </div>
                <div py:with="c=w.children.body"
                     class="form-group ${c.error_msg and 'has-error' or ''}">
                    <label for="${c.compound_id}" class="col-md-2 control-label">${c.label}</label>
                    <div class="col-md-10">
                        ${c.display()}
                        <span class="help-block" py:content="c.error_msg"/>
                    </div>
                </div>

            </div>
        </div>

    </div>
     <input type="submit" class="btn btn-warning col-md-1 col-md-push-10" formaction="validate_template_model" value="Validate"></input>

</div>
'''
        name = TextField(label='Model Name', css_class='form-control',
                         validator=UniqueModelNameValidator(not_empty=True, outputEncoding=None))
        usage = TextArea(label='Description', css_class='form-control',
                         validator=UnicodeString(not_empty=True, outputEncoding=None))
        language = TextField(label='Language', css_class='form-control',
                             validator=UnicodeString(not_empty=True, outputEncoding=None))
        subject = TextField(label='Subject', css_class='form-control',
                            validator=KajikiTextTemplateValidator())

        body = TextArea(label='Email content', rows=10, css_class='form-control',
                        validator=KajikiTemplateValidator())

    submit = SubmitButton(css_class='btn btn-primary pull-right', value=l_('Create'))


class EditDescriptionForm(Form):
    action = 'update_description'

    class child(BaseLayout):
        inline_engine_name = 'kajiki'

        template = '''

<div py:strip="">
    <py:for each="c in w.children_hidden">
        ${c.display()}
    </py:for>

    <div class="form form-horizontal">
        <div class="form-group">
        <div class="mail-templates-title">Edit model description</div>
            <div class="col-md-12">
             <div py:with="c=w.children.description"
                     class="form-group ${c.error_msg and 'has-error' or ''}">
                    <label for="${c.compound_id}" class="col-md-2 control-label">${c.label}</label>
                    <div class="col-md-10">
                        ${c.display()}
                        <span class="help-block" py:content="c.error_msg"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
'''
        model_id = HiddenField()
        description = TextArea(label='Description', css_class='form-control')

    submit = SubmitButton(css_class='btn btn-primary pull-right', value=l_('Save'))


class TestEmailForm(Form):
    action = 'send_test_email'

    class child(BaseLayout):
        inline_engine_name = 'kajiki'

        template = '''

    <div py:strip="">
        <py:for each="c in w.children_hidden">
            ${c.display()}
        </py:for>

        <div class="form form-horizontal">
            <div class="form-group">
            <div class="mail-templates-title">Send Test Email</div>
                <div class="col-md-12">
                 <div py:with="c=w.children.email"
                         class="form-group ${c.error_msg and 'has-error' or ''}">
                        <label for="${c.compound_id}" class="col-md-2 control-label">${c.label}</label>
                        <div class="col-md-10">
                            ${c.display()}
                            <span class="help-block" py:content="c.error_msg"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''
        translation_id = HiddenField()
        language = HiddenField()
        body = HiddenField()
        subject = HiddenField()
        email = TextField(label='Recipient', css_class='form-control',
                          validator=twc.EmailValidator(not_empty=True))

    submit = SubmitButton(css_class='btn btn-primary pull-right', value=l_('Send'))