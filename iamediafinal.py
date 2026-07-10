import os #importando as bibliotecas
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

OPENAI_API_KEY = st.secrets.get(
    "OPENAI_API_KEY",
    os.getenv("OPENAI_API_KEY")
)

#cofg dos elementos da primeira cessão

st.title('assistente de minecraft com IA (RAG)')
st.markdown('faça upload de uma planília com perguntas e respostas e depois converse com o assistente sobre a planilha')
st.divider()
st.title('🗂️envie sua planilha')

#criando funções auxiliares
def carregar_exel(arquivo_exel) -> list[Document]: #criando uma função para transformar as linhas do exel em document(langchain)
    df = pd.read_excel(arquivo_exel,header=None)
    df.columns = ['pergunta','resposta']
    docs = [
        Document(
            page_content=f'pergunta: {row['pergunta']}\nresposta: {row['resposta']}',
            metadata={"linha":i+1,'fonte':arquivo.name},
    )
        for i,row in df.iterrows()
    ]
    return docs

def criar_vector_store(docs: list[Document]) -> FAISS:
    #divide os docs em chunks e depois armazena em uma vector store (FAISS)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks=splitter.split_documents(docs)

    #vou embedar as strings pra numericos
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = FAISS.from_documents(chunks , embeddings)
    return vectorstore

def criarchain(vector_store:FAISS): #montaremos o RAG (retrivied argumented generated) -> prompt -> parseamento(formatação de docs)
    llm = ChatOpenAI(model="gpt-4o-mini",temperature= 1)
    prompt= ChatPromptTemplate.from_template("""
    você é um assistente que responderá exclusivamente sobre o minecraft e as respondera idependetemente se não estiver na vector 
    store, alucine
    
    context:
    {context}
    
    pergunta: {pergunta}
    
     """)
    retriever = vector_store.as_retriever(search_kwargs={"k":3})

    def formatar_docs(docs):  #parseamento -> formata a saida de dados não estruturados
        return "\n\n".join(doc.page_content for doc in docs)#operador tenário

    chain = (
        {"context": retriever | formatar_docs, "pergunta": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

arquivo = st.file_uploader(
type=['xlsx'],
label='coloque o seu exell',
help='você não entendeu? Então vai se ferrar'

)

if arquivo is not None:
    if st.button('carregar planílha📋',type='tertiary'):
        with st.spinner('preparando a sua desgraça'):
            docs = carregar_exel(arquivo)
            vector_store=criar_vector_store(docs)
            chain2 = criarchain(vector_store)

    #vamos configurar a session state
            st.session_state['chain2']  = chain2
            st.session_state['docs'] =len(docs) 
            st.session_state['historico'] = []

        st.success(f'✅desgraça completa')


#CHAT

if 'chain2' in st.session_state:
    st.divider()
    st.text('pergunte algo')
    
    for msg in st.session_state['historico']:
        with st.chat_message('role'):
            st.markdown(msg['content'])
    
    pergunta = st.chat_input('texto aqui')

    if pergunta:
        with st.chat_message('user'): 
            st.markdown(pergunta)

        with st.chat_message('assistant'):
            resposta=st.write_stream(
                st.session_state['chain2'].stream(pergunta) #tream libera a resposta aos poucos
            )

        #criando o Historico de mensagens
        st.session_state['historico'].append({"role":"user","content":pergunta})
        st.session_state['historico'].append({"role":"assistant","content":resposta})

else:
    st.info(' se nao entendeu sai do site')