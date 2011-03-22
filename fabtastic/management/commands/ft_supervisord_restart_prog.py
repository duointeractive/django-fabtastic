from subprocess import call
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Restarts one or all of supervisord's managed programs"

    def handle(self, *args, **options):
        self.args = args
        self.options = options

        cmd = ['supervisorctl', 'restart']

        if self.args:
            cmd.append(self.args[0])
        else:
            cmd.append('all')

        call(cmd)
