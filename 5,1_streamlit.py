import streamlit as st

st.title('VCNFG-1.0')
st.subheader("minecraft AI assistant made using langchain")

st.write("made by obasdes")

nome = st.text_input("whats your name")
age = st.number_input("how old are you?",0,150)

elo = st.slider("what's your elo?",0,2000)

animal = st.selectbox("que animal você tem", ['cachorro','gato','sapo'])

audio = st.audio_input("oi")