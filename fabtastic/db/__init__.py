from django.conf import settings
from fabtastic.db import util

db_engine = util.get_db_setting('ENGINE')

if 'postgresql_psycopg2' in db_engine:
    from fabtastic.db.postgres import *
else:
    print("Fabtastic WARNING: DB engine '%s' is not supported" % db_engine)
