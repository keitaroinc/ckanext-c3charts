from ckanext.c3charts.model import FeaturedCharts
from ckan.logic import get_action
import ckan.model as model

def c3charts_featured_charts(limit=3):
    resource_view_show = get_action('resource_view_show')
    charts = FeaturedCharts.get_featured_charts(limit) or []

    for chart in charts:
        view = resource_view_show({'model': model}, {'id': chart['resource_view_id']})
        print " ===> view: ", view
        chart['title'] = view.get('title')

    return charts
