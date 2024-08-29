import configparser
import os

class ConfigReader:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join('config', 'config.ini'))

    def get_base_url(self, environment='DEFAULT'):
        return self.config[environment]['base_url']

    def get_browser(self, environment='DEFAULT'):
        return self.config[environment]['browser']
