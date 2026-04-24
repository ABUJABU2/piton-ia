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
df.columns = ["pergunta", "resposta"]

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

# ============================================================
# ETAPA 3 —embeddingsV 
# ============================================================

embedddings = OpenAIEmbeddings(model='text-embedding-3-small')

# ============================================================
# ETAPA 4 —vector store 
# ============================================================

vector_store = FAISS.from_documents(chunks,embedddings) # originei a vector store usando os chunks gerados e o modelo de embedding 
#especificados
vector_store.save_local('minha_vectorstore')
print('vector store foi salva em disco local')

# ============================================================
# ETAPA 5 —prompt + llm
# ============================================================

llm=ChatOpenAI(model="gpt-4o-mini",temperature = 0)
prompt = ChatPromptTemplate.from_template(
    """você é um assistente prestativo que deverá responder perguntas exclusivamente com base no contexto abaixo
    .caso vocênão saiba a resposta, simplesmente fale que mâo sabe a resposta

    contexto:{context}
    
    pergunta:{input}

    """

)

# ============================================================
# ETAPA 6 — Cadeia RAG via LCEL
# ============================================================

retriever = vector_store.as_retriever(search_kwargs={"k": 3}) # pegando 3 chunks da minha vectore store

def formatar_docs(docs): #formatando a schunks
    return "\n\n".join(doc.page_content for doc in docs)

#uma linguagem de encadeiamento onde os estágios se conectam
qa_chain = (
    {"context": retriever  | formatar_docs , 'input':RunnablePassthrough()} # alimento o meu contexto formatando as chunks selecionadas no retriever
    |prompt #usamos o chat promt template e alimentamos o {contex} do prompt
    | llm #enviamos o prompt para a llm destacada
    |StrOutputParser () # formatamos a resposta da llm
)


pergunta = 'por que o vitor faltou no galileu hoje?'
print(f'\nPergunta: {pergunta}')

resposta = qa_chain.invoke(pergunta)
print(f'\nResposta: {resposta}')
