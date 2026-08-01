import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import random
import time

st.title("Acerte o País")

# =====================================================

# FUNÇÕES

# =====================================================

def gerar_novo_pais():

```
pais_df = pd.read_csv("pais.txt", sep="\t")

pr = gpd.read_file("mundo.shp")
pr.rename(columns={"GMI_CNTRY": "sigla"}, inplace=True)

pr = pd.merge(pr, pais_df, on="sigla", how="inner")
pr = pr[pr["dificuldade"] < 4]

pais_escolhido = random.choice(list(pr["pais"]))

st.session_state.elemento_aleatorio = pais_escolhido

pais = pr[pr["pais"] == pais_escolhido]

st.session_state.elemento_moeda = pais["CURR_TYPE"].values[0]
st.session_state.elemento_capital = pais["capital"].values[0]
st.session_state.elemento_cont = pais["continente"].values[0]
st.session_state.elemento_band = pais["ISO_2DIGIT"].values[0]

fig, ax = plt.subplots()
pais.plot(ax=ax)
ax.set_title("Mapa do País Selecionado")

st.session_state.fig = fig
```

def verificar_resposta():

```
chute = st.session_state.chute.strip().lower()

if chute == st.session_state.elemento_aleatorio.lower():

    st.session_state.pontos += 10
    st.session_state.mensagem = "✅ Você acertou!"

    gerar_novo_pais()

    # limpa a caixa de texto
    st.session_state.chute = ""

else:
    st.session_state.mensagem = "❌ Tente novamente."
```

# =====================================================

# INICIALIZAÇÃO

# =====================================================

if "pontos" not in st.session_state:
st.session_state.pontos = 0

if "mensagem" not in st.session_state:
st.session_state.mensagem = ""

if "timer" not in st.session_state:
st.session_state.timer = time.time() + 120

if "elemento_aleatorio" not in st.session_state:
gerar_novo_pais()

# =====================================================

# MAPA

# =====================================================

st.pyplot(st.session_state.fig)

# =====================================================

# DICAS

# =====================================================

col1, col2, col3, col4 = st.columns(4)

if col1.button("DICA MOEDA"):
st.info(f"Moeda: {st.session_state.elemento_moeda}")

if col2.button("DICA CAPITAL"):
st.info(f"Capital: {st.session_state.elemento_capital}")

if col3.button("DICA CONTINENTE"):
st.info(f"Continente: {st.session_state.elemento_cont}")

if col4.button("DICA BANDEIRA"):
url = (
"https://flagcdn.com/160x120/"
+ st.session_state.elemento_band.lower()
+ ".png"
)
st.image(url)

# =====================================================

# CAMPO DE RESPOSTA

# =====================================================

st.text_input(
"Digite um país:",
key="chute",
on_change=verificar_resposta
)

# =====================================================

# RESULTADO

# =====================================================

if st.session_state.mensagem:
st.write(st.session_state.mensagem)

# =====================================================

# DESISTIR

# =====================================================

if st.button("Desistir"):

```
st.warning(
    f"O país era: {st.session_state.elemento_aleatorio}"
)

gerar_novo_pais()
```

# =====================================================

# PONTUAÇÃO

# =====================================================

st.write(
f"🏆 Você possui {st.session_state.pontos} pontos."
)

# =====================================================

# PLACAR

# =====================================================

placar = pd.read_csv("placar.txt", sep=",")

if (
st.session_state.pontos > 50
and time.time() > st.session_state.timer
):

```
nome = st.text_input(
    "Parabéns! Digite seu nome:"
)

if st.button("Salvar no placar"):

    novo = pd.DataFrame(
        {
            "nome": [nome],
            "pontuação": [st.session_state.pontos]
        }
    )

    placar = pd.concat(
        [placar, novo],
        ignore_index=True
    )

    placar.to_csv(
        "placar.txt",
        index=False
    )

    st.success("Pontuação salva!")
```

else:

```
st.dataframe(placar)
```
