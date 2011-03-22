from fabric.api import *
from fabtastic.fabric.util import _current_host_has_role

def celeryd_restart(roles='webapp_servers'):
    """
    Reloads celeryd. This must be done to re-compile the code after a new
    revision has been checked out.
    
    NOTE: This broadcasts a 'shutdown' call to all celery workers. You must have
    supervisor or something running to start them back up, or this ends up
    just being a shutdown (sans restart).
    """
    if _current_host_has_role(roles):
        print("=== RESTARTING CELERY DAEMON ===")
        with cd(env.REMOTE_CODEBASE_PATH):
            run("./manage.py ft_celeryd_restart")
            print "Celery shutdown broadcasted, workers restarting."
