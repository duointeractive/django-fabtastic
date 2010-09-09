import os
import signal

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from fabric.api import *
import fabfile

class Command(BaseCommand):
    help = 'Restarts gunicorn workers after code changes.'

    def handle(self, *args, **options):
        pid_path = env.GUNICORN_PID_PATH
        if os.path.exists(pid_path):
            pid = int(open(pid_path, 'r').read())
            os.kill(pid, signal.SIGHUP)
        else:
            raise CommandError("No gunicorn process running.")