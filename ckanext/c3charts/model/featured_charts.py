import logging

import ckan.logic as l
from sqlalchemy import orm, types, ForeignKey, Column, Table, exists

from ckan.model.meta import metadata, mapper, Session
from ckan.model.types import make_uuid
from ckan.model.domain_object import DomainObject
from ckan.model import Package
import ckan.lib.dictization as d

log = logging.getLogger(__name__)


__all__ = [
    'FeaturedCharts', 'featured_charts_table',
]

featured_charts_table = None


class FeaturedCharts(DomainObject):

    @classmethod
    def get_featured_charts(cls, limit=3):
        results = Session.query(cls).\
            join(Package, cls.package_id == Package.id).\
            order_by(Package.metadata_modified.desc()).\
            limit(limit).\
            all()
        return [d.table_dictize(result, {'model': FeaturedCharts}) for result in results]

    @classmethod
    def save_featured_chart(cls, package_id, resource_id, view_id):
        already_exists = Session.query(exists().\
                        where(FeaturedCharts.package_id == package_id and FeaturedCharts.resource_id == resource_id and FeaturedCharts.resource_view_id == view_id)).scalar()
        if not already_exists:
            featured_chart = FeaturedCharts(resource_view_id=view_id, package_id=package_id, resource_id=resource_id)
            Session.add(featured_chart)
            Session.commit()
    
    @classmethod
    def delete_from_featured_charts(cls, resource_view_id):
        results = Session.query(FeaturedCharts).filter(FeaturedCharts.resource_view_id == resource_view_id).all()
        for result in results:
            Session.delete(result)
        Session.commit()

def setup():
    if featured_charts_table is None:
        define_featured_charts_table()
        log.debug('User extra table defined in memory')

        if not featured_charts_table.exists():
            featured_charts_table.create()
            log.debug('User extra created')
        else:
            log.debug('User extra table already created')
    else:
        log.debug('User extra table already exist')


def define_featured_charts_table():
    global featured_charts_table
    featured_charts_table = Table('featured_charts', metadata,
                             Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
                             Column('resource_view_id', types.UnicodeText),
                             Column('resource_id', types.UnicodeText),
                             Column('package_id', types.UnicodeText)
                             )

    mapper(
        FeaturedCharts,
        featured_charts_table
    )
