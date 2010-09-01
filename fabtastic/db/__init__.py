from django.conf import settings
from fabtastic.db import util

db_engine = util.get_db_setting('ENGINE')

if db_engine in ['postgresql_psycopg2', 'postgresql']:
    from fabtastic.db.postgres import *
else:
    raise NotImplementedError("Fabtastic: DB engine '%s' is not supported" % db_engine)