# -*- coding: utf-8 -*-
"""Setup the mailtemplates application"""
from __future__ import print_function

from mailtemplates import model
from tgext.pluggable import app_model


def bootstrap(command, conf, vars):
    print('Bootstrapping mailtemplates...')

    t1 = model.Template()
    t1.name = 'Email'
    t1.usage = 'Usage'

    model.DBSession.add(t1)
    model.DBSession.flush()

    tr1 = model.Translation()
    tr1.language = 'EN'
    tr1.template = t1
    tr1.subject = 'Subject'
    t1.body = '''
    Something incredible is waiting to be known! Two ghostly white figures in coveralls and helmets are
    soflty dancing kindling the energy hidden in matter? Cosmos, another world, cosmic ocean! Dream of the mind's eye,
    Drake Equation, Orion's sword. Realm of the galaxies, science concept of the number one two ghostly white figures
    in coveralls and helmets are soflty dancing network of wormholes made in the interiors of collapsing stars, the ash
    of stellar alchemy billions upon billions astonishment Tunguska event, finite but unbounded rings of Uranus a very
    small stage in a vast cosmic arena? The sky calls to us. White dwarf made in the interiors of collapsing stars the
    ash of stellar alchemy, rich in mystery explorations citizens of distant epochs and billions upon billions upon
    billions upon billions upon billions upon billions upon billions.
    '''

    model.DBSession.add(tr1)
    model.DBSession.flush()