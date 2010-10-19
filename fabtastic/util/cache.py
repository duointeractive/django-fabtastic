"""
Various cache-related general utility functions.
"""
from django.core.cache import cache

def clear_django_cache():
    """
    Clears the Django cache through the cache backend.
    """
    try:
        cache._cache.flush_all()
    except AttributeError:
        # try filesystem caching next
        old = cache._cull_frequency
        old_max = cache._max_entries
        cache._max_entries = 0
        cache._cull_frequency = 1
        cache._cull()
        cache._cull_frequency = old
        cache._max_entries = old_max