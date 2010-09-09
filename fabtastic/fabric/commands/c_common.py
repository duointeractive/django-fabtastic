import os
import sys
from fabric.api import *
from fabtastic import db
from fabtastic.fabric.util import _current_host_has_role
   
def get_remote_db(roles='webapp_servers'):
    """
    Retrieves a remote DB dump, wipes your local DB, and installs the
    remote copy in place.
    """
    if _current_host_has_role(roles):
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
                
def flush_cache(roles='webapp_servers'):
    """
    Flushes the cache.
    """
    if _current_host_has_role(roles):
        print("=== FLUSHING CACHE ===")
        with cd(env.REMOTE_VIRTUALENV_NAME):
            run("workon %s && ./manage.py ft_clear_cache" % env.REMOTE_VIRTUALENV_NAME)
            
def pip_update_reqs(roles='webapp_servers'):
    """
    Updates your virtualenv from requirements.txt.
    """
    if _current_host_has_role(roles):
        print("=== UPDATING REQUIREMENTS ===")
        with cd(env.REMOTE_VIRTUALENV_NAME):
            run("workon %s && ./manage.py ft_pip_update_reqs" % env.REMOTE_VIRTUALENV_NAME)

def fabtastic_update(roles='webapp_servers'):
    """
    Updates your copy of django-fabtastic from the git repository.
    """
    if _current_host_has_role(roles):
        print("=== UPDATING FABTASTIC ===")
        with cd(env.REMOTE_VIRTUALENV_NAME):
            run("workon %s && ./manage.py ft_fabtastic_update" % env.REMOTE_VIRTUALENV_NAME)