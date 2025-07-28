# -*- coding: utf-8 -*-

import sys
import types

# Patch ckan.__version__ before any other CKAN imports
def patch_ckan_version():
    if 'ckan' in sys.modules:
        ckan = sys.modules['ckan']
    else:
        ckan = types.ModuleType('ckan')
        sys.modules['ckan'] = ckan

    if not hasattr(ckan, '__version__'):
        ckan.__version__ = '2.11.0'

patch_ckan_version()

pytest_plugins = [
    u'ckan.tests.pytest_ckan.ckan_setup',
    u'ckan.tests.pytest_ckan.fixtures',
]
