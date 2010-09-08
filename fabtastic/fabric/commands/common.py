import os
import sys
from fabric.api import *
from fabtastic import db
from fabtastic.fabric.util import _current_host_has_role
   
def get_remote_db():
    """
    Retrieves a remote DB dump, wipes your local DB, and installs the
    remote copy in place.
    """
    if _current_host_has_role('webapp_servers'):
        dump_filename = db.util.get_db_dump_filename()
        dump_path = os.path.join(env.REMOTE_CODEBASE_PATH, dump_filename)
        
        with cd(env.REMOTE_CODEBASE_PATH):
            run("workon %s && ./manage.py ft_dump_db %s" % (
                env.REMOTE_VIRTUALENV_NAME,
                dump_filename))
            get(dump_path, dump_filename)
            run("rm %s" % dump_filename)
    
        local('./manage.py ft_restore_db %s' % dump_filename, capture=False)
        local('rm %s' % dump_filename)
        
        # Die after this to prevent executing this with more hosts.
        sys.exit(0)
                
def flush_cache():
    """
    Flushes the cache.
    """
    if _current_host_has_role('webapp_servers'):
        print("=== FLUSHING CACHE ===")
        with cd(env.REMOTE_VIRTUALENV_NAME):
            run("workon %s && ./manage.py ft_clear_cache" % env.REMOTE_VIRTUALENV_NAME)
