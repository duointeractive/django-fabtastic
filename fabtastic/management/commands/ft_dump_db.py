import os
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from fabtastic import db

class Command(BaseCommand):
    args = '[<output_file_path>]'
    help = 'Dumps a SQL backup of your entire DB. Defaults to CWD.'
                        
    def _set_dump_path(self):
        """
        Determines the path to write the SQL dump to. Depends on whether the
        user specified a path or not.
        """
        if len(self.args) > 0:
            self.dump_path = self.args[0]
        else:
            today = datetime.today()
            self.dump_filename = "%s-%s.sql.tar.bz2" %  (
                self.DATABASE['NAME'], 
                today.strftime("%Y_%m_%d-%H%M"),
            )
            self.dump_path = os.path.join(os.getcwd(), self.dump_filename)
        
    def handle(self, *args, **options):
        """
        Handle raw input.
        """
        self.args = args
        self.options = options
        
        # Get DB settings from settings.py.
        self.DATABASE = db.util.get_db_setting_dict()
        # Figure out where to dump the file to.
        self._set_dump_path()

        # Run the db dump.
        db.backup_to_tmp(self.dump_path, self.DATABASE)