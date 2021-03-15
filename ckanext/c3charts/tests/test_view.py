# encoding: utf-8
import pytest

import ckan.plugins as p

from ckan.tests import factories


@pytest.mark.usefixtures(u'clean_db', u'clean_index')
@pytest.mark.ckan_config('ckan.views.default_views', '')
def test_view_shown_on_resource_page():

    dataset = factories.Dataset()
    sysadmin = factories.Sysadmin()

    resource = factories.Resource(package_id=dataset['id'],
                                  url='http://some.website.html',)

    datastore_resource = p.toolkit.get_action('datastore_create')(
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
