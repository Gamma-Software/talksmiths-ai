""" This module contains the Memory class, which is used to retrieve the memory of the bot.
It's a kind of hack from Langchain, as we won't store the memory in a Memory class from Langchain but in a file."""

from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import BaseMemory
from langchain.chains.llm import LLMChain
from pydantic import BaseModel
from typing import List, Dict, Any
from langchain.memory.prompt import (
    ENTITY_SUMMARIZATION_PROMPT,
)

from talksmith.utils.configuration import Config

def load_long_term_memory(conf: Config):
    loader = TextLoader('conf/bots/memory/anne_frank.txt')
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(openai_api_key=conf.open_ai_api_key)

    # TODO create a persistant DB: persist_directory = 'db'
    memory_db = Chroma.from_documents(docs, embeddings)
    retriever = memory_db.as_retriever()
    return retriever

class SpacyEntityMemory(BaseMemory, BaseModel):
    """Memory class for storing information about mindsets."""

    # Define dictionary to store information about mindsets.
    mindsets: dict = {}
    # Define key to pass information about mindsets into prompt.
    memory_key: str = "mindsets"

    def clear(self):
        self.mindsets = {}

    @property
    def memory_variables(self) -> List[str]:
        """Define the variables we are providing to the prompt."""
        return [self.memory_key]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """Load the memory variables, in this case the entity key."""

        chain = LLMChain(llm=self.llm, prompt=ENTITY_SUMMARIZATION_PROMPT)
        if self.input_key is None:
            prompt_input_key = get_prompt_input_key(inputs, self.memory_variables)
        else:
            prompt_input_key = self.input_key
        buffer_string = get_buffer_string(
            self.buffer[-self.k * 2 :],
            human_prefix=self.human_prefix,
            ai_prefix=self.ai_prefix,
        )
        output = chain.predict(
            history=buffer_string,
            input=inputs[prompt_input_key],
        )
        if output.strip() == "NONE":
            entities = []
        else:
            entities = [w.strip() for w in output.split(",")]
        entity_summaries = {}
        for entity in entities:
            entity_summaries[entity] = self.entity_store.get(entity, "")
        self.entity_cache = entities
        if self.return_messages:
            buffer: Any = self.buffer[-self.k * 2 :]
        else:
            buffer = buffer_string
        return {
            self.chat_history_key: buffer,
            "entities": entity_summaries,
        }

        # Get the input text and run through spacy
        doc = nlp(inputs[list(inputs.keys())[0]])
        # Extract known information about mindsets, if they exist.
        mindsets = [self.mindsets[str(ent)] for ent in doc.ents if str(ent) in self.mindsets]
        # Return combined information about mindsets to put into context.
        return {self.memory_key: "\n".join(mindsets)}

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save context from this conversation to buffer."""
        # Get the input text and run through spacy
        text = inputs[list(inputs.keys())[0]]
        doc = nlp(text)
        # For each entity that was mentioned, save this information to the dictionary.
        for ent in doc.ents:
            ent_str = str(ent)
            if ent_str in self.mindsets:
                self.mindsets[ent_str] += f"\n{text}"
            else:
                self.mindsets[ent_str] = text
