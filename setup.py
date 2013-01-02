#!/usr/bin/env python

from distutils.core import setup

setup(name='xml_models',
      version='0.6.4',
      description='JSON/XML backed models queried from external REST apis',
      author='Chris Tarttelin and Cam McHugh',
      author_email='chris@pyruby.com',
      url='http://djangorestmodel.sourceforge.net/',
      packages=['rest_client', 'xml_models', 'json_models','common_models'],
      install_requires=['mock', 'py-dom-xpath']
     )
