import os #biblioteca que conversa com o meu sistema operacional
import pandas as pd #principal biblioteca para manejo de dados,estudos e limpeza de dados
from dotenv import load_dotenv #serve para abrir o seu arquivo .env que armazena a api da LLM (openai)
from langchain_community.document_loaders import UnstructuredExcelLoader #classe que carrega um arquivo de exel não estruturado
from langchain_text_splitters import RecursiveCharacterTextSplitter #classe que divide textos em pedaços menores (chunks(tipo as do minecraft))
from langchain_openai import OpenAIEmbeddings, ChatOpenAI #transforma a pergunta (str(string)) em num(numérico)
from langchain_community.vectorstores import FAISS #vectorstore disponível na langchain
from langchain_core.prompts import ChatPromptTemplate #esqueleto do prompt 💀💀💀💀💀💀💀
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# ============================================================
# ETAPA 1 — Carregar e formatar o Excel
# ============================================================
df = pd.read_excel("pergunta_resposta.xlsx", header=None) #criamos uma tabela que lê o meu exel
df.columns = ["pegunta", "resposta"]

docs_formatados = [
    Document(
        page_content=f"Pergunta: {row['pergunta']}\nResposta: {row['resposta']}",
        metadata={"linha": i + 1, "fonte": "pergunta_resposta.xlsx"}
    )
    for i, row in df.iterrows()
]
print(f"Documentos formatados: {len(docs_formatados)}")

# ============================================================
# ETAPA 2 —text splitter 
# ============================================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks=splitter.split_documents(docs_formatados)
print(f'chunks gerados:{len(chunks)}')
