import os
import stat
from subprocess import Popen, PIPE

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

def backup_to_tmp(dump_path, database, no_password_prompt=False):
    """
    Backs up the current ligonier DB to a .gz file, stashed in /tmp/.
    
    Returns a tuple in the format of (filename, full_file_path). For example: 
    
        (ligonier-<dtime>.sql.gz, /tmp/ligonier-<dtime.sql.gz)
        
    You will probably want to run _remove_tmp_backup(db_filepath) after doing
    whatever you need to do with the file.
    """
    # Set a .pgpass file up so we're not prompted for a password.
    set_pgpass(database)
    
    cmd = ['pg_dump', '-i']
    
    if database['HOST'] is not '':
        cmd.append('--host=%s' % database['HOST'])
        
    if database['PORT'] is not '':
        cmd.append('--port=%s' % database['PORT'])
        
    if no_password_prompt:
        cmd.append('--no-password')
        
    cmd.append('--username=%s' % database['USER'])
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
    