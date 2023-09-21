import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import random
import pandas as pd
import time
import requests
import base64
st.title('Acerte o país')

placar = pd.read_csv('placar.txt', sep='\t')
pla = placar
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
    st.session_state.elemento_band = pais['ISO_2DIGIT'].values[0]
    fig, ax = plt.subplots()
    pais.plot(ax=ax)
    ax.set_title('Mapa do País Selecionado')
    st.session_state.fig = fig
    st.session_state.timer = None
    st.session_state.pontos = 0  # Inicializa os pontos com 0

st.pyplot(st.session_state.fig)

col1, col2, col3, col4 = st.columns(4)

if col1.button('DICA MOEDA'):
    st.write(f"A moeda desse país é: {st.session_state.elemento_moeda}")
if col2.button('DICA Capital'):
    st.write(f"A Capital desse país é: {st.session_state.elemento_capital}")
if col3.button('DICA Continente'):
    st.write(f"O continente desse país é: {st.session_state.elemento_cont}")
if col4.button('DICA Bandeira'):
    url_imagem = 'https://flagcdn.com/160x120/' + st.session_state.elemento_band.lower() + '.png'
    st.image(url_imagem, caption='Minha Imagem Online', use_column_width=True)

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
            pr = pr[pr['dificuldade'] < 4]
            lista = pr['pais']
            st.session_state.elemento_aleatorio = random.choice(lista)
            pais = pr[pr['pais'] == st.session_state.elemento_aleatorio]
            st.session_state.elemento_moeda = pais['CURR_TYPE'].values[0]
            st.session_state.elemento_capital = pais['capital'].values[0]
            st.session_state.elemento_cont = pais['continente'].values[0]
            st.session_state.elemento_band = pais['ISO_2DIGIT'].values[0]
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
                    pr = pr[pr['dificuldade'] < 4]
                    lista = pr['pais']
                    st.session_state.elemento_aleatorio = random.choice(lista)
                    pais = pr[pr['pais'] == st.session_state.elemento_aleatorio]
                    st.session_state.elemento_moeda = pais['CURR_TYPE'].values[0]
                    st.session_state.elemento_capital = pais['capital'].values[0]
                    st.session_state.elemento_cont = pais['continente'].values[0]
                    st.session_state.elemento_band = pais['ISO_2DIGIT'].values[0]
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
    pr = pr[pr['dificuldade'] < 4]
    lista = pr['pais']
    st.session_state.elemento_aleatorio = random.choice(lista)
    pais = pr[pr['pais'] == st.session_state.elemento_aleatorio]
    st.session_state.elemento_moeda = pais['CURR_TYPE'].values[0]
    st.session_state.elemento_capital = pais['capital'].values[0]
    st.session_state.elemento_cont = pais['continente'].values[0]
    st.session_state.elemento_band = pais['ISO_2DIGIT'].values[0]
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
        data = {'nome': [nome_jogador], 'pontuação': [st.session_state.pontos]}
        df = pd.DataFrame(data, index=[0])
        placar = pd.read_csv('placar.txt', sep='       ')
        pl = pd.concat([placar, df], ignore_index=True)
        #df = pd.DataFrame(placar)
        st.write(pl)
        #df.to_csv('placar.txt', index=False)
        p = pl.to_string(index=False)
        username = "WevertonVerica"
        repository = "Streamlit"
        path = "placar.txt"  # O caminho para onde deseja salvar o arquivo no repositório
        token = "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"  # Substitua pelo seu token de acesso do GitHub
        conteudo_txt = p
        conteudo_base64 = base64.b64encode(conteudo_txt.encode()).decode()
        # Faça uma solicitação PUT para enviar o arquivo TXT para o repositório no GitHub
        url = f"https://api.github.com/repos/{username}/{repository}/contents/{path}"
        headers = {
            "Authorization": f"token {token}",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            conteudo_existente = response.json()
            sha_existente = conteudo_existente["sha"]
        else:
            # Se o arquivo não existir, o SHA-1 será None
            sha_existente = None
        data = {
            "message": "Adicionando ou atualizando arquivo TXT via Streamlit",
            "content": conteudo_base64,
            "sha": sha_existente,  # Forneça o SHA-1 do arquivo existente
        }
        response = requests.put(url, headers=headers, json=data)
else:
    df = pd.DataFrame(pla)
    st.write(df)
