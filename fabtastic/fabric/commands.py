import os
from fabric.api import *
from fabtastic import db

# Used to prevent double migrations.
env.already_db_migrated = False
env.already_media_synced = False
   
def _current_host_has_role(role_str):
    """
    Looks to see if the host the current task is being executed on has
    the specified role.
    """
    if len(env.roledefs) is 0 and env.hosts:
        # No roledefs defined, but env.hosts is. If we set env.hosts, assume
        # that the operation should be done to everything in env.hosts.
        return True
    
    # Otherwise check the role list for the current host in env.
    return env['host_string'] in env.roledefs[role_str] 
   
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
    
def git_pull(roles='webapp_servers'):
    """
    Pulls the latest master branch from the git repo.
    """
    if _current_host_has_role(roles):
        print("=== PULLING FROM GIT ===")
        with cd(env.REMOTE_VIRTUALENV_NAME):
            run("git pull")
            
def mediasync_with_s3():
    """
    Syncs the checked out git media with S3.
    """
    if _current_host_has_role('webapp_servers') and not env.already_media_synced:
        print("=== SYNCING STATIC MEDIA WITH S3 ===")
        with cd(env.REMOTE_VIRTUALENV_NAME):
            run("./manage.py syncmedia")
        env.already_media_synced = True
        
def migrate_db_schema_via_south():
    """
    Migrates the DB schema with South. Sets already_db_migrated to prevent
    double migrations.
    """
    if _current_host_has_role('webapp_servers') and not env.already_db_migrated:
        print("=== RUNNING SOUTH DB MIGRATIONS ===")
        with cd(env.REMOTE_VIRTUALENV_NAME):
            run("workon %s && ./manage.py migrate" % env.REMOTE_VIRTUALENV_NAME)
        env.already_db_migrated = True
        
def flush_cache():
    """
    Flushes the cache.
    """
    if _current_host_has_role('webapp_servers'):
        print("=== FLUSHING CACHE ===")
        with cd(env.REMOTE_VIRTUALENV_NAME):
            run("workon %s && ./manage.py ft_clear_cache" % env.REMOTE_VIRTUALENV_NAME)
            
def reload_gunicorn():
    """
    Reloads gunicorn. This must be done to re-compile the code after a new
    revision has been checked out.
    """
    if _current_host_has_role('webapp_servers'):
        print("=== RESTARTING GUNICORN WEBAPP NODE ===")
        run('killall gunicorn')
        
def deploy():
    """
    Full git deployment. Migrations, reloading gunicorn.
    """
    git_pull()
    migrate_db_schema_via_south()
    reload_gunicorn()
    flush_cache()
    # Un-comment this once we get django-mediasync integrated.
    #_mediasync_with_s3()
    print("-- Deployment complete. --")
    
@roles('webapp_servers')
def deploy_soft():
    """
    Just checkout the latest source, don't reload.
    """
    git_pull()
    print("--- Soft Deployment complete. ---")