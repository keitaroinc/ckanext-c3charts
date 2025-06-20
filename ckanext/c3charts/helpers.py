from ckan.logic import get_action
import ckan.lib.helpers as h
import ckan.model as model
from uuid import uuid4
from ckan.plugins import toolkit
import logging
logger = logging.getLogger(__name__)


def c3charts_featured_charts(limit=3):
    FeaturedCharts = get_featured_charts_model()

    resource_view_show = get_action('resource_view_show')
    resource_show = get_action('resource_show')
    package_show = get_action('package_show')
    charts = FeaturedCharts.get_featured_charts(limit) or []
    context = {'model': model, 'ignore_auth': True}
    result_charts = []
    for chart in charts:
        resource = None
        dataset = None
        view = None

        view = _call_ignore_error(resource_view_show, context, {'id': chart['resource_view_id']}) # noqa
        resource = _call_ignore_error(resource_show, context, {'id': chart['resource_id']}) # noqa
        dataset = _call_ignore_error(package_show, context, {'id': chart['package_id']}) # noqa
        if view is None or resource is None or dataset is None:
            continue
        chart['title'] = view.get('title')
        chart['resource_view'] = view
        chart['resource'] = resource
        chart['dataset'] = dataset
        chart['resource_view_url'] = h.url_for(str('/dataset/%s/resource/%s' % (chart['package_id'], chart['resource_id'])), view_id=chart['resource_view_id']) # noqa
        result_charts.append(chart)
    return result_charts


def c3charts_uuid(id):
    if not id:
        return str(uuid4())
    return "%s_%s" % (id, str(uuid4()))


def _call_ignore_error(func, *args):
    try:
        return func(*args)
    except Exception:
        return None


def c3charts_render_featured_chart(featured_chart, embed=True):
    return h.rendered_resource_view(featured_chart['resource_view'],
                                    featured_chart['resource'],
                                    featured_chart['dataset'],
                                    embed=embed)


def get_ckan_version():
    data = toolkit.get_action('status_show')({})
    return data['ckan_version']


def get_featured_charts_model():
    """Dynamically imports and initializes the
    FeaturedCharts model based on CKAN version."""
    version = get_ckan_version()
    try:
        if version.startswith('2.11'):
            from ckanext.c3charts.model import featured_charts_2_11 as fc_model
        else:
            from ckanext.c3charts.model import featured_charts as fc_model

        fc_model.setup()
        return fc_model.FeaturedCharts
    except ImportError as e: # noqa
        logger.exception(f"Could not import FeaturedCharts model for CKAN version {version}") # noqa
        raise
