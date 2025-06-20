import logging

from sqlalchemy import types, Column, Table, exists
from sqlalchemy.sql.expression import false
from sqlalchemy import create_engine
from sqlalchemy import inspect

from ckan.model.meta import metadata, mapper, Session
from ckan.model.types import make_uuid
from ckan.model.domain_object import DomainObject
from ckan.model import Package
import ckan.lib.dictization as d
from ckan.plugins.toolkit import config

log = logging.getLogger(__name__)

__all__ = [
    'FeaturedCharts', 'featured_charts_table',
]

featured_charts_table = None


class FeaturedCharts(DomainObject):

    @classmethod
    def get_featured_charts(cls, limit=3):
        results = Session.query(cls). \
            join(Package, cls.package_id == Package.id). \
            order_by(Package.metadata_modified.desc()). \
            filter(Package.private == false()). \
            limit(limit). \
            all()
        return [d.table_dictize(result, {'model': FeaturedCharts}) for result in results] # noqa

    @classmethod
    def save_featured_chart(cls, package_id, resource_id, view_id):
        already_exists = Session.query(exists().
                                       where(FeaturedCharts.package_id == package_id). # noqa
                                       where(FeaturedCharts.resource_id == resource_id). # noqa
                                       where(FeaturedCharts.resource_view_id == view_id)).scalar() # noqa
        if not already_exists:
            featured_chart = FeaturedCharts(resource_view_id=view_id,
                                            package_id=package_id,
                                            resource_id=resource_id)
            Session.add(featured_chart)
            Session.commit()

    @classmethod
    def delete_from_featured_charts(cls, resource_view_id):
        results = Session.query(FeaturedCharts). \
            filter(FeaturedCharts.resource_view_id == resource_view_id).all()
        for result in results:
            Session.delete(result)
        Session.commit()

    @classmethod
    def delete_from_featured_charts_by_resource(cls, resource_id):
        results = Session.query(FeaturedCharts). \
            filter(FeaturedCharts.resource_id == resource_id).all()
        for result in results:
            Session.delete(result)
        Session.commit()

    @classmethod
    def delete_from_featured_charts_by_package(cls, package_id):
        results = Session.query(FeaturedCharts). \
            filter(FeaturedCharts.package_id == package_id).all()
        for result in results:
            Session.delete(result)
        Session.commit()


def setup():
    if featured_charts_table is None:
        define_featured_charts_table()
        log.debug('Featured charts table defined in memory')
        db_url = config.get('sqlalchemy.url')

        engine = create_engine(db_url)

        featured_charts_table.metadata.bind = engine
        inspector = inspect(engine)
        if not inspector.has_table('ckanext_c3charts_featured_charts'):
            featured_charts_table.metadata.create_all(bind=engine)
            log.debug('Featured charts table created')
        else:
            log.debug('Featured charts table already exists')
    else:
        log.debug('Featured charts table already exists')


def define_featured_charts_table():
    global featured_charts_table
    featured_charts_table = Table('ckanext_c3charts_featured_charts', metadata,
                              Column('id', types.UnicodeText, primary_key=True, default=make_uuid), # noqa
                              Column('resource_view_id', types.UnicodeText), # noqa
                              Column('resource_id', types.UnicodeText), # noqa
                              Column('package_id', types.UnicodeText), extend_existing=True) # noqa

    mapper(
        FeaturedCharts,
        featured_charts_table
    )

    db_url = config.get('sqlalchemy.url')
    engine = create_engine(db_url)
    featured_charts_table.metadata.bind = engine

    inspector = inspect(engine)
    if not inspector.has_table('ckanext_c3charts_featured_charts'):
        featured_charts_table.metadata.create_all(bind=engine)
        log.debug('Featured charts table created')
    else:
        log.debug('Featured charts table already exists')
