""" This module contains the Memory class, which is used to retrieve the memory of the bot.
It's a kind of hack from Langchain, as we won't store the memory in a Memory class from Langchain but in a file."""

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import TextLoader
import langchain

loader = TextLoader("../../state_of_the_union.txt")
documents = loader.load()