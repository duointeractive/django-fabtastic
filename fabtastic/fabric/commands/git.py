from fabric.api import *
from fabtastic.fabric.util import _current_host_has_role

def git_pull(roles='webapp_servers'):
    """
    Pulls the latest master branch from the git repo.
    """
    if _current_host_has_role(roles):
        print("=== PULLING FROM GIT ===")
        with cd(env.REMOTE_CODEBASE_PATH):
            run("git pull")