import configparser

def load_config():
    config = configparser.ConfigParser()
    config.read('config/framework.ini')
    return config
