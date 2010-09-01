import os
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from fabtastic import db

class Command(BaseCommand):
    args = '[<output_file_path>]'
    help = 'Dumps a SQL backup of your entire DB. Defaults to CWD.'
            
    def _set_db_values(self):
        self.db_name = db.util.get_db_setting('NAME')
        self.db_user = db.util.get_db_setting('USER')
        self.db_password = db.util.get_db_setting('PASSWORD')
            
    def _set_dump_path(self):
        if len(self.args) > 0:
            self.dump_path = self.args[0]
        else:
            today = datetime.today()
            db_filename = "%s-%s.sql" %  (self.db_name, today.strftime("%Y%m%d-%H%M"));
            self.dump_path = os.path.join(os.getcwd(), db_filename)
        
    def handle(self, *args, **options):
        self.args = args
        self.options = options


        db.set_pgpass(self.db_name, self.db_user, self.db_password, 
                      db_host="*", db_port="*")
        self._set_dump_path()