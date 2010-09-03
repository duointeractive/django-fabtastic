import os
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from fabtastic import db

class Command(BaseCommand):
    args = '[<output_file_path>]'
    help = 'Restores a DB from a SQL dump file.'
                               
    def handle(self, *args, **options):
        """
        Handle raw input.
        """
        self.args = args
        self.options = options
        
        if len(self.args) < 1:
            raise CommandError('You must specify the path to the DB dump file to restore from.')

        # Path to file to restore from.
        dump_path = self.args[0]
        
        # Get DB settings from settings.py.
        database_dict = db.util.get_db_setting_dict()

        # Run the db dump.
        db.drop_db(database_dict)
        #db.restore_db_from_file(dump_path, self.DATABASE)