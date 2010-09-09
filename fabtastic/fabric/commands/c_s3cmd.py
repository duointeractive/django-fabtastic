import sys
import os
from fabric.api import *
from fabtastic import db
from fabtastic.fabric.util import _current_host_has_role
       
def backup_db_to_s3():
    """
    Backs up the DB to Amazon S3. The DB server runs pg_dump,
    then uploads to S3 via the s3cmd command. On new DB instances, you'll need
    to run 's3cmd --configure' (as the user that will be running s3cmd) to setup 
    the keys. You'll notice they aren't passed here as a result of that.
    """
    if _current_host_has_role('webapp_servers'):
        dump_filename = db.util.get_db_dump_filename()
        dump_path = os.path.join(env.REMOTE_CODEBASE_PATH, dump_filename)
        
        with cd(env.REMOTE_CODEBASE_PATH):
            run("workon %s && ./manage.py ft_dump_db %s" % (
                env.REMOTE_VIRTUALENV_NAME,
                dump_filename))
            # Now upload via s3cmd. See note above about s3cmd --configure.
            run("s3cmd put %s s3://ligonier-db-backup/%s" % (dump_path, dump_filename))
            run("rm %s" % dump_filename)
        
        # Die after this to prevent executing this with more hosts.
        sys.exit(0)