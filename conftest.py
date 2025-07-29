import pytest
import ckan

@pytest.fixture(autouse=True)
def mock_ckan_version():
    ckan.__version__ = '2.10'

pytest_plugins = [
    u'ckan.tests.pytest_ckan.ckan_setup',
    u'ckan.tests.pytest_ckan.fixtures',
]
