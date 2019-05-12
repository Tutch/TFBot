from github import Github, BadCredentialsException
from repository_folder_interface import RepositoryFolderInterface
from tf_bot_exception import NoUserTokenException
from util import levenshtein_distance

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
            self.g = Github(token)
            self.token = token
            self.repository = None
            self.authenticated_user = self.g.get_user()
        except Exception as ex:
            if isinstance(ex, BadCredentialsException):
                raise NoUserTokenException('GitHub user token is invalid.')
            
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

    def get_repository_info(self, repository_name):
        pass