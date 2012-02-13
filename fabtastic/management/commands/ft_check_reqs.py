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
                print ' %s==%s in reqs.txt, but %s==%s local' % (
                    pkg_name,
                    req_version,
                    pkg_name,
                    local_version
                )

        if missing_pkgs:
            print "==== Missing (locally) packages ===="
            for pkg_name in missing_pkgs:
                print ' %s' % pkg_name

        if not wrong_version_pkgs and not missing_pkgs:
            print "Your local environment is up to date, good job."