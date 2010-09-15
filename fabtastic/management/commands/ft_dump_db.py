import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from fabtastic import db

class Command(BaseCommand):
    args = '[<output_file_path>]'
    help = 'Dumps a SQL backup of your entire DB. Defaults to CWD.'
                        
    def get_dump_path(self):
        """
        Determines the path to write the SQL dump to. Depends on whether the
        user specified a path or not.
        """
        if len(self.args) > 0:
            return self.args[0]
        else:
            dump_filename = db.util.get_db_dump_filename()
            return os.path.join(os.getcwd(), dump_filename)
        
    def handle(self, *args, **options):
        """
        Handle raw input.
        """
        self.args = args
        self.options = options
        
        # Get DB settings from settings.py.
        database = db.util.get_db_setting_dict()
        # Figure out where to dump the file to.
        dump_path = self.get_dump_path()

        # Run the db dump.
        db.dump_db_to_file(dump_path, database)