from subprocess import call
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Restarts all of supervisord's managed programs"

    def handle(self, *args, **options):
        cmd = ['supervisorctl', 'restart', 'all']
        call(cmd)
