from fabric.api import *
from fabtastic.fabric.util import _current_host_has_role

def gunicorn_restart_workers():
    """
    Reloads gunicorn. This must be done to re-compile the code after a new
    revision has been checked out.
    """
    if _current_host_has_role('webapp_servers'):
        print("=== RESTARTING GUNICORN WORKERS ===")
        with cd(env.REMOTE_CODEBASE_PATH):
            run("workon %s && ./manage.py ft_gunicorn_restart" % env.REMOTE_VIRTUALENV_NAME)
        print("Gunicorn reloaded")