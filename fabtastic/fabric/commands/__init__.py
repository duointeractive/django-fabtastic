from fabtastic.fabric.commands.c_common import *
from fabtastic.fabric.commands.c_git import *
from fabtastic.fabric.commands.c_s3cmd import *

try:
    import mediasync
    from fabtastic.fabric.commands.c_mediasync import *
except ImportError:
    pass

try:
    import south
    from fabtastic.fabric.commands.c_south import *
except ImportError:
    pass

try:
    import gunicorn
    from fabtastic.fabric.commands.c_gunicorn import *
except ImportError:
    pass

try:
    import celery
    from fabtastic.fabric.commands.c_celery import *
except ImportError:
    pass

# Used to prevent double migrations.
env.already_db_migrated = False
env.already_media_synced = False