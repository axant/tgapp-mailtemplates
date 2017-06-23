# -*- coding: utf-8 -*-

"""WebHelpers used in mailtemplates."""

#from webhelpers import date, feedgenerator, html, number, misc, text
from markupsafe import Markup

def bold(text):
    return Markup('<strong>%s</strong>' % text)

def ellipsis(text, n_char=200):
    return text[0:int(n_char)] + '...'