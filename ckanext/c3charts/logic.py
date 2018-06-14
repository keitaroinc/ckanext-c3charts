from ckanext.c3charts.model import FeaturedCharts

def save_featured_chart(package_id, resource_id, view_id):
    print "Saving featured chart: ", package_id, resource_id, view_id
    FeaturedCharts.save_featured_chart(package_id, resource_id, view_id)