#from wasanbon.util import git
import os
#import . as git
import wasanbon.util.git 
#from wasanbon.util.git  import git_command

class GitRepositoryNotFoundException(Exception):
    def __init__(self):
        pass


class GitRepository():

    def __init__(self, path, verbose=False, init=False):
        self._path = path
        if not os.path.isdir(os.path.join(path, '.git')):
            if not init:
                raise GitRepositoryNotFoundException()
            self.init(verbose=verbose)

    def init(self, verbose=False):
        wasanbon.util.git.git_command(['init'], verbose=verbose, path=self.path)
        gitignore_files = ['*~', '.pyc', 'build-*', 'system/.metadata/*']
        fout = open('.gitignore', 'w')
        for filename in gitignore_files:
            fout.write(filename + '\n')
        fout.close()
        self.add(['.gitignore'], verbose=verbose)
        first_comment = 'This if first commit. This repository is generated by wasanbon'    
        self.commit(first_comment, verbose=verbose)
        pass

    def add(self, files, verbose=False):
        wasanbon.util.git.git_command(['add'] + files, verbose=verbose, path=self.path)

    @property
    def path(self):
        return self._path

    @property
    def hash(self):
        popen = wasanbon.util.git.git_command(['log', '--pretty=format:"%H"', '-1'], pipe=True)
        popen.wait()
        return popen.stdout.readline().strip()[1:-1]

    def pull(self, verbose=False):
        curdir = os.getcwd()
        os.chdir(self.path)
        wasanbon.util.git.git_command(['pull', 'origin', 'master'], verbose=verbose)
        os.chdir(curdir)
        pass

    def push(self, verbose=False):
        curdir = os.getcwd()
        os.chdir(self.path)
        wasanbon.util.git.git_command(['push', 'origin', 'master'], verbose=verbose)
        os.chdir(curdir)
        pass

    def commit(self, comment,  verbose=False):
        curdir = os.getcwd()
        os.chdir(self.path)
        wasanbon.util.git.git_command(['commit', '-a', '-m', comment], verbose=verbose)
        os.chdir(curdir)
        pass

    def checkout(self, verbose=False, hash=""):
        curdir = os.getcwd()
        os.chdir(self.path)
        if len(hash):
            wasanbon.util.git.git_command(['checkout' 'master', '--force'], verbose=verbose)
        else:
            wasanbon.util.git.git_command(['checkout', hash], verbose=verbose)
        os.chdir(curdir)
        pass

    def change_upstream_pointer(url, verbose=False):
        curdir = os.getcwd()
        os.chdir(self.path)
        filename = os.path.join(distpath, '.git', 'config')
        tempfilename = filename + ".bak"
        if os.path.isfile(tempfilename):
            os.remove(tempfilename)
            pass
        os.rename(filename, tempfilename)

        git_config = open(filename, 'w')
        git_config_bak = open(tempfilename, 'r')
        for line in git_config_bak:
            if line.strip() == '[remote "origin"]':
                line = '[remote "upstream"]\n'
                pass
            git_config.write(line)
            pass
        git_config.write('[remote "origin"]\n')
        git_config.write('       url = %s\n' % url)
        git_config.write('       fetch = +refs/heads/*:refs/remotes/origin/*\n')
        
        git_config.close()
        git_config_bak.close()

        os.chdir(curdir)
