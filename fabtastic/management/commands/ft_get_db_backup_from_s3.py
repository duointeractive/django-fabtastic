from django.core.management.base import BaseCommand
from django.conf import settings

from fabtastic.util.aws import get_s3_connection

class Command(BaseCommand):
    help = 'Retrieves the latest backup from S3.'

    def handle(self, *args, **options):
        download_key = 'latest_db.sql.tar.bz2'
        
        conn = get_s3_connection()
        bucket = conn.create_bucket(settings.S3_DB_BACKUP['BUCKET'])
        key = bucket.new_key(download_key)

        print "Downloading %s DB backup from S3." % download_key
        fobj = open(download_key, 'w')
        key.get_contents_to_file(fobj)

        print "S3 DB backup download complete."
