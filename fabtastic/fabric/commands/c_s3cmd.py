import sys
from fabric.api import *
from fabtastic.fabric.util import _current_host_has_role
       
def backup_db_to_s3():
    """
    Backs up the DB to Amazon S3. The DB server runs pg_dump,
    then uploads to S3 via the s3cmd command. On new DB instances, you'll need
    to run 's3cmd --configure' (as the user that will be running s3cmd) to setup 
    the keys. You'll notice they aren't passed here as a result of that.
    """
    if _current_host_has_role('webapp_servers'):        
        print("=== BACKING UP DB TO S3 ===")
        with cd(env.REMOTE_CODEBASE_PATH):
            run("workon %s && ./manage.py ft_backup_db_to_s3" % env.REMOTE_VIRTUALENV_NAME)
        print("DB backed up to S3.")
        
        # Die after this to prevent executing this with more hosts.
        sys.exit(0)