from fabric.api import *
from fabtastic.fabric.util import _current_host_has_role

def south_migrate():
    """
    Migrates the DB schema with South. Sets already_db_migrated to prevent
    double migrations.
    """
    if _current_host_has_role('webapp_servers') and not env.already_db_migrated:
        print("=== RUNNING SOUTH DB MIGRATIONS ===")
        with cd(env.REMOTE_CODEBASE_PATH):
            run("workon %s && ./manage.py migrate" % env.REMOTE_VIRTUALENV_NAME)
        env.already_db_migrated = True