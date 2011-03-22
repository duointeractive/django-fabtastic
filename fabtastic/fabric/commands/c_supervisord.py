from fabric.api import *
from fabtastic.fabric.util import _current_host_has_role

def supervisord_restart_all(roles='webapp_servers'):
    """
    Restarts all of supervisord's managed programs.
    """
    if _current_host_has_role(roles):
        print("=== RESTARTING SUPERVISORD PROGRAMS ===")
        with cd(env.REMOTE_CODEBASE_PATH):
            run("workon %s && ./manage.py ft_supervisord_restart_prog" % env.REMOTE_VIRTUALENV_NAME)

def supervisord_restart_prog(program, roles='webapp_servers'):
    """
    Restarts all of supervisord's managed programs.
    
    :arg str program: The name of the program to restart (as per supervisor's
        conf.d/ contents).
    """
    if _current_host_has_role(roles):
        print("=== RESTARTING SUPERVISORD PROGRAMS ===")
        with cd(env.REMOTE_CODEBASE_PATH):
            run("workon %s && ./manage.py ft_supervisord_restart_prog %s" % (
                env.REMOTE_VIRTUALENV_NAME, program))
