from ckanext.c3charts.helpers import get_featured_charts_model


def save_featured_chart(package_id, resource_id, view_id):
    FeaturedCharts = get_featured_charts_model()
    FeaturedCharts.save_featured_chart(package_id, resource_id, view_id)


def remove_from_featured_charts(view_id):
    FeaturedCharts = get_featured_charts_model()
    FeaturedCharts.delete_from_featured_charts(view_id)


def remove_all_featured_charts_for_resource(resource_id):
    FeaturedCharts = get_featured_charts_model()
    FeaturedCharts.delete_from_featured_charts_by_resource(resource_id)


def remove_all_featured_charts_for_package(package_id):
    FeaturedCharts = get_featured_charts_model()
    FeaturedCharts.delete_from_featured_charts_by_package(package_id)
