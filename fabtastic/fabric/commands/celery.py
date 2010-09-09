from fabric.api import *
from fabtastic.fabric.util import _current_host_has_role

def celeryd_restart(roles='webapp_servers'):
    """
    Reloads celeryd. This must be done to re-compile the code after a new
    revision has been checked out.
    """
    if _current_host_has_role(roles):
        print("=== RESTARTING CELERY DAEMON ===")
        with cd(env.REMOTE_CODEBASE_PATH):
            run("./manage.py ft_celeryd_restart")