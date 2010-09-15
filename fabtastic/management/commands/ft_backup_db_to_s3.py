import os
from subprocess import call

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from fabric.api import *
from fabtastic import db
import fabfile

class Command(BaseCommand):
    help = 'Backs the DB up to S3. Make sure to run s3cmd --configure.'

    def handle(self, *args, **options):
        # Get DB settings from settings.py.
        database = db.util.get_db_setting_dict()
        # Generate a temporary DB dump filename.      
        dump_filename = db.util.get_db_dump_filename()
        # Carry out the DB dump.
        db.dump_db_to_file(dump_filename, database)
        
        # Now upload via s3cmd. See note above about s3cmd --configure.
        cmd = ['s3cmd', 'put']
        cmd.append(dump_filename)
        cmd.append('s3://%s/%s' % (env.S3_DB_BACKUP_BUCKET, dump_filename))
        call(cmd)
        
        # Clean up the temporary download file.
        os.remove(dump_filename)
