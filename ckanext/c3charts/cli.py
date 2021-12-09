# -*- coding: utf-8 -*-
import click

from ckanext.c3charts.model.featured_charts \
    import setup as setup_featured_charts_table


@click.group()
def c3charts():
    """c3charts management commands.
    """
    pass


@c3charts.command(name='init-db')
def init_db():
    setup_featured_charts_table()
    click.echo(u'Featured charts tables initialized')


def get_commands():
    return [c3charts]
