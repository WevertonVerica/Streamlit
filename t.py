import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import random
import pandas as pd

# Verifica se o estado já foi inicializado
if 'elemento_aleatorio' not in st.session_state:
    pais = pd.read_csv('pais.txt', sep = '\t')
    pr = gpd.read_file('mundo.shp')
    pr.rename(columns={'GMI_CNTRY': 'sigla'}, inplace=True)
    pr = pd.merge(pr, pais, on='sigla', how='inner')
    lista = pr['pais']
    st.session_state.elemento_aleatorio = random.choice(lista)
    pais = pr[pr['pais'] == st.session_state.elemento_aleatorio]

    fig, ax = plt.subplots()
    pais.plot(ax=ax)
    ax.set_title('Mapa do País Selecionado')
    st.session_state.fig = fig

st.title('Acerte o país')
st.pyplot(st.session_state.fig)
st.write(st.session_state.elemento_aleatorio.lower())
chute = st.text_input('Digite um país:')
resultado = ""

if st.button('Verificar'):
    if chute.lower() == st.session_state.elemento_aleatorio.lower():
        resultado = "Você acertou!"
    else:
        resultado = "Tente outra vez."

st.write(resultado)