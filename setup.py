# -*- coding: utf-8 -*-
import sys, os

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools

    use_setuptools()
    from setuptools import setup, find_packages

install_requires = [
    "tgext.pluggable",
    "sprox >= 0.9.1",
    "tgext.mailer",
    "kajiki",
    "tgext.asyncjob==0.3.1"
]

testpkgs = ['WebTest >= 1.2.3',
            'nose',
            'coverage',
            'ming',
            'sqlalchemy',
            'zope.sqlalchemy',
            'repoze.who',
            'tw2.forms',
            'pyquery',
            'TurboGears2 >= 2.3.9',
            ]
here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

setup(
    name='tgapp-mailtemplates',
    version='0.10.0',
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
