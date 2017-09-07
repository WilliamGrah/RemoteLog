import datetime
import git
import os
import sys


class Saver():
    def __init__(self):
        self.repo = None
        self.repo_name = None
        pass

    def get_repository(self, path, repository_name, user=None):
        self.repo_name = repository_name
        path = os.path.abspath(path)
        path = os.path.join(path, self.repo_name)

        print('Will look for:', path)
        if not os.path.isdir(path):
            try:
                self.repo = git.Git().clone(
                    "ssh://git@github.com/{}/{}.git".format(user, repository_name))
            except Exception as e:
                print(e)
        else:
            print('Folder with same name already exist !')
        self.repo = git.Repo(path)
        assert not self.repo.bare

    def commit(self, msg=None, branch='master'):
        commit_msg = msg
        if commit_msg == None:
            commit_msg = datetime.datetime.now(
                datetime.timezone.utc).strftime("%H:%M:%S - %d/%m/%Y (%Z)")
        self.repo.index.commit(commit_msg)
        print('Pushing to remote.')
        self.repo.remotes.origin.push(branch)

    def add(self, arg='--all'):
        try:
            self.repo.git.add(arg)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    print(path)
    s = Saver()
    s.get_repository(path, 'log', 'patrickelectric')
    s.add()
    s.commit()
