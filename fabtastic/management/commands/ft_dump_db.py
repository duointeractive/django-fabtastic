import os
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from fabtastic import db

class Command(BaseCommand):
    args = '[<output_file_path>]'
    help = 'Dumps a SQL backup of your entire DB. Defaults to CWD.'
            
    def _set_db_values(self):
        """
        Set some variables from settings.py.
        """
        self.db_name = db.util.get_db_setting('NAME')
        self.db_user = db.util.get_db_setting('USER')
        self.db_password = db.util.get_db_setting('PASSWORD')
        self.db_host = db.util.get_db_setting('HOST')
        self.db_port = db.util.get_db_setting('PORT')

        # Put these back together in Django 1.2 format for convenience.
        self.DATABASE = {'NAME': self.db_name,
                         'USER': self.db_user,
                         'PASSWORD': self.db_password,
                         'HOST': self.db_host,
                         'PORT': self.db_port}
            
    def _set_dump_path(self):
        """
        Determines the path to write the SQL dump to. Depends on whether the
        user specified a path or not.
        """
        if len(self.args) > 0:
            self.dump_path = self.args[0]
        else:
            today = datetime.today()
            self.dump_filename = "%s-%s.sql" %  (self.db_name, 
                                                 today.strftime("%Y%m%d-%H%M"))
            self.dump_path = os.path.join(os.getcwd(), self.dump_filename)
        
    def handle(self, *args, **options):
        """
        Handle raw input.
        """
        self.args = args
        self.options = options

        self._set_db_values()
        self._set_dump_path()

        db.set_pgpass(self.DATABASE)
        
        db.backup_to_tmp(self.dump_path, self.DATABASE)