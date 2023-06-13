from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.loading import load_prompt

from langchain.memory import ConversationBufferMemory, CombinedMemory

from talksmith.core.memory import load_long_term_memory
from talksmith.core.memory import ConversationMindsetMemory
from talksmith.utils.configuration import Config
from talksmith.core.prompts import load_character_info, adapt_prompt


class TalksmithBot:

    # Initialize the prompt and llm chain
    def __init__(self, conf: Config):
        llm = ChatOpenAI(temperature=0, openai_api_key=conf.open_ai_api_key)
        chat_history = ConversationBufferMemory(return_messages=True,
                                                human_prefix="human",
                                                ai_prefix="ai")
        mindset = ConversationMindsetMemory(return_messages=True)

        bot_info = load_character_info(conf.chatbot_info_path)
        template= adapt_prompt(bot_info)

        self.prompt = PromptTemplate(
            input_variables=["history", "input"],
            template=template
        )

        """template="You are a helpful assistant that translates {input_language} to {output_language}."
        context_message_prompt = SystemMessagePromptTemplate.from_template(template)
        current_conversation_message_prompt = SystemMessagePromptTemplate.from_template("\n\nCurrent conversation:\n{history}")
        mindset_message_prompt = SystemMessagePromptTemplate.from_template("\nCurrent mindset: {mindset}")
        human_message_prompt = HumanMessagePromptTemplate.from_template("\nhuman: {input}")

        self.prompt = ChatPromptTemplate.from_messages([
            context_message_prompt,
            current_conversation_message_prompt,
            mindset_message_prompt,
            human_message_prompt])"""

        self.conversation = ConversationChain(
            prompt=self.prompt,
            llm=llm,
            memory=CombinedMemory(memories=[chat_history, mindset]),
            verbose=conf.chat_debug
        )

        """self.chain = LLMChain(llm=chat, prompt=chat_prompt)


        retriever = load_long_term_memory(conf)
        qa_stuff = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            verbose=True
        )

        conversation = ConversationChain(
            llm=llm,
            verbose=True,
            memory=ConversationBufferMemory()
        )

        # Initialize the prompt
        prompt = PromptTemplate(
            input_variables=["history", "human_input"],
            template=prompt_template
        )

        # Initialize the LLM Chain and memory
        chatgpt_chain = LLMChain(
            llm=OpenAI(temperature=0, max_tokens=100),
            prompt=prompt,
            memory=ConversationBufferMemory(return_messages=True)
        )
        return chatgpt_chain"""

    def process_input(self, user_input):
        """Process user input and display response or error message

        Args:
            chatgpt_chain (_type_): _description_
            user_input (_type_): _description_

        Returns:
            Bool: True if the process ended correctly
            Str:  AI message (Could be an error message)
        """
        try:
            response = self.conversation.predict(input=user_input)
            print(self.conversation.memory.mindset_store.store)
            return True, response
        except Exception as e:
            print(e)
            error_message = "AI Assistant encountered an error. Please try again later."
            print(error_message)
            return False, error_message
