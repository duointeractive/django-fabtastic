from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Restarts all celery daemons.'

    def handle(self, *args, **options):
        try:
            from celery.task.control import broadcast
        except ImportError:
            raise CommandError("Celery is not currently installed.")
        
        # Shut them all down.
        broadcast("shutdown")