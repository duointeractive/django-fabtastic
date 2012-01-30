"""
Utilities for syncing your virtualenv to requirements.txt.
"""
import pkg_resources

class RequirementsParser(object):
    def __init__(self, path):
        self.path = path

    def parse(self):
        fobj = open(self.path, 'r')
        lines = fobj.readlines()
        req_packages = {}
        for line in lines:
            line = line.rstrip()
            if not line or line.startswith('git+') or not line[0].isalpha():
                continue

            equal_split = line.split('==', 1)
            pkg_name = equal_split[0]
            if len(equal_split) == 2:
                req_packages[pkg_name] = equal_split[1]
            else:
                req_packages[pkg_name] = None

        return req_packages


def compare_reqs_to_env(requirements_path):
    local_packages = {}
    for package in pkg_resources.working_set:
        local_packages[package.project_name] = package.version

    parser = RequirementsParser(requirements_path)
    req_packages = parser.parse()

    missing_pkgs = []
    wrong_version_pkgs = []
    for key, val in req_packages.items():
        if not local_packages.has_key(key):
            missing_pkgs.append(key)
            continue

        if val and val != local_packages[key]:
            wrong_version_pkgs.append((key, val, local_packages[key]))

    #print "MISSING"
    #print missing_pkgs
    #print "WRONG VERSION"
    #print wrong_version_pkgs
    return missing_pkgs, wrong_version_pkgs
