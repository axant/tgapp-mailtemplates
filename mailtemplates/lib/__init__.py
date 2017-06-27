# -*- coding: utf-8 -*-
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from smtplib import SMTP

import tg
import turbomail as turbomail
from markupsafe import Markup
from tg import config, request, render_template
from tgext.mailer import get_mailer, Message
import kajiki

from mailtemplates import model


def format_rich_mail(title, body):
    params = {'title': title, 'body': Markup(body)}
    return render_template(params, template_engine='email',
                           template_name='movieday.templates.email.md_rich_email')


def send_email(recipients, sender, mail_model_name, translation=None, data=None, subject_data=None):
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
    """
    __, mail_models = model.provider.query(model.MailModel, filters=dict(name=mail_model_name))
    if not mail_models:
        raise Exception("Mail model '%s' not found." % mail_model_name)
    mail_model = mail_models[0]

    language = translation or config['_mailtemplates']['default_language']

    __, translations = model.provider.query(model.TemplateTranslation, filters=dict(mail_model=mail_model,
                                                                                    language=language))
    if not translations:
        raise Exception('Translation for this mail model not found')
    tr = translations[0]

    Template = kajiki.XMLTemplate(tr.body)
    Template.loader = tg.config['render_functions']['kajiki'].loader

    html = Template(data).render()

    if subject_data:
        Template = kajiki.TextTemplate(tr.subject)
        subject = Template(subject_data).render()
    else:
        subject = tr.subject

    mailer = get_mailer(request)
    message_to_send = Message(
        subject=subject,
        sender=sender,
        recipients=recipients,
        html=html
    )
    if config.get('tm.enabled', False):
        mailer.send(message_to_send)
    else:
        mailer.send_immediately(message_to_send)