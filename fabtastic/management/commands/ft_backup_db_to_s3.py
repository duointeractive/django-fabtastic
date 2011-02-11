import os

from django.core.management.base import BaseCommand
from django.conf import settings

from fabtastic import db
from fabtastic.util.aws import get_s3_connection

class Command(BaseCommand):
    help = 'Backs the DB up to S3. Make sure to run s3cmd --configure.'

    def handle(self, *args, **options):
        # Get DB settings from settings.py.
        database = db.util.get_db_setting_dict()
        # Generate a temporary DB dump filename.      
        dump_filename = db.util.get_db_dump_filename()
        # Carry out the DB dump.
        dump_file_path = db.dump_db_to_file(dump_filename, database)

        print "Uploading to S3."
        conn = get_s3_connection()
        bucket = conn.create_bucket(settings.S3_DB_BACKUP['BUCKET'])
        key = bucket.new_key(dump_filename)
        key.set_contents_from_filename(dump_file_path)
        print "S3 DB backup complete."

        # Clean up the temporary download file.
        os.remove(dump_filename)
