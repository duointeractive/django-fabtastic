"""
Various database-related utility functions.
"""
from django.conf import settings

def get_db_setting(db_setting, db_alias='default'):
    """
    Gets a database setting from settings.py. Extra logic to support
    Django 1.1 and Django 1.2.
    """
    if hasattr(settings, 'DATABASE'):
        return settings.DATABASE[db_alias]['ENGINE']
    else:
        return settings.DATABASE_ENGINE