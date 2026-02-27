import openai

#importar da biblioteca dotenv, os métodos load e find dotenv
from dotenv import load_dotenv, find_dotenv

#finddotenv procura arquivo que armazena a minha api,logo en seguida, o loaddotenv carrega esse arquivo e armazena na váriável anônima(_)
_= load_dotenv(find_dotenv())

#inicialização da openai no meu ambiente de código
client = openai.client



