from django.core.management.base import BaseCommand
from fabtastic.util.cache import clear_django_cache

class Command(BaseCommand):
    help = "Flushes the Django cache."

    def handle(self, *args, **options):
        clear_django_cache()            
