import os
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
    #dump_filename = "ligonier-2010_09_07-1725.sql.tar.bz2"
    dump_path = os.path.join(env.REMOTE_CODEBASE_PATH, dump_filename)
    
    with cd(env.REMOTE_CODEBASE_PATH):
        run("workon %s && ./manage.py ft_dump_db %s" % (
            env.REMOTE_VIRTUALENV_NAME,
            dump_filename))
        get(dump_path, dump_filename)
        run("rm %s" % dump_filename)

    local('./manage.py ft_restore_db %s' % dump_filename, capture=False)
    local('rm %s' % dump_filename)
        
def testit():
    output = local('./manage.py ft_dump_db woot', capture=False)
    print "OUTPUT", output