from subprocess import call
from django.core.management.base import BaseCommand
from fabric.api import *
import fabfile

class Command(BaseCommand):
    help = "Updates your virtualenv from requirements.txt."

    def handle(self, *args, **options):
        pip_req_path = env.PIP_REQUIREMENTS_PATH
        cmd = ['pip', 'install', '--upgrade', '-r', pip_req_path]
        call(cmd)        
