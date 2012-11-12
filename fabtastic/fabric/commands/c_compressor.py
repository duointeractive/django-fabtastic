from fabric.api import *
from fabtastic.fabric.util import _current_host_has_role

def compress(roles='webapp_servers'):
    """
    Runs django-compressor's offline compression command.
    """
    if _current_host_has_role(roles):
        print("=== COMPRESSING STATIC MEDIA ===")
        with cd(env.REMOTE_CODEBASE_PATH):
            run("workon %s && ./manage.py compress --force" % env.REMOTE_VIRTUALENV_NAME)