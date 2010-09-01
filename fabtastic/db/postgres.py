import os
import stat

def set_pgpass(db_name, db_user, db_pass, db_host="*", db_port="*"):
    """
    Sets the ~/.pgpass file up so that psql and pg_dump doesn't ask 
    for a password.
    """
    pgpass_file = os.path.expanduser('~')
    pgpass_file = os.path.join(pgpass_file, '.pgpass')
    
    fd = open(pgpass_file, 'wb')
    fd.write('*:*:%s:%s:%s' % (db_name, db_user, db_pass))
    fd.close()
    
    perms = [stat.S_IRUSR, stat.S_IWUSR]
    os.chmod(pgpass_file, perms)

def backup_to_tmp():
    """
    Backs up the current ligonier DB to a .gz file, stashed in /tmp/.
    
    Returns a tuple in the format of (filename, full_file_path). For example: 
    
        (ligonier-<dtime>.sql.gz, /tmp/ligonier-<dtime.sql.gz)
        
    You will probably want to run _remove_tmp_backup(db_filepath) after doing
    whatever you need to do with the file.
    """
    print("Backing up database '%s'. This may take a minute or so..." % db_name)
    
    today = datetime.today()
    db_filename = "%s-%s.sql.gz" %  (db_name, today.strftime("%Y%m%d-%H%M"));
    db_filepath = "/tmp/%s" % db_filename
    
    # Set up a ~/.pgpass to avoid password prompts when running pg_dump.
    _set_pgpass()
    run("pg_dump -i -h %s -U %s %s | gzip > %s" % (db_host, db_user, db_name, 
                                                   db_filepath))
    
    return (db_filename, db_filepath)