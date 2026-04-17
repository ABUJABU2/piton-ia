import os #biblioteca que conversa com o meu sistema operacional
import pandas as pd #principal biblioteca para manejo de dados,estudos e limpeza de dados
from dotenv import load_dotenv #serve para abrir o seu arquivo .env que armazena a api da LLM (openai)
from langchain_community.document_loaders import UnstructuredExcelLoader #classe que carrega um arquivo de exel não estruturado
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
#_______________________________________________________________________________________________________________________

#-----------------------------------------------------------------------------------------------------------------------
