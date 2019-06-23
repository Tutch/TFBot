from github_comm import GithubComm
from repository_folder_interface import RepositoryFolderInterface
from tf_bot_exception import NoUserTokenException

class TFBot:
    """
    TFBot gets data from the commit history of a GitHub repository and produces
    a report about the truck factor.

    Args:
        token (str): GitHub user token.
    """
    def __init__(self, token=None):
        try:
            self.github_comm = GithubComm(token)
            self.token = token
        except NoUserTokenException as ex:
            print(ex)

    def set_repository_token(self, token=None):
        """
        Sets the GitHub token for this instance of TFBot.
        
        Args:
            token (str): GitHub user token.
        """
        if token is not None:
            self.token = token
            self.github_comm = GithubComm(token)

    def get_repository_info(self, repository_name):
        """
        Gets user information from the repository_name for the current user. 
            
        Args:
            token (str): GitHub user token.
        """
        try:
            #0 Init
            self.github_comm.init_repository(repository_name)

            #1 Get source files list
            source_files = self.github_comm.get_target_source_files()
            print(source_files)

            #2 Compile the list of users in the repository
            contributors_list = self.github_comm.get_contributors_list()
            print(contributors_list)


        except Exception as ex:
            print(ex)