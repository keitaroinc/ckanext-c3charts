from ckanext.c3charts.model import FeaturedCharts
from ckan.logic import get_action
import ckan.lib.helpers as h
import ckan.model as model

def c3charts_featured_charts(limit=3):
    resource_view_show = get_action('resource_view_show')
    resource_show = get_action('resource_show')
    package_show = get_action('package_show')
    charts = FeaturedCharts.get_featured_charts(limit) or []
    context = {'model': model}
    for chart in charts:
        resource = None
        dataset = None
        view = None

        view = _call_ignore_error(resource_view_show, context, {'id': chart['resource_view_id']})
        resource = _call_ignore_error (resource_show, context, {'id': chart['resource_id']})
        dataset = _call_ignore_error(package_show, context, {'id': chart['package_id']})
        chart['title'] = view.get('title')
        chart['resource_view'] = view
        chart['resource'] = resource
        chart['dataset'] = dataset
        chart['resource_view_url'] = h.url_for(str('/dataset/%s/resource/%s' % (chart['package_id'], chart['resource_id'])),view_id=chart['resource_view_id'])
    return charts


def _call_ignore_error(func, *args):
    try:
        return func(*args)
    except:
        return None

def c3charts_render_featured_chart(featured_chart, embed=True):
    return h.rendered_resource_view(featured_chart['resource_view'], featured_chart['resource'], featured_chart['dataset'], embed=embed )
