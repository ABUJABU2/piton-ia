import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


#configurando a aba da pagina
st.set_page_config(

page_title='assistente de mine',
page_icon='image.png',
layout='centered'

)

#chamar api dentro do script
load_dotenv()

#cofg dos elementos da primeira cessão

st.title('assistente de minecraft com IA (RAG)')
st.markdown('faça upload de uma planília com perguntas e respostas e depois converse com o assistente sobre a planilha')
st.divider()
st.title('🗂️envie sua planilha')

#criando funções auxiliares
def carregar_exel(arquivo_exel) -> list[Document]: #criando uma função para transformar as linhas do exel em document(langchain)
    df = pd.read_excel(arquivo_exel,header=None)
    df.columns = ['pergunta ',' resposta']
    docs = [
        Document(
            page_content=f'pergunta: {row['pergunta']}\nresposta: {row['resposta']}',
            metadata={"linha":i+1,'fonte':arquivo.name},
    )
        for i,row in df.iterrows()
    ]
    return docs

def criar_vector_store(docs: list[Document] -> FAISS):
    #divide os docs em chunks e depois armazena em uma vector store (FAISS)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks=splitter.split_documents(docs)