from tf_bot import TFBot
import yaml 

# Entry point
if __name__ == '__main__':
    with open("info.yaml", 'r') as stream:
        try:
            info = yaml.safe_load(stream)
            tf_bot = TFBot(info['token'])
            tf_bot.get_repository_info(info['repository'])
        except yaml.YAMLError as ex:
            print(ex)