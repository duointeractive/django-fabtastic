from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = "Flushes the Django cache."

    def handle(self, *args, **options):
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
