# -*- coding: utf-8 -*-
import sys, os

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

install_requires=[
    "TurboGears2 >= 2.3.9",
    "tgext.pluggable",
    "sprox >= 0.9.1",
    "tgext.mailer"
]

testpkgs = ['WebTest >= 1.2.3',
          'nose',
          'coverage',
          'ming',
          'sqlalchemy',
          'zope.sqlalchemy',
          'repoze.who',
          'tw2.forms',
          'kajiki',
          'pyquery']
here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

setup(
    name='mailtemplates',
    version='0.1.0',
    description='',
    long_description=README,
    author='',
    author_email='',
    #url='',
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
        # Used by Drone.io
        'testing': testpkgs,
    },
    message_extractors={'mailtemplates': [
            ('**.py', 'python', None),
            ('templates/**.xhtml', 'kajiki', None),
            ('public/**', 'ignore', None)
    ]},
    entry_points="""
    """,
    zip_safe=False
)
