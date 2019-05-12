import os
from pydriller import GitRepository, RepositoryMining
from git import Repo

class RepositoryFolderInterface:
    """
    RepositoryFolderInterface is responsible for the local clone of the
    repository.
    """
    REPOSITORIES_FOLDER = './repositories'
    
    def __init__(self, folder=None):
        if folder is not None:
            self.REPOSITORIES_FOLDER = folder
        
    def clone_repository(self, github_repo_url, repo_name):
        """ 
        Clones the repository locally to the constant REPOSITORES_FOLDER location.

        The folder is saved on a full-name structure. Example: User/MyRepo will
        be saved to REPOSITORIES_FOLDER/User/MyRepo.

        Args:
            github_repo_url (str): url for the GitHub repository.
            repo_name (str): the full-name of the repository.
        Returns:
            str: the repository location on disk.
        """
        repo_folder = '{}/{}'.format(self.REPOSITORIES_FOLDER, repo_name)
        
        try:
            if os.path.isdir(repo_folder):
                return repo_folder
            
            Repo.clone_from(github_repo_url, repo_folder)
            return repo_folder
        except Exception as ex:
            print(ex)
            return ''

    def drill(self, github_repo_url):
        pass