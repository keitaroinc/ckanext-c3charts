# -*- coding: utf-8 -*-

from logging import getLogger

from ckan.lib.cli import CkanCommand
from ckanext.c3charts.model.featured_charts \
    import setup as setup_featured_charts_table

log = getLogger('ckanext.c3charts')


class InitDB(CkanCommand):
    ''' Initialize Featured charts tables. '''

    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = 0
    min_args = 0

    def command(self):
        self._load_config()
        
        setup_featured_charts_table()

        log.info('Featured charts tables initialized')