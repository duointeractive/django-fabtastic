from fabric.api import *
from fabtastic.fabric.util import _current_host_has_role

def mediasync_with_s3(roles='webapp_servers'):
    """
    Syncs the checked out git media with S3.
    """
    if _current_host_has_role(roles) and not env.already_media_synced:
        print("=== SYNCING STATIC MEDIA WITH S3 ===")
        with cd(env.REMOTE_CODEBASE_PATH):
            run("workon %s && ./manage.py syncmedia" % env.REMOTE_VIRTUALENV_NAME)
        env.already_media_synced = True