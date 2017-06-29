# -*- coding: utf-8 -*-
"""Setup the mailtemplates application"""
from __future__ import print_function

from mailtemplates import model
from tgext.pluggable import app_model


def bootstrap(command, conf, vars):
    print('Bootstrapping mailtemplates...')

    __, managers = model.provider.query(app_model.Group, filters=dict(group_name='managers'))
    if managers:
        manager = managers[0]
        model.provider.create(app_model.Permission, dict(permission_name=u'mailtemplates',
                                                         description=u'This permission allow access to the '
                                                                     u'mailtemplates pluggable',
                                                         groups=[manager]
                                                         )
                              )

    t1 = model.provider.create(model.MailModel, dict(name=u'Email', usage=u'Usage'))
    t2 = model.provider.create(model.MailModel, dict(name=u'Email1',
                                                     usage=u'This is the description of the email content, including '
                                                           u'the usage of the email in his context'
                                                     )
                               )
    model.DBSession.flush()

    tr1 = model.provider.create(model.TemplateTranslation,
                                dict(language=u'EN', mail_model=t1, subject=u'Subject',
                                     body=u'''Something incredible is waiting to be known! Two ghostly white figures in
                                     coveralls and helmets are soflty dancing kindling the energy hidden in matter?
                                     Cosmos, another world, cosmic ocean! Dream of the mind's eye,Drake Equation,
                                     Orion's sword. Realm of the galaxies, science concept of the number one two ghostly
                                      white figuresin coveralls and helmets are soflty dancing network of wormholes made
                                       in the interiors of collapsing stars, the ash of stellar alchemy billions upon
                                       billions astonishment Tunguska event, finite but unbounded rings of Uranus a very
                                       small stage in a vast cosmic arena? The sky calls to us. White dwarf made in the
                                       interiors of collapsing stars the ash of stellar alchemy, rich in mystery
                                       explorations citizens of distant epochs and billions upon billions upon billions
                                       upon billions upon billions upon billions upon billions.'''))

    model.DBSession.flush()