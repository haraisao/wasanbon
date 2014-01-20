import os, sys, optparse, getpass
import wasanbon
import wasanbon.core.package as pack
from  wasanbon.core.package import workspace
from wasanbon.core import repositories

def _create(args, verbose, force, clean):
    wasanbon.arg_check(args, 4)
    sys.stdout.write(' @ Creating package %s\n' % args[3])
    _package = pack.create_package(args[3], verbose=verbose)

def _unregister(args, verbose, force, clean):
    wasanbon.arg_check(args, 4)
    sys.stdout.write(' @ Removing workspace %s\n' % args[3])
    dic = workspace.load_workspace()
    if not args[3] in dic.keys():
        sys.stdout.write(' - Can not find package %s\n' % args[3])
        return
    try:
        _package = pack.get_package(args[3], verbose=verbose)
        _package.unregister(verbose=verbose, clean=clean)
    except wasanbon.PackageNotFoundException, ex:
        sys.stdout.write(' - Package Not Found (%s).\n' % args[3])
        from wasanbon import util
        if util.yes_no('Do you want to remove the record?') == 'yes':
            dic = workspace.load_workspace()
            dic.pop(args[3])
            workspace.save_workspace(dic)
            sys.stdout.write(' - Removed.\n')

def _list(args, verbose, force ,clean):
    sys.stdout.write(' @ Listing packages.\n')
    _packages = pack.get_packages(verbose=verbose)
    for _package in _packages:
        sys.stdout.write(' ' + _package.name + ' '*(10-len(_package.name)) + ':' + _package.path + '\n')

def _clone(args, verbose, force, clean):
    wasanbon.arg_check(args,4)
    sys.stdout.write(' @ Cloning Package from Repository %s\n' % args[3])
    repo = pack.get_repository(args[3], verbose=verbose)
    _package = repo.clone(verbose=verbose)


def _fork(args, verbose, force ,clean):
    wasanbon.arg_check(args, 4)
    sys.stdout.write(' @ Forking Package from Repository %s\n' % args[3])
    user, passwd = wasanbon.user_pass()
    original_repo = pack.get_repository(args[3], verbose=verbose)
    repo = original_repo.fork(user, passwd, verbose=verbose)
    _package = repo.clone(verbose=verbose)

                
class Command(object):
    def __init__(self):
        pass

    def alternative(self):
        return ['create', 'unregister', 'list', 'directory', 'repository', 'clone', 'fork', 'diff']
    
    def execute_with_argv(self, args, verbose, force, clean):
        wasanbon.arg_check(args, 3)

        if '-l' in args:
            long_option = True
        else:
            long_option = False
        args = [arg for arg in args if not arg is '-l']

        if args[2] == 'create':
            _create(args, verbose, force ,clean)

        elif args[2] == 'unregister':
            _unregister(args, verbose, force, clean)

        elif args[2] == 'list':
            _list(args, verbose, force, clean)

        elif args[2] == 'directory':
            try:
                _package = pack.get_package(args[3].strip())
                print _package.path
            except:
                print '.'

        elif args[2] == 'repository':

            if len(args) == 3: # list
                args.append('list')
                pass

            if args[3] == 'list':
                sys.stdout.write(' @ Listing Package Repositories\n')
                #rtcs, packs = repositories.load_repositories(verbose=verbose)
                repos = pack.get_repositories(verbose=verbose)
                for repo in repos:
                    print_repository(repo, long=long_option)
            elif args[3] == 'create':
                (username, passwd) = wasanbon.user_pass()
                sys.stdout.write('  - Input repository name :')
                repo_name = raw_input()
                repositories.create_local_repository(username, passwd, repo_name, verbose=verbose)
            elif args[3] == 'update':
                sys.stdout.write(' @ Updating Package Repositories\n')
                pack.update_repositories(verbose=verbose)
            elif args[3] == 'clone':
                wasanbon.arg_check(args,5)
                sys.stdout.write(' @ Cloning Package Repositories\n')
                pack.update_repositories(verbose=verbose, url=args[4])


        elif args[2] == 'clone':
            _clone(args, verbose, force, clean)

        elif args[2] == 'fork':
            _fork(args, verbose, force, clean)

        elif args[2] == 'diff':
            wasanbon.arg_check(args, 5)
            sys.stdout.write(' @ Diff between %s and %s\n' % (args[3], args[4]))
            repo1 = pack.get_package(args[3], verbose=verbose)
            repo2 = pack.get_package(args[4], verbose=verbose)
            diff = pack.diff(repo1, repo2)
            print_diff(diff)


        else:
            raise wasanbon.InvalidUsageException()

def print_repository(repo, long=False):

    if long:
        sys.stdout.write('    - ' + repo.name + '\n')
        sys.stdout.write('       - description : ' + repo.description + '\n')
        sys.stdout.write('       - url         : ' + repo.url + '\n')

    else:
        sys.stdout.write('    - ' + repo.name + ' ' * (24-len(repo.name)) + ' : ' + repo.description + '\n')

def print_diff(diff):
    [plus, minus] = diff.rtcs
    sys.stdout.write(' - RTC\n')
    for rtc in plus:
        sys.stdout.write('  + %s\n' % rtc.name)
    for rtc in minus:
        sys.stdout.write('  - %s\n' % rtc.name)

