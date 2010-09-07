from fabric.api import *
from fabtastic import db

def staging():
    """
    Sets env.hosts to the first staging server.
    """
    env.hosts = [env.roledefs['staging_servers'][0]]
    
def get_remote_db():
    """
    Retrieves a remote DB dump, wipes your local DB, and installs the
    remote copy in place.
    """
    dump_filename = db.util.get_db_dump_filename()
    
    with cd(env.REMOTE_CODEBASE_PATH):
        run("workon %s && ./manage.py ft_dump %s" % (
            env.REMOTE_VIRTUALENV_NAME,
            dump_filename))