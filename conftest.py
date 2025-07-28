# -*- coding: utf-8 -*-
import sys

pytest_plugins = [
    u'ckan.tests.pytest_ckan.ckan_setup',
    u'ckan.tests.pytest_ckan.fixtures',
]

def try_patch_ckan_version():
    try:
        import ckan
        if not hasattr(ckan, '__version__'):
            ckan.__version__ = '2.11.0'
    except ImportError:
        pass

def pytest_load_initial_conftests(args):
    try_patch_ckan_version()