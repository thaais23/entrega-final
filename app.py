import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import random
from collections import Counter

# Configuración inicial
st.set_page_config(page_title="Explora el Universo de los K-dramas", layout="wide")

# CSS general
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #fff0f5;
            color: #222222;
        }

        h1, h2, h3, h4 {
            color: #e91e63 !important;
        }

        section[data-testid="stSidebar"] {
            background-color: #dddddd !important;
        }

        section[data-testid="stSidebar"] * {
            color: #222 !important;
        }

        .stAlert-success {
            background-color: #ffe6ef !important;
            border-left: 6px solid #f48fb1 !important;
            color: #000000 !important;
            font-weight: bold;
        }

        .stDataFrame div {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        div[data-baseweb="select"] {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #ccc !important;
            border-radius: 6px;
        }

        .stSelectbox label {
            color: #000000 !important;
            font-weight: bold;
        }

        .stMarkdown {
            color: #000000 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Cargar dataset
df = pd.read_csv("kdrama_DATASET.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Menú lateral
st.sidebar.image("Nevertheless.jpg", caption="✨ K-drama vibes", use_container_width=True)
opcion = st.sidebar.radio("📌 Elige qué explorar:", [
    "🏠 Inicio",
    "📅 Producción por año",
    "🎭 Géneros más comunes",
    "☁️ Nube de palabras en títulos",
    "🔍 Filtrar por año",
    "🎮 Mini juego: ¿Verdadero o falso?"
])

# Inicio
if opcion == "🏠 Inicio":
    st.image("Songjoongkipng.png", use_container_width=True)
    st.markdown("<h1 style='text-align:center;'>Bienvenid@ a tu app de K-dramas ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Analiza, explora y diviértete con los mejores títulos coreanos 💕</p>", unsafe_allow_html=True)

# Producción por año
elif opcion == "📅 Producción por año":
    st.subheader("📈 Cantidad de K-dramas producidos por año")
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(x='year_of_release', data=df, order=sorted(df['year_of_release'].dropna().unique()), palette="pastel", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Géneros más comunes
elif opcion == "🎭 Géneros más comunes":
    st.subheader("🎬 Top 10 géneros más frecuentes en K-dramas")
    sns.set_style("whitegrid")
    generos = df['genre'].dropna().str.split(", ")
    generos_flat = [g for sublist in generos for g in sublist]
    conteo = Counter(generos_flat)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x=[g[0] for g in conteo.most_common(10)],
        y=[g[1] for g in conteo.most_common(10)],
        palette="pastel", ax=ax
    )
    ax.set_title("Géneros más frecuentes")
    ax.set_xlabel("Género")
    ax.set_ylabel("Frecuencia")
    st.pyplot(fig)

# Nube de palabras
elif opcion == "☁️ Nube de palabras en títulos":
    st.subheader("☁️ Palabras más comunes en los títulos de K-dramas")
    textos = " ".join(df['title'].dropna())
    wc = WordCloud(width=800, height=400, background_color="white", colormap="pink").generate(textos)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

# NUEVO: Filtrar por año
elif opcion == "🔍 Filtrar por año":
    st.subheader("📅 Filtrar K-dramas por año de estreno")
    
    with st.expander("Selecciona el año que quieres analizar"):
        años = sorted(df['year_of_release'].dropna().unique())
        año = st.selectbox("🎯 Año de lanzamiento", años, index=len(años)-1)

    filtrado = df[df['year_of_release'] == año]

    st.markdown(
        f"<div style='background-color:#ffe6ef; padding:10px; border-radius:8px; color:#000; font-weight:bold;'>🎬 Se encontraron {len(filtrado)} títulos en {año}.</div>",
        unsafe_allow_html=True
    )

    st.dataframe(filtrado[['title', 'genre', 'number_of_episodes']])
    st.image("Lovenextdoor.jpg", caption="Una escena de K-drama", use_container_width=True)

# NUEVO: Minijuego
elif opcion == "🎮 Mini juego: ¿Verdadero o falso?":
    st.subheader("🎲 Juego: ¿Verdadero o falso sobre los episodios?")

    if "puntos" not in st.session_state:
        st.session_state.puntos = 0
        st.session_state.ronda = 1
        st.session_state.jugando = True

    if st.session_state.ronda <= 3 and st.session_state.jugando:

        container = st.container()
        drama = df[['title', 'number_of_episodes']].dropna().sample(1).iloc[0]
        alterado = drama['number_of_episodes'] + random.choice([-3, -1, 0, +2, +4])

        container.markdown(f"### 🔹 Ronda {st.session_state.ronda}")
        container.markdown(f"**'{drama['title']}' tiene {alterado} episodios. ¿Verdadero o falso?**")

        col1, col2 = container.columns(2)
        with col1:
            if st.button("✅ Verdadero"):
                correcto = alterado == drama['number_of_episodes']
                if correcto:
                    st.success("¡Correcto!")
                    st.session_state.puntos += 1
                else:
                    st.error(f"Incorrecto. Tiene {drama['number_of_episodes']} episodios.")
                st.session_state.ronda += 1

        with col2:
            if st.button("❌ Falso"):
                correcto = alterado != drama['number_of_episodes']
                if correcto:
                    st.success("¡Correcto!")
                    st.session_state.puntos += 1
                else:
                    st.error(f"Incorrecto. Tiene {drama['number_of_episodes']} episodios.")
                st.session_state.ronda += 1

    elif st.session_state.ronda > 3:
        st.success(f"🎉 Juego terminado. Tu puntaje fue: {st.session_state.puntos}/3")
        if st.button("🔄 Volver a jugar"):
            st.session_state.puntos = 0
            st.session_state.ronda = 1
            st.session_state.jugando = True
        st.image("Collagecuadrado.jpg", caption="¡Gracias por jugar!", use_container_width=True)
