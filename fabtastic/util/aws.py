"""
Amazon AWS-related utils.
"""
import boto
from django.conf import settings

def get_s3_connection():
    """
    Returns an S3Connection object. Uses values from fabfile.env for creds.
    """
    conf = settings.S3_DB_BACKUP
    return boto.connect_s3(conf['AWS_ACCESS_KEY_ID'],
                           conf['AWS_SECRET_ACCESS_KEY'])
