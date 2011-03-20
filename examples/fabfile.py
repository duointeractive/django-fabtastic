from __future__ import with_statement
import os

from django.core import management
# We have to re-name this to avoid clashes with fabric.api.settings.
import settings as django_settings
management.setup_environ(django_settings)

from fabric.api import *
# This will import every command, you may need to get more selective if
# you aren't using all of the stuff we do.
# For example:
# from fabtastic.fabric.commands.c_common import *
# from fabtastic.fabric.commands.c_git import git_pull
from fabtastic.fabric.commands import *

"""
Here are some deployment related settings. These can be pulled from your
settings.py if you'd prefer. We keep strictly deployment-related stuff in
our fabfile.py, but you don't have to.
"""
# The path on your servers to your codebase's root directory. This needs to
# be the same for all of your servers. Worse case, symlink away.
env.REMOTE_CODEBASE_PATH = '/home/account/codebase'
# Path relative to REMOTE_CODEBASE_PATH.
env.PIP_REQUIREMENTS_PATH = 'requirements.txt'
# The standardized virtualenv name to use.
env.REMOTE_VIRTUALENV_NAME = 'your_virtualenv'

# This is used for reloading gunicorn processes after code updates.
# Only needed for gunicorn-related tasks.
env.GUNICORN_PID_PATH = os.path.join(env.REMOTE_CODEBASE_PATH, 'gunicorn.pid')

def staging():
    """
    Sets env.hosts to the sole staging server. No roledefs means that all
    deployment tasks get ran on every member of env.hosts.
    """
    env.hosts = ['staging.example.org']

def prod():
    """
    Set env.roledefs according to our deployment setup. From this, an
    env.hosts list is generated, which determines which hosts can be
    messed with. The roledefs are only used to determine what each server is.
    """
    # Nginx proxies.
    env.roledefs['proxy_servers'] = ['proxy1.example.org']
    # The Django + gunicorn app servers.
    env.roledefs['webapp_servers'] = ['app1.example.org']
    # Static media servers
    env.roledefs['media_servers'] = ['media1.example.org']
    # Postgres servers.
    env.roledefs['db_servers'] = ['db1.example.org']

    # Combine all of the roles into the env.hosts list.
    env.hosts = [host[0] for host in env.roledefs.values()]

def deploy():
    """
    Full git deployment. Migrations, reloading gunicorn.
    """
    git_pull()
    south_migrate()
    gunicorn_restart_workers()
    flush_cache()
    # Un-comment this if you have mediasync installed to sync on deploy.
    #mediasync_syncmedia()

def deploy_soft():
    """
    Just checkout the latest source, don't reload.
    """
    git_pull()
    print("--- Soft Deployment complete. ---")
