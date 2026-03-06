

import openai

#importar da biblioteca dotenv, os métodos load e find dotenv
from dotenv import load_dotenv, find_dotenv

#finddotenv procura arquivo que armazena a minha api,logo en seguida, o loaddotenv carrega esse arquivo e armazena na váriável anônima(_)
_= load_dotenv(find_dotenv())

#inicialização da openai no meu ambiente de código
client = openai.Client()

#criar a interação que é a interação do usuário com o LLM
mensagens = [{'role':'user','content':'o que você sabe do Elon Musk?'}]

#Configurar resposta da LLM
resposta =client.chat.completions.create(
     messages=mensagens,
     model='gpt-5.4',
     #max_tokens=,
     temperature=0,
    stream=True #retorna a resposta enquanto ela for construída 

)

#criando estrutura de laço para retornar os pedaços da resposta da LLM
resposta_completa=''
for stream_resposta in resposta:
    texto= stream_resposta.choices[0].delta.content
    if texto:
        resposta_completa+=texto
        print(texto,end='')


