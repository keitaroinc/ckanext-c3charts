# encoding: utf-8
import pytest

import ckan.plugins as p

from ckan.tests import factories
from ckan.plugins import toolkit
import ckan.tests.helpers as helpers


@pytest.fixture(scope="session")
def with_plugins():
    """Load required plugins for tests"""
    plugins_to_load = ['datastore', 'c3charts']
    loaded_plugins = []

    for plugin in plugins_to_load:
        if not p.plugin_loaded(plugin):
            p.load(plugin)
            loaded_plugins.append(plugin)

    yield

    # Cleanup
    for plugin in loaded_plugins:
        p.unload(plugin)


@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
@pytest.mark.ckan_config('ckan.views.default_views', '')
def test_view_shown_on_resource_page():

    dataset = factories.Dataset()
    sysadmin = factories.Sysadmin()

    resource = factories.Resource(package_id=dataset['id'],
                                  url='http://some.website.html',)

    if toolkit.check_ckan_version(min_version="2.11"):
        data = {
            "resource_id": resource.get('id'),
            "force": True,
        }
        helpers.call_action("datastore_create", **data)
    else:
        p.toolkit.get_action('datastore_create')(
            {'user': sysadmin.get('name')},
            {'resource_id': resource.get('id'), 'force': True}
        )

    resource_view = factories.ResourceView(
        resource_id=resource['id'],
        view_type='Chart builder',
        chart_type='Bar Chart',
        key_fields='foo,bar',
        x_fields='foo',
        color_scheme='#B80000',
        text_chart_number_action='average',
        legend='bottom',)

    response = p.toolkit.get_action('resource_view_show')(
        {'user': sysadmin.get('name')},
        {'id': resource_view.get('id')}
    )

    assert response.get('view_type') == 'Chart builder'
    assert response.get('chart_type') == 'Bar Chart'
    assert response.get('key_fields') == 'foo,bar'
    assert response.get('x_fields') == 'foo'
    assert response.get('color_scheme') == '#B80000'
    assert response.get('text_chart_number_action') == 'average'
    assert response.get('legend') == 'bottom'
