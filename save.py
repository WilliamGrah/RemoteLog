import datetime
import git
import os
import sys


class Saver():
    def __init__(self, repo_name = None):
        self.repo_name = repo_name
        self.repo = None

    def get_repository(self, path, user=None, password=None, repo=None):
        if repo == None and self.repo_name != None:
            repo = self.repo_name
        else:
            print('No repository to use !')
            sys.exit()
        path = os.path.abspath(path)
        repository_name = "log"
        path += '/' + repository_name
        repo= None
        print('Will look for:', path)
        if not os.path.isdir(path):
            try:
                repo = git.Git().clone("https:/{}:{}@github.com/{}/{}.git".format(user, password, user, repository_name))
            except Exception as e:
                print(e)
        else:
            print('Folder with same name already exist !')
        repo = git.Repo(path)
        assert not repo.bare
        self.repo = repo
        return repo

    def commit(self, msg=None, branch='master'):
        commit_msg = msg
        if commit_msg == None:
            commit_msg = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S - %d/%m/%Y (%Z)")
        self.repo.index.commit(commit_msg)
        self.repo.remotes.origin.push(branch)

    def add(self, file='log.csv'):
        self.repo.git.add(file)

if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    print(path)
    s = Saver('log')
    s.get_repository(path=path)
    s.add()
    s.commit()
