import os
import configparser

class Config:
    @property
    def open_ai_api_key(self):
        return self.__open_ai_api_key

def load(config_file="config.ini") -> Config:
    parser = configparser.ConfigParser().read(config_file)
    config = Config()
    config.open_ai_api_key = parser.get('API_KEYS', 'OPENAI-API_KEY')
