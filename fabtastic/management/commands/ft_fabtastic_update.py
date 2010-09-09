from subprocess import call
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Updates your copy of Fabtastic to the latest from git."

    def handle(self, *args, **options):
        fabtastic_repo = 'git+http://github.com/duointeractive/django-fabtastic.git#egg=fabtastic'
        cmd = ['pip', 'install', '--upgrade', fabtastic_repo]
        call(cmd)        
