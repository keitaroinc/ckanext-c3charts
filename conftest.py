# -*- coding: utf-8 -*-
import sys

pytest_plugins = [
    u'ckan.tests.pytest_ckan.ckan_setup',
    u'ckan.tests.pytest_ckan.fixtures',
]

if 'ckan' in sys.modules:
    ckan = sys.modules['ckan']
    if not hasattr(ckan, '__version__'):
        ckan.__version__ = '2.11.0'
