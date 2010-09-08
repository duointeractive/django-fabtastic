from fabric.api import *

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