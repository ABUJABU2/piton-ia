ideias = {
"tecnologia": [
"App que organiza tarefas escolares",
"IA para resumir aulas",
"Site para aprender programação"
],

"games": [
"Campeonato online",
"Loja de skins",
"Canal de gameplay"
],

"pets": [
"Coleira inteligente",
"Hotel para pets",
"Rede social de animais"
],

"comidas": [
"Delivery saudável",
"Doceria online",
"App de receitas"
],

"esportes": [
"Escolinha online",
"App de treinos",
"Ranking de atletas"
]
}


import streamlit as st
import random
st.logo("socrates.jpg")
a = st.title("gerador de ideia")
q=st.text_input("qual seu nome")
w=st.selectbox("qual seu tipo de negócio" ,[ "tecnologia" , "games" , "pets","comidas", "esportes"] )
e=st.button("ideia aleatória")

if e :
    random=random.choice(ideias[w])
    st.title(random)  
    st.balloons()

    