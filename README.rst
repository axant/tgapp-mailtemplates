.. image:: https://travis-ci.org/axant/tgapp-mailtemplates.svg?branch=master
   :target: https://travis-ci.org/axant/tgapp-mailtemplates

About mailtemplates
-------------------------

mailtemplates is a Pluggable application for TurboGears2.

mailtemplates provides a dashboard meant for managers of your website (whoever has the ``mailtemplates`` permission) allowing them to customize the templates of the email that are sent from your application.

the templates are stored in a database and both ``sqlalchemy`` and ``ming`` are supported.

kajiki is the template engine used.

Installing
-------------------------------

mailtemplates can work with ``tgext.asyncjob`` or ``tgext.asyncjob``
you can choose by installing with the right bundle::

    pip install "mailtemplates[asyncjob]"

or::

    pip install "mailtemplates[celery]"

if you just want to send emails in a syncronous context then install the base package and plug with ``async_sender`` set to ``None``

Plugging mailtemplates
----------------------------

In your application *config/app_cfg.py* import **plug**::

    from tgext.pluggable import plug

Then at the *end of the file* call plug with mailtemplates::

    plug(base_config, 'mailtemplates')

For configure your default language for email templates, add the ISO 3166-2 code as parameter of the `plug` call::

     plug(base_config, 'mailtemplates', default_language='IT')

If not specified, 'EN' will be the default language for you app.

If you intend to use tgext.celery then plug and configure it **before** plugging mailtemplates with ``async_sender`` option::

    plug(base_config, 'mailtemplates', async_sender='tgext.celery')

and in your ``.ini`` file add under ``celery.CELERY_INCLUDE`` ``mailtemplates.lib.celery_tasks``::

    celery.CELERY_INCLUDE = myapp.lib.celery.tasks mailtemplates.lib.celery_tasks


You will be able to access the plugged application at
*http://localhost:8080/mailtemplates*.

Sending emails
--------------

access to the dashboard and create a mail model, then you can use::

    from mailtemplates.lib import send_email
    send_email(
      recipients=['address@example.com'],
      sender=config.get('mail.username'),
      mail_model_name='test',
      data=dict(test='test string'),
      send_async=True,
    )

in your controllers to actually send the email.

details of params of ``send_email``

- recipients: An array representing the email address of the recipient of the email
- sender: A string representing the email address of the sender of the email
- mail_model_name: The name of the MailModel representing an email
- translation: The language of a TemplateTranslation (e.g. 'EN'). If omitted, the
  default language provided while plugging mailtemplates is used
- data: A dictionary representing the variables used in the email template, like ${name}
- send_async: The email will sent asynchronously if this flag is True

Note on send_async
--------------------

if you are already in an asyncronous context then you can't use tgext.asyncjob with send_async=True,
but you're already in an asyncronous context, so you can just use send_async=False.
If you really need to send email asynchronously from an already asyncronous context, then use tgext.celery
