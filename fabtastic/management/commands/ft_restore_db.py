from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from fabtastic import db

class Command(BaseCommand):
    args = '[<output_file_path>]'
    help = 'Restores a DB from a SQL dump file.'

    def add_arguments(self, parser):
        parser.add_argument('--force', '-f',
                    action='store_true',
                    dest='prod_override',
                    default=False,
                    help='Override to allow restoring DB in production.'),
        )

    def handle(self, *args, **options):
        """
        Handle raw input.
        """
        self.args = args
        self.options = options

        if len(self.args) < 1:
            raise CommandError("ft_restore_db: You must specify the path to "
                               "the DB dump file to restore from.")

        is_production = getattr(settings, 'IS_PRODUCTION', False)
        has_prod_override = self.options['prod_override']
        if is_production and not has_prod_override:
            raise CommandError("ft_restore_db: Not allowed in production. "
                               "Use -f option to override.")

        # Path to file to restore from.
        dump_path = self.args[0]

        db_alias = getattr(settings, 'FABTASTIC_DIRECT_TO_DB_ALIAS', 'default')
        # Get DB settings from settings.py.
        database_dict = db.util.get_db_setting_dict(db_alias=db_alias)

        # Drop the DB.
        db.drop_db(database_dict)
        # Re-create an empty DB with the same name.
        db.create_db(database_dict)
        # Restore from the DB dump.
        db.restore_db_from_file(dump_path, database_dict)
