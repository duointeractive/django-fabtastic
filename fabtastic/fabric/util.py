from fabric.api import *

def _current_host_has_role(roles):
    """
    Looks to see if the host the current task is being executed on has
    the specified role.
    """
    if len(env.roledefs) is 0 and env.hosts:
        # No roledefs defined, but env.hosts is. If we set env.hosts, assume
        # that the operation should be done to everything in env.hosts.
        return True

    # Otherwise check the role list for the current host in env.
    if isinstance(roles, basestring):
        # roles is a string.
        return env['host_string'] in env.roledefs.get(roles, [])
    else:
        # roles is a list of roles.
        for role in roles:
            if env['host_string'] in env.roledefs.get(role, []):
                return True
        return False