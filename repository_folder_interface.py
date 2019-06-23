import os
from pydriller import GitRepository, RepositoryMining

class RepositoryFolderInterface:
    """
    RepositoryFolderInterface is responsible for the local clone of the
    repository.
    """
    REPOSITORIES_FOLDER = './repositories'
    
    def __init__(self, folder=None):
        if folder is not None:
            self.REPOSITORIES_FOLDER = folder
    
    def get_repository_folder(self, repo_name):
        """
        Returns folder path for the target repository.

        Args:
            repo_name (str): the full-name of the repository.
        Returns:
            str: path on disk.
        """
        return '{}/{}'.format(self.REPOSITORIES_FOLDER, repo_name)

    def get_files_on_repo(self, repo_name):
        files = []
        path = self.get_repository_folder(repo_name)

        for r, _, f in os.walk(path):
            for file in f:
                files.append(os.path.join(r, file))

        return files

    def repo_exists(self, repo_folder):
        if os.path.isdir(repo_folder):
            return True
        else:
            return False

    def drill(self, github_repo_url):
        pass