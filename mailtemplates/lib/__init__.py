# -*- coding: utf-8 -*-
import tg
from tg import app_globals
from tg import config
from tgext.mailer import get_mailer, Message
import kajiki

from mailtemplates import model
from mailtemplates.lib.exceptions import MailTemplatesError
from mailtemplates.lib.template_filler import TemplateFiller, FakeCollect

import logging

import dis


log = logging.getLogger(__name__)


def send_email(
    recipients, 
    sender, 
    mail_model_name,
    cc=None,
    translation=None, 
    data=None, 
    send_async=False
):
    """
    Method for sending email in this pluggable. Use this method to send your email, specifying
    the name of a MailModel and the language of the email (optionally).
    E.g. send_email('to_addr@example.com', 'no_reply@example.com', 'registration_mail', 'EN')
    If a language is not specified, the default language passed as Plugin option will be used.

    :param recipients: An array representing the email address of the recipient of the email
    :param sender: A string representing the email adress of the sender of the email
    :param mail_model_name: The name of the MailModel representing an email
    :param translation: The language of a TemplateTranslation (e.g. 'EN'). If omitted, the
        default language provided while plugging mailtemplates is used
    :param data: A dictionary representing the variables used in the email template, like ${name}
    :param send_async: The email will sent asynchronously if this flag is True
    """
    if 'kajiki' not in config['render_functions']:
        raise MailTemplatesError('Kajiki must be allowed in your app.')

    __, mail_models = model.provider.query(model.MailModel, filters=dict(name=mail_model_name))
    if not mail_models:
        raise MailTemplatesError("Mail model '%s' not found." % mail_model_name)
    mail_model = mail_models[0]

    language = translation or config['_mailtemplates']['default_language']

    __, translations = model.provider.query(
        model.TemplateTranslation,
        filters=dict(mail_model=mail_model, language=language)
    )
    if not translations:
        raise MailTemplatesError('Translation for this mail model not found')
    tr = translations[0]

    # as the template is already translated, use a fake gettext
    data.update({'gettext': lambda x: x})

    Template = kajiki.XMLTemplate(source=tr.body)
    Template.loader = tg.config['render_functions']['kajiki'].loader
    html = Template(data).render()

    Template = kajiki.TextTemplate(tr.subject)
    subject = Template(data).render()

    _send_email(sender, recipients, subject, html, cc=cc, send_async=send_async)


def _get_request():
    """You can mock this helper in order to unit-test not-async mails
    @patch('mailtemplates.lib._get_request', Mock(return_value=None))
    You should do this because in tests you do not have anymore the request,
    using global mailer in tests is good enough.
    """
    return tg.request

def _send_email(sender, recipients, subject, html, cc=None, send_async=True):
    if not isinstance(recipients, list):
        recipients = list(recipients)

    if send_async and config['_mailtemplates']['async_sender'] == 'tgext.celery':
        from mailtemplates.lib.celery_tasks import mailtemplates_async_send_email
        mailtemplates_async_send_email.delay(
            subject=subject, sender=sender,
            recipients=recipients, html=html, cc=cc
        )
    elif send_async and config['_mailtemplates']['async_sender'] == 'tgext.asyncjob':
        from tgext.asyncjob import asyncjob_perform
        mailer = get_mailer(None)
        message = Message(
            subject=subject, sender=sender, recipients=recipients, 
            html=html, cc=cc
        )
        asyncjob_perform(mailer.send_immediately, message=message)
    else:
        try:
            mailer = get_mailer(_get_request())
            log.debug('using request mailer')
        except AttributeError:
            log.debug('using global mailer in not-async context')
            mailer = get_mailer(None)
        message = Message(
            subject=subject, sender=sender, recipients=recipients, 
            html=html, cc=cc
        )
        mailer.send_immediately(message)


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
