import sys
import importlib

def safe_register_plugin(name):
    module = sys.modules.get(name)
    if not module:
        module = importlib.import_module(name)
    return module

pytest_plugins = [
    safe_register_plugin('ckan.tests.pytest_ckan.ckan_setup'),
    safe_register_plugin('ckan.tests.pytest_ckan.fixtures'),
]
