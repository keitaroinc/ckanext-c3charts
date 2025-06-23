import logging

logger = logging.getLogger(__name__)

try:
    import ckan
    if not hasattr(ckan, '__version__'):
        try:
            import pkg_resources
            ckan.__version__ = pkg_resources.get_distribution("ckan").version
        except Exception:
            ckan.__version__ = '2.9.0'
except ImportError:
    logging.info("Ckan module not found")
