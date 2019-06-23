from github import Github, BadCredentialsException
from repository_folder_interface import RepositoryFolderInterface
from tf_bot_exception import NoUserTokenException
from util import levenshtein_distance
from git import Repo, Git

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
            self.repo_folder = ''
            self.api_repository = None
            self.git_repository = None
            self.authenticated_user = self.g.get_user()
        except Exception as ex:
            if isinstance(ex, BadCredentialsException):
                raise NoUserTokenException('GitHub user token is invalid.')
            
    def init_repository(self, repo_name):
        self.api_repository = self.authenticated_user.get_repo(repo_name)
        self.repo_folder = self.folder_interface.get_repository_folder(self.api_repository.full_name)

        if self.folder_interface.repo_exists(self.api_repository.full_name):
            self.folder_interface.remove_repo(self.api_repository.full_name)
            self.git_repository = Repo.clone_from(self.api_repository.clone_url, self.repo_folder)

    def get_target_source_files(self):
        """
        Creates a list of the source files on the the repository.

        This list is aggregated based following the algorithm on Valente's 2016
        paper "A Novel Approach for Estimating Truck Factor", namely step #1
        "List Target Source Files".

        Returns:
            list: A list of dictionaries containing the fields 'email' and 'dev_aliases'.
        """
        source_files = {}
        
        if self.git_repository is not None:
            commit_list = list(self.git_repository.iter_commits())

            # Commit history (from first to last)
            for commit in commit_list:
                tag = commit.hexsha
                
                # Checkout
                Git(self.repo_folder).checkout(tag)

                source_files[tag] = self.folder_interface.get_files_on_repo(self.api_repository.full_name)

        return source_files

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

        if self.api_repository is not None:
            for collaborator in self.api_repository.get_collaborators():
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