from django.core.management.base import BaseCommand
from fabric.api import *
import fabfile
from fabtastic.util.req_syncer import compare_reqs_to_env

class Command(BaseCommand):
    help = "Compares your current virtualenv to requirements.txt."

    def handle(self, *args, **options):
        missing_pkgs, wrong_version_pkgs = compare_reqs_to_env(env.PIP_REQUIREMENTS_PATH)

        if wrong_version_pkgs:
            print "==== Version mis-matches ===="
            for pkg_tuple in wrong_version_pkgs:
                pkg_name, req_version, local_version = pkg_tuple
                print ' %s %s -> %s' % (pkg_name, req_version, local_version)

        if missing_pkgs:
            print "==== Missing packages ===="
            for pkg_name in missing_pkgs:
                print ' %s' % pkg_name