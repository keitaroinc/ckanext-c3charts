from ckanext.c3charts.model import FeaturedCharts

def save_featured_chart(package_id, resource_id, view_id):
    print "Saving featured chart: ", package_id, resource_id, view_id
    FeaturedCharts.save_featured_chart(package_id, resource_id, view_id)


def remove_from_featured_charts(view_id):
    FeaturedCharts.delete_from_featured_charts(view_id)