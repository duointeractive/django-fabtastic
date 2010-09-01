import os
import stat
from subprocess import call

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
    
    if db_host is not '':
        db_host = "*"
    if db_port is not '':
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
    #print("Backing up database '%s'. This may take a minute or so..." % db_name)
    print "DAT", database
    
    cmd = ['pg_dump', '-i']
    
    if database['HOST'] is not '':
        cmd.append('--host=%s' % database['HOST'])
        
    if database['PORT'] is not '':
        cmd.append('--port=%s' % database['PORT'])
        
    if no_password_prompt:
        cmd.append('--no-password')
        
    cmd.append('--username=%s' % database['USER'])
    cmd.append('--file=%s' % dump_path)
    cmd.append('--format=tar')
    cmd.append(database['NAME'])
    
    print cmd
    call(cmd)
    
    print "pg_dumping to %s" % dump_path
    
    """
    run("pg_dump -i -h %s -U %s %s | gzip > %s" % (database['HOST'], 
                                                   database['USER'],
                                                   database['NAME'],
                                                   database['PORT'], 
                                                   dump_path))
    """
    #run("pg_dump -i -h %s -U %s %s | gzip > %s" % (db_host, db_user, db_name, 
    #                                               db_filepath))