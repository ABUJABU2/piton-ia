ideias = {
"Tecnologia": [
"App que organiza tarefas escolares",
"IA para resumir aulas",
"Site para aprender programação"
],

"Games": [
"Campeonato online",
"Loja de skins",
"Canal de gameplay"
],

"Pets": [
"Coleira inteligente",
"Hotel para pets",
"Rede social de animais"
],

"Comida": [
"Delivery saudável",
"Doceria online",
"App de receitas"
],

"Esportes": [
"Escolinha online",
"App de treinos",
"Ranking de atletas"
]
}


import streamlit as st
import random

a = st.title("gerador de ideia")
q=st.text_input("qual seu nome")
w=st.selectbox("qual seu tipo de negócio" ,[ "tecnologia" , "games" , "pets","comidas", "esports"] )
e=st.button("ideia aleatória")

if e :
    st.title( random.choice(ideias))
