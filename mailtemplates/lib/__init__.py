# -*- coding: utf-8 -*-
import tg
from tg import app_globals
from tg import config
from tgext.asyncjob import asyncjob_perform
from tgext.mailer import get_mailer, Message
import kajiki

from mailtemplates import model
from mailtemplates.lib.exceptions import MailTemplatesError
from mailtemplates.lib.template_filler import TemplateFiller, FakeCollect

import dis


def send_email(recipients, sender, mail_model_name, translation=None, data=None, async=False, base_globals=None):
    """
    Method for sending email in this pluggable. Use this method to send your email, specifying the name of a MailModel and
    the language of the email (optionally).
    E.g. send_email('to_addr@example.com', 'no_reply@example.com', 'registration_mail', 'EN')
    If a language is not specified, the default language passed as Plugin option will be used.


    :param recipients: An array representing the email addresss of the recipient of the email
    :param sender: A string representing the email address of the sendere of the email
    :param mail_model_name: The name of the MailModel representing an email
    :param translation: The language of a TemplateTranslation (e.g. 'EN'). If omitted, he default language passed as
        Plugin option will be used.
    :param data: A dictionary representing the variables used in the email template, like ${name}
    :param async: The email will sent asynchronously if this flag is true
    """
    if 'kajiki' not in config['render_functions']:
        raise MailTemplatesError('Kajiki must be allowed in your app.')

    __, mail_models = model.provider.query(model.MailModel, filters=dict(name=mail_model_name))
    if not mail_models:
        raise MailTemplatesError("Mail model '%s' not found." % mail_model_name)
    mail_model = mail_models[0]

    language = translation or config['_mailtemplates']['default_language']

    __, translations = model.provider.query(model.TemplateTranslation, filters=dict(mail_model=mail_model,
                                                                                    language=language))
    if not translations:
        raise MailTemplatesError('Translation for this mail model not found')
    tr = translations[0]

    values = {} if base_globals is None else base_globals.copy()
    values.update(data)

    Template = kajiki.XMLTemplate(source=tr.body)
    Template.loader = tg.config['render_functions']['kajiki'].loader

    html = Template(values)
    html = html.render()

    Template = kajiki.TextTemplate(tr.subject)
    subject = Template(values).render()
    _send_email(sender, recipients, subject, html, async)


def _send_email(sender, recipients, subject, html, async=True):
    mailer = get_mailer(None)
    if not isinstance(recipients, list):
        recipients = list(recipients)

    message_to_send = Message(
        subject=subject,
        sender=sender,
        recipients=recipients,
        html=html
    )
    if async:
        asyncjob_perform(mailer.send_immediately, message=message_to_send)
    else:
        mailer.send_immediately(message_to_send)


def _get_variables_for_template(tmpl):
    global_vars = []
    for elem in dir(tmpl):
        if elem.startswith('_kj_block') or elem == '__main__':
            global_vars += _get_variables_for_block(tmpl, elem)
    return global_vars


def _get_globals_py2(func):
    import opcode
    global_vars = []
    code = func.func_code.co_code
    code_len = len(code)
    i = 0
    while i < code_len:
        op = ord(code[i])
        i += 1
        if op >= opcode.HAVE_ARGUMENT:
            oparg = ord(code[i]) + ord(code[i + 1]) * 256
            i += 2
        if opcode.opname[op] == 'LOAD_GLOBAL':
            varname = func.func_code.co_names[oparg]
            yield varname


def _get_globals_py3(func):
    for o in dis.get_instructions(func):
        if o.opname == 'LOAD_GLOBAL':
            yield o.argval


def _get_variables_for_block(tmpl, blockname):
    no_append = ['len', 'locals']
    f = getattr(tmpl, blockname)._func
    global_vars = []

    if hasattr(dis, 'get_instructions'):
        get_globals = _get_globals_py3
    else:
        get_globals = _get_globals_py2

    for varname in get_globals(f):
        if varname not in tmpl.__globals__ and varname not in no_append:
            global_vars.append(varname)
    return global_vars
