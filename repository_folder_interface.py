import os
import shutil
import subprocess
import json
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

        wd = os.getcwd()
        os.chdir(path)
        output = subprocess.check_output(['github-linguist', '--json'])
        output = json.loads(output)
        os.chdir(wd)

        for key, file_list in output.items():
            for f in file_list:
                files.append(f)

        return files

    def remove_repo(self, repo_name):
        shutil.rmtree(self.get_repository_folder(repo_name))

    def repo_exists(self, repo_name):
        if os.path.isdir(self.get_repository_folder(repo_name)):
            return True
        else:
            return False

    def drill(self, github_repo_url):
        pass