# -*- coding: utf-8 -*-
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from smtplib import SMTP

import tg
from markupsafe import Markup
from tg import app_globals
from tg import config, request, render_template
from tgext.mailer import get_mailer, Message
import kajiki

from mailtemplates import model
from mailtemplates.lib.exceptions import MailTemplatesError


def send_email(recipients, sender, mail_model_name, translation=None, data=None, test_mode=False):
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
    :param subject_data:  A dictionary representing the variables used in the email subject, like ${name}
    :param test_mode: A flag for using this function in test mode. With test mode active, you don't have to pass to the
        template the variables associated. Instead, the variables were be filled with their names. E.g. If you have a
        variable named ${name} in your template, you'll se in the test mail ${name} in his position.
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

    body = tr.body if not test_mode else tr.body.replace('$', '$$')
    Template = kajiki.XMLTemplate(body)
    Template.loader = tg.config['render_functions']['kajiki'].loader

    html = Template(data).render()

    Template = kajiki.TextTemplate(tr.subject)
    subject = Template(data).render()
    _send_email(sender, recipients, subject, html)


def _send_email(sender, recipients, subject, html):
    mailer = get_mailer(app_globals)
    if not isinstance(recipients, list):
        recipients = list(recipients)

    message_to_send = Message(
        subject=subject,
        sender=sender,
        recipients=recipients,
        html=html
    )

    try:
        #     if config.get('tm.enabled', False):
        #         mailer.send(message_to_send)
        #     else:
        mailer.send_immediately(message_to_send)
    except Exception as e:

        raise MailTemplatesError(e)
