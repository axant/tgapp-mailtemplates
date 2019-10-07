# -*- coding: utf-8 -*-
import sys, os

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools

    use_setuptools()
    from setuptools import setup, find_packages

install_requires = [
    "tgext.pluggable >= 0.7.2",
    "sprox >= 0.9.1",
    "tgext.mailer",
    "kajiki >= 0.7.1",
    "TurboGears2 >= 2.3.8",
]

testpkgs = ['WebTest>=1.2.3',
            'nose',
            'coverage',
            'mock',
            'ming',
            'sqlalchemy',
            'zope.sqlalchemy',
            'repoze.who',
            'tw2.forms',
            'pyquery',
            'tgext.asyncjob']
here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

setup(
    name='tgapp-mailtemplates',
    version='0.13.9',
    description='Email template management for web applications',
    long_description=README,
    author='Marco Bosio',
    author_email='marco.bosio@axant.it',
    url='https://github.com/axant/tgapp-mailtemplates',
    keywords='turbogears2.application',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    package_data={'mailtemplates': [
        'i18n/*/LC_MESSAGES/*.mo',
        'templates/*/*',
        'public/*/*'
    ]},
    tests_require=testpkgs,
    extras_require={
        'testing': testpkgs,
        'asyncjob': ['tgext.asyncjob == 0.3.1'],
        'celery': ['tgext.celery >= 0.0.3']
    },
    message_extractors={'mailtemplates': [
        ('**.py', 'python', None),
        ('templates/**.xhtml', 'kajiki', None),
        ('templates/**.html', 'genshi', None),
        ('public/**', 'ignore', None)
    ]},
    entry_points="""
    """,
    zip_safe=False
)
