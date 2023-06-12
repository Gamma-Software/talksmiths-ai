import sys
from langchain.llms import BaseLLM
from langchain.schema import Memory
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
from langchain.memory import ConversationKGMemory


class TalksmithBot:

    # Initialize the prompt and llm chain
    def __init__(self, llm: BaseLLM, long_term_memory: Memory):

        memory = ConversationKGMemory(llm=llm)
        memory.save_context({"input": "say hi to sam"}, {"output": "who is sam"})
        memory.save_context({"input": "sam is a friend"}, {"output": "okay"})

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
        return chatgpt_chain


    # Call LLM API to generate a response
    async def generate_response(chain, user_input):
        response = await chain.arun(human_input=user_input)
        return response

    # Process user input and display response or error message
    async def process_input(chatgpt_chain, user_input):
        sys.stdout.write(".....waiting for magic.....")
        sys.stdout.flush()
        try:
            response = await generate_response(chatgpt_chain, user_input)
            sys.stdout.write("\r" + " " * len(".....waiting for magic.....") + "\r")
            sys.stdout.flush()
            print(response, "\n")
            return None
        except Exception as e:
            sys.stdout.write("\r" + " " * len(".....waiting for magic.....") + "\r")
            sys.stdout.flush()
            error_message = "AI Assistant encountered an error. Please try again later."
            print(error_message)
            return error_message
