from django.core.management.base import BaseCommand, CommandError
from celery.task.control import broadcast

class Command(BaseCommand):
    help = 'Restarts all celery daemons.'

    def handle(self, *args, **options):
        # Shut them all down.
        broadcast("shutdown")