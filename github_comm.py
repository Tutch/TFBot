from github import Github, BadCredentialsException
from repository_folder_interface import RepositoryFolderInterface
from tf_bot_exception import NoUserTokenException
from util import levenshtein_distance
from git import Repo

class GithubComm:
    """
    GithubComm gets data from Github using the PyGithub library.
    
    Args:
        token: GitHub user token.
    """
    # Constants
    EMAIL_FIELD = 'email'
    DEV_ALIASES = 'dev_aliases'

    def __init__(self, token=None):
        try:
            self.folder_interface = RepositoryFolderInterface()
            self.g = Github(token)
            self.token = token
            self.repository = None
            self.authenticated_user = self.g.get_user()
        except Exception as ex:
            if isinstance(ex, BadCredentialsException):
                raise NoUserTokenException('GitHub user token is invalid.')
            
    def get_target_source_files(self):
        """
        Creates a list of the source files on the the repository.

        This list is aggregated based following the algorithm on Valente's 2016
        paper "A Novel Approach for Estimating Truck Factor", namely step #1
        "List Target Source Files".

        Returns:
            list: A list of dictionaries containing the fields 'email' and 'dev_aliases'.
        """
        source_files = []

        if self.repository is not None:
            pass

    def get_contributors_list(self):
        """
        Creates a list of dicts containing the collaborators for the repository.

        This list is aggregated based following the algorithm on Valente's 2016
        paper "A Novel Approach for Estimating Truck Factor", namely step #2 "Detect
        Developer Aliases.

        The collaborators are indexed by email and the names is a list of developer
        aliases that the user might have. The user is considered the same user
        if the leveshtein distance for the two users names is equal or less than
        one.

        Returns:
            list: A list of dictionaries containing the fields 'email' and 'dev_aliases'.
        """
        contributors_list = []

        if self.repository is not None:
            for collaborator in self.repository.get_collaborators():
                email = collaborator.email
                name = collaborator.name
        
                list_entry = {
                    self.EMAIL_FIELD: email,
                    self.DEV_ALIASES: [name]
                }

                fresh_user = True

                for contributor in contributors_list:                    
                    for alias in contributor.dev_aliases:
                        if levenshtein_distance(alias, name) <= 1:
                            contributor.dev_aliases.append(name)
                            fresh_user = False
                            break
                    if not fresh_user:
                        break
                    
                if fresh_user:
                    contributors_list.append(list_entry)
                    
        return contributors_list

    def get_repository_url(self, repository_name):
        """
        Gets the clone url for the GitHub repository.

        Args:
            repository_name (str): the name of the repository.
        Returns:
            str: GitHub url for the git repository.
        """
        self.repository = self.authenticated_user.get_repo(repository_name)

        return self.repository.clone_url, self.repository.full_name
    
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
        repo_folder = self.folder_interface.get_repository_folder(repo_name)
        
        try:
            if self.folder_interface.repo_exists(repo_folder):
                return repo_folder 
            
            Repo.clone_from(github_repo_url, repo_folder)
            return repo_folder
        except Exception as ex:
            print(ex)
            return ''