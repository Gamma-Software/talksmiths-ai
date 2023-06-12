import os
import configparser

class Config:
    @property
    def open_ai_api_key(self):
        return self.__open_ai_api_key

    @property
    def log_path(self):
        return self.__logging_log_path

    @property
    def log_level(self):
        return self.__logging_log_level

    @property
    def chat_history_path(self):
        return self.__logging_chat_history_path

    @property
    def chatbot_memory_path(self):
        return self.__chatbot_memory_path

    @property
    def chatbot_personality_path(self):
        return self.__chatbot_personality_path

    @property
    def chatbot_prompt_path(self):
        return self.__chatbot_prompt_path

    @property
    def chatbot_name(self):
        return self.__chatbot_name

    @property
    def chatbot_temperature(self):
        return self.__chatbot_temperature

    @property
    def chatbot_max_token(self):
        return self.__chatbot_max_token


def load(config_file="config.ini") -> Config:
    parser = configparser.ConfigParser().read(config_file)
    config = Config()

    config.open_ai_api_key = parser.get('API_KEYS', 'OPENAI-API_KEY')

    config.log_path = parser.get('LOGGING', 'LOG_PATH')
    config.log_level = parser.get('LOGGING', 'LOG_LEVEL')
    config.chat_history_path = parser.get('LOGGING', 'CHAT_HISTORY_PATH')

    config.chatbot_memory_path = parser.get('CHATBOT', 'MEMORY_PATH')
    config.chatbot_personality_path = parser.get('CHATBOT', 'PERSONALITY_PATH')
    config.chatbot_prompt_path = parser.get('CHATBOT', 'PROMPT_PATH')
    config.chatbot_name = parser.get('CHATBOT', 'NAME')
    config.chatbot_temperature = parser.get('CHATBOT', 'TEMPERATURE')
    config.chatbot_max_token = parser.get('CHATBOT', 'MAX_TOKENS')
