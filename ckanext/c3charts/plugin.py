import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging
from ckan.lib.plugins import DefaultTranslation

logger = logging.getLogger(__name__)
not_empty = plugins.toolkit.get_validator('not_empty')
ignore_missing = plugins.toolkit.get_validator('ignore_missing')
ignore_empty = plugins.toolkit.get_validator('ignore_empty')


class ChartsPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IResourceView, inherit=True)
    plugins.implements(plugins.ITranslation)

    # IConfigurer

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('fanstatic', 'c3charts')

    def info(self):
        schema = {
            'chart_type': [not_empty],
            'key_fields': [not_empty],
            'x_fields': [ignore_missing],
            'color_scheme': [not_empty],
            'header': [ignore_missing],
            'measure_unit_x': [ignore_missing],
            'measure_unit_y': [ignore_missing],
            'text_chart_number_action': [not_empty],
            'legend': [not_empty],
            'rotated': [ignore_missing],
            'data_labels': [ignore_missing],
            'x_grid': [ignore_missing],
            'y_grid': [ignore_missing],
            'remap_key': [ignore_missing],
            'aggregate': [ignore_missing]
        }

        return {'name': toolkit._('Chart builder'),
                'icon': 'bar-chart-o',
                'filterable': True,
                'iframed': False,
                'schema': schema}

    def can_view(self, data_dict):
        return data_dict['resource'].get('datastore_active', False)

    def setup_template_variables(self, context, data_dict):
        resource = data_dict['resource']
        resource_view = data_dict['resource_view']

        fields = _get_fields_without_id(resource)
        remap_keys = list(fields)
        remap_keys.insert(0, {'value': ''})
        logger.debug(remap_keys)

        return {'resource': resource,
                'resource_view': resource_view,
                'fields': fields,
                'remap_keys': remap_keys,
                'chart_types': [{'value': 'Bar Chart'},
                                {'value': 'Stacked Bar Chart'},
                                {'value': 'Donut Chart'},
                                {'value': 'Line Chart'},
                                {'value': 'Pie Chart'},
                                {'value': 'Spline Chart'},
                                {'value': 'Table Chart'},
                                {'value': 'Simple Chart'}],
                'color_schemes': [{'value': '#B80000, #995522, #556677, #118888, #115588, '
                                            '#4C3D3D, #2B2B2B, #660000, #221100',
                                   'text': toolkit._('Saturated')},
                                  {'value': '#DDBBAA, #79E6F2, #88AA99, #00A864, #228899, '
                                            '#3F797F, #775555, #118855, #008751, #3D4C46',
                                   'text': toolkit._('Light')},
                                  {'value': '#ADC0D8, #79AFF2, #8899AA, #0EAAB2, #00A0A8, '
                                            '#776655, #118888, #885511, #3F5C7F, #225599',
                                   'text': toolkit._('Pastel')},
                                  {'value': '#ADB1D8, #8899AA, #7983F2, #777752, #887711, '
                                            '#0070C0, #0062A8, #3F457F, #115588, #3D464C',
                                   'text': toolkit._('Pastel 2')},
                                  {'value': '#AA9988, #A88600, #779922, #6C7F3F, #887711, '
                                            '#555577, #665500, #665100, #4C493D, #2B2B2V',
                                   'text': toolkit._('Contrast')}],
                'text_chart_number_actions': [{'value': 'substract',
                                               'text': toolkit._('Substract last two entries')},
                                              {'value': 'average',
                                               'text': toolkit._('Average')},
                                              {'value': 'last',
                                               'text': toolkit._('Show last')}],
                'legend_options': [{'text': toolkit._('Hide'), 'value': 'hide'},
                                     {'text': toolkit._('Right'), 'value': 'right'},
                                     {'text': toolkit._('Bottom'), 'value': 'bottom'}]
                }

    def view_template(self, context, data_dict):
        return 'charts_view.html'

    def form_template(self, context, data_dict):
        return 'charts_form.html'


def _get_fields_without_id(resource):
    fields = _get_fields(resource)
    return [{'value': v['id']} for v in fields if v['id'] != '_id']


def _get_fields(resource):
    data = {
        'resource_id': resource['id'],
        'limit': 0
    }
    result = plugins.toolkit.get_action('datastore_search')({}, data)
    return result['fields']
