import os
import stat
from subprocess import Popen, PIPE, call

def set_pgpass(database):
    """
    Sets the ~/.pgpass file up so that psql and pg_dump doesn't ask 
    for a password.
    """
    pgpass_file = os.path.expanduser('~')
    pgpass_file = os.path.join(pgpass_file, '.pgpass')
    
    db_host = database['HOST']
    db_port = database['PORT']
    db_name = database['NAME']
    db_user = database['USER']
    db_pass = database['PASSWORD']
    
    if db_host is '':
        db_host = "*"
    if db_port is '':
        db_port = "*"
    
    fd = open(pgpass_file, 'wb')
    # host:port:database:username:password
    fd.write('%s:%s:%s:%s:%s' % (db_host, db_port, db_name, db_user, db_pass))
    fd.close()
    
    perms = stat.S_IRUSR | stat.S_IWUSR
    os.chmod(pgpass_file, perms)
    
def add_common_options_to_cmd(cmd, database, no_password_prompt=False,
                              **kwargs):
    """
    Adds some commonly used options to the given command string. psql,
    pg_dump, pg_restore, and a few others have some flags in common.
    
    cmd: (list) A command list, in format for Popen/call().
    """
    if database['HOST'] is not '':
        cmd.append('--host=%s' % database['HOST'])
        
    if database['PORT'] is not '':
        cmd.append('--port=%s' % database['PORT'])
        
    if no_password_prompt:
        cmd.append('--no-password')
        
    cmd.append('--username=%s' % database['USER'])

def dump_db_to_file(dump_path, database, **kwargs):
    """
    pg_dumps the specified database to a given path. Passes output through
    bzip2 for compression.
    
    dump_path: (str) Complete path (with filename) to pg_dump out to.
    database: (dict) Django 1.2 style DATABASE settings dict.
    no_password_prompt: (bool) When True, never prompt for password, and fail
                               if none is provided by env variables or .pgpass.
                               
    Returns the path that was dumped to.
    """
    # Set a .pgpass file up so we're not prompted for a password.
    set_pgpass(database)
    
    cmd = ['pg_dump', '-i']
    
    # Add some common postgres options.
    add_common_options_to_cmd(cmd, database, **kwargs)
        
    cmd.append('--format=tar')
    cmd.append(database['NAME'])
    
    print "pg_dumping database '%s' to %s" % (database['NAME'], dump_path)
    
    # Run pg_dump
    db_dump = Popen(cmd, stdout=PIPE)
    # Open the eventual .tar.bz2 file for writing by bzip2.
    tfile = open(dump_path, 'w')
    # Use bzip2 to dump into the open file handle via stdout.
    db_bzip = Popen(['bzip2'], stdin=db_dump.stdout, stdout=tfile)
    db_bzip.wait()
    tfile.close()
    
    print "Database dump complete."
    
    return dump_path

def drop_db(database, **kwargs):
    """
    Drops the specified database.
    """
    # Set a .pgpass file up so we're not prompted for a password.
    set_pgpass(database)
    
    cmd = ['dropdb']
    
    # Add some common postgres options.
    add_common_options_to_cmd(cmd, database, **kwargs)
    
    cmd.append(database['NAME'])
    
    print cmd
    
    call(cmd)

def restore_db_from_file(dump_path, database, **kwargs):
    """
    Restores the specified database from a pg_dump file.
    
    dump_path: (str) Complete path (with filename) to pg_restore from.
    database: (dict) Django 1.2 style DATABASE settings dict.
    """
    # Set a .pgpass file up so we're not prompted for a password.
    set_pgpass(database)
    
    cmd = ['pg_restore', '-i']
    
    # Add some common postgres options.
    add_common_options_to_cmd(cmd, database, **kwargs)

    cmd.append('--format=tar')
    cmd.append(dump_path)
    
    call(cmd)