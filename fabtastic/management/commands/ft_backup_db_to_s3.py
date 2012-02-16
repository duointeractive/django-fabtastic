import os
import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

from fabtastic import db
from fabtastic.util.aws import get_s3_connection

class Command(BaseCommand):
    help = 'Backs the DB up to S3.'

    def handle(self, *args, **options):
        db_alias = getattr(settings, 'FABTASTIC_DIRECT_TO_DB_ALIAS', 'default')
        # Get DB settings from settings.py.
        database = db.util.get_db_setting_dict(db_alias=db_alias)
        # Generate a temporary DB dump filename.      
        dump_filename = db.util.get_db_dump_filename(db_alias=db_alias)
        # Carry out the DB dump.
        dump_file_path = db.dump_db_to_file(dump_filename, database)

        print "Uploading to S3."
        conn = get_s3_connection()
        bucket = conn.create_bucket(settings.S3_DB_BACKUP['BUCKET'])
        now = datetime.datetime.now()
        s3_path = '%d/%d/%d/%s' % (
            now.year,
            now.month,
            now.day,
            dump_filename,
        )
        key = bucket.new_key(s3_path)
        key.set_contents_from_filename(dump_file_path)
        bucket.copy_key(
            'latest_db.sql.tar.bz2',
            settings.S3_DB_BACKUP['BUCKET'],
            s3_path,
        )
        print "S3 DB backup complete."

        # Clean up the temporary download file.
        os.remove(dump_filename)
