import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import random
import pandas as pd
import time
st.title('Acerte o país')

placar = pd.read_csv('placar.txt', sep=',')
placar.to_csv('placar.txt', index=False)
# Verifica se o estado já foi inicializado
if 'elemento_aleatorio' not in st.session_state:
    pais = pd.read_csv('pais.txt', sep='\t')
    pr = gpd.read_file('mundo.shp')
    pr.rename(columns={'GMI_CNTRY': 'sigla'}, inplace=True)
    pr = pd.merge(pr, pais, on='sigla', how='inner')
    pr = pr[pr['dificuldade'] < 4]
    lista = pr['pais']
    st.session_state.elemento_aleatorio = random.choice(lista)
    pais = pr[pr['pais'] == st.session_state.elemento_aleatorio]
    st.session_state.elemento_moeda = pais['CURR_TYPE'].values[0]
    st.session_state.elemento_capital = pais['capital'].values[0]
    st.session_state.elemento_cont = pais['continente'].values[0]
    fig, ax = plt.subplots()
    pais.plot(ax=ax)
    ax.set_title('Mapa do País Selecionado')
    st.session_state.fig = fig
    st.session_state.timer = None
    st.session_state.pontos = 0  # Inicializa os pontos com 0


st.pyplot(st.session_state.fig)

# Adicionar um botão para mostrar o país selecionado

if st.button('DICA MOEDA'):
    st.write(f"A moeda desse país é: {st.session_state.elemento_moeda}")
if st.button('DICA Capital'):
    st.write(f"A moeda desse país é: {st.session_state.elemento_capital}")
if st.button('DICA Continente'):
    st.write(f"A moeda desse país é: {st.session_state.elemento_cont}")

chute = st.text_input('Digite um país:')
resultado = ""
tempo_restante = ""


if st.button('Verificar'):
    if st.session_state.timer is None:
        st.session_state.timer = time.time() + 120  # Define um temporizador de 20 segundos
    if time.time() < st.session_state.timer:
        if chute.lower() == st.session_state.elemento_aleatorio.lower():
            resultado = "Você acertou!"
            st.session_state.pontos += 10  # Incrementa os pontos em 10
            pais = pd.read_csv('pais.txt', sep='\t')
            pr = gpd.read_file('mundo.shp')
            pr.rename(columns={'GMI_CNTRY': 'sigla'}, inplace=True)
            pr = pd.merge(pr, pais, on='sigla', how='inner')
            pr = pr[pr['dificuldade'] <= 3]
            lista = pr['pais']
            st.session_state.elemento_aleatorio = random.choice(lista)
            pais = pr[pr['pais'] == st.session_state.elemento_aleatorio]
            st.session_state.elemento_moeda = pais['CURR_TYPE'].values[0]
            st.session_state.elemento_capital = pais['capital'].values[0]
            st.session_state.elemento_cont = pais['continente'].values[0]
            fig, ax = plt.subplots()
            pais.plot(ax=ax)
            ax.set_title('Mapa do País Selecionado')
            st.session_state.fig = fig
            if st.button('Jogar novamente'):
                if chute.lower() == st.session_state.elemento_aleatorio.lower():
                    resultado = "Você acertou!"
                    st.session_state.pontos += 10  # Incrementa os pontos em 10
                    pais = pd.read_csv('pais.txt', sep='\t')
                    pr = gpd.read_file('mundo.shp')
                    pr.rename(columns={'GMI_CNTRY': 'sigla'}, inplace=True)
                    pr = pd.merge(pr, pais, on='sigla', how='inner')
                    pr = pr[pr['dificuldade'] <= 3]
                    lista = pr['pais']
                    st.session_state.elemento_aleatorio = random.choice(lista)
                    pais = pr[pr['pais'] == st.session_state.elemento_aleatorio]
                    st.session_state.elemento_moeda = pais['CURR_TYPE'].values[0]
                    st.session_state.elemento_capital = pais['capital'].values[0]
                    st.session_state.elemento_cont = pais['continente'].values[0]
                    fig, ax = plt.subplots()
                    pais.plot(ax=ax)
                    ax.set_title('Mapa do País Selecionado')
                    st.session_state.fig = fig
                else:
                    resultado = "Tente outra vez."
        else:
            resultado = "Tente outra vez."
    else:
        resultado = "Tempo esgotado!"

st.write(resultado)

# Se o botão "Pular" for clicado, gera um novo país aleatório
if st.button('Desistir'):
    st.write(f"O país selecionado era: {st.session_state.elemento_aleatorio.lower()}")
    pais = pd.read_csv('pais.txt', sep='\t')
    pr = gpd.read_file('mundo.shp')
    pr.rename(columns={'GMI_CNTRY': 'sigla'}, inplace=True)
    pr = pd.merge(pr, pais, on='sigla', how='inner')
    pr = pr[pr['dificuldade'] <= 3]
    lista = pr['pais']
    st.session_state.elemento_aleatorio = random.choice(lista)
    pais = pr[pr['pais'] == st.session_state.elemento_aleatorio]
    st.session_state.elemento_moeda = pais['CURR_TYPE'].values[0]
    st.session_state.elemento_capital = pais['capital'].values[0]
    st.session_state.elemento_cont = pais['continente'].values[0]
    fig, ax = plt.subplots()
    pais.plot(ax=ax)
    ax.set_title('Mapa do País Selecionado')
    st.session_state.fig = fig
    if st.button('Pular'):
        st.write('tente novamente')
st.write(f"Você possui {st.session_state.pontos} pontos.")
if st.session_state.pontos > 10 and time.time() > st.session_state.timer:
    nome_jogador = st.text_input("Parabéns! Você ganhou mais de 10 pontos. Insira seu nome:")
    if st.button('Incluir o nome do placar de lider'):
        nova_linha = {'nome': nome_jogador, 'pontuação': st.session_state.pontos}
        placar = pd.read_csv('placar.txt', sep=',')
        placar = pd.DataFrame(placar)
        df = placar.append(nova_linha, ignore_index=True)
        #df = pd.DataFrame(placar)
        df = df.dropna()
        st.write(df)
        #df = df.dropna()
        df.to_csv('placar.txt', index=False)
else:
    df = pd.DataFrame(placar)
    st.write(df)
