from langchain import OpenAI
from langchain.memory import ConversationBufferMemory
import os
import asyncio
import datetime

import talksmith.utils.configuration as configuration
from talksmith.core.bot import TalksmithBot
from talksmith.hmi.chat import CLI
from talksmith.core.io import export_chat_history

class Core:

    def __init__(self):
        """Get the configuration and init the bot, its memory and its chains"""
        self.conf = configuration.load()
        print(conf)
        self.hmi = CLI()
        self.bot = TalksmithBot(OpenAI(temperature=0),
                                          ConversationBufferMemory(
                                              return_messages=True,
                                              human_prefix="human",
                                              ai_prefix="ai",
                                              memory_key="memory"))

    def check_for_exit(self, user_input: str) -> bool:
        if user_input.lower() == 'exit':
                export_input = input("Nice talking to you. Do you want to export our conversation? (Y/N): ")
                if export_input.lower() == 'y':
                    # Access the memory
                    memory = self.chatgpt_chain.memory.load_memory_variables({})
                    # Save chat history in memory
                    export_chat_history(memory, os.path.join(
                        self.conf.chat_history_path,
                        self.conf.chatbot_name,
                        datetime.datetime.now()))
                return True
        return False

    def run(self):
        """Get user input and process it"""
        end_chat = False
        while not end_chat:
            user_input = self.hmi.get_user_input()
            end_chat = self.check_for_exit(user_input)
            error_message = self.bot.process_input(chatgpt_chain, user_input)
            if error_message is not None:
                end_chat = True
