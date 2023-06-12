from langchain import OpenAI
from langchain.memory import ConversationBufferMemory

import talksmith.utils.configuration as configuration
from talksmith.core.bot import TalksmithBot

# Run async function synchronously
def run_async(coroutine_object):
    return asyncio.get_event_loop().run_until_complete(coroutine_object)

class Core:

    def __init__(self):
        """Get the configuration and init the bot, its memory and its chains"""
        conf = configuration.load()
        print(conf)
        exit(0)
        chatgpt_chain = TalksmithBot(OpenAI(temperature=0), ConversationBufferMemory(return_messages=True, human_prefix="human", ai_prefix="ai", memory_key="memory"))

    def run(self):
        """Get user input and process it"""
        end_chat = False
        while not end_chat:
            user_input = input(f"\nYour message: ")
            if user_input.lower() == 'exit':
                export_input = input(f"\nNice talking to you. Do you want to export our conversation? (Y/N): ")
                if export_input.lower() == 'y':
                    # Access the memory
                    memory = chatgpt_chain.memory.load_memory_variables({})
                    # Save chat history in memory
                    export_chat_history(memory, "human_assistant_messages.txt")
                end_chat = True
            else:
                error_message = run_async(process_input(chatgpt_chain, user_input))
                if error_message is not None:
                    end_chat = True
