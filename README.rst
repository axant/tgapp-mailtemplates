About mailtemplates
-------------------------

mailtemplates is a Pluggable application for TurboGears2.

Installing
-------------------------------

mailtemplates can be installed both from pypi or from bitbucket::

    pip install mailtemplates

should just work for most of the users

Plugging mailtemplates
----------------------------

In your application *config/app_cfg.py* import **plug**::

    from tgext.pluggable import plug

Then at the *end of the file* call plug with mailtemplates::

    plug(base_config, 'mailtemplates')

For configure your default language for email templates, add the ISO 3166-2 code as parameter of the `plug` call::

     plug(base_config, 'mailtemplates', default_language='IT')

If not specified, 'EN' will be the default language for you app.

You will be able to access the plugged application at
*http://localhost:8080/mailtemplates*.

Available Hooks
----------------------
mailtemplates makes available a some hooks which will be
called during some actions to alter the default
behavior of the appplications:

Exposed Partials
----------------------

mailtemplates exposes a bunch of partials which can be used
to render pieces of the blogging system anywhere in your
application:

Exposed Templates
--------------------

The templates used by registration and that can be replaced with
*tgext.pluggable.replace_template* are:

