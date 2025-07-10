import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import random
from collections import Counter

st.set_page_config(page_title="Explora el Universo de los K-dramas", layout="wide")

# ✅ CSS correcto según tus indicaciones
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

        /* ✅ Mensaje “Se encontraron…” con fondo rosa y texto negro */
        .stAlert-success {
            background-color: #ffe6ef !important;
            border-left: 6px solid #f48fb1 !important;
            color: #000000 !important;
            font-weight: bold;
        }

        /* ✅ Resultado de filtrado estilo limpio blanco y visible */
        .stDataFrame div {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        /* ✅ Selector de año estilo limpio */
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

        /* ✅ Radios del minijuego: texto negro, fondo claro */
        div[data-baseweb="radio"] label {
            background-color: #fff3f7 !important;
            color: #000000 !important;
            padding: 6px 12px;
            border-radius: 6px;
            font-weight: 500;
        }

        /* ✅ Botón “Responder”: fondo rosado claro, texto negro */
        button[kind="primary"] {
            background-color: #ffe4ec !important;
            color: #000000 !important;
            border: none;
            border-radius: 6px;
            padding: 8px 14px;
        }

        /* ✅ Texto de pregunta en minijuego */
        .stMarkdown {
            color: #000000 !important;
        }
    </style>
""", unsafe_allow_html=True)

# 📚 Cargar dataset
df = pd.read_csv("kdrama_DATASET.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# 📋 Menú lateral
st.sidebar.image("Nevertheless.jpg", caption="✨ K-drama vibes", use_container_width=True)
opcion = st.sidebar.radio("📌 Elige qué explorar:", [
    "🏠 Inicio",
    "📅 Producción por año",
    "🎭 Géneros más comunes",
    "☁️ Nube de palabras en títulos",
    "🔍 Filtrar por año",
    "🎮 Mini juego: ¿Verdadero o falso?"
])

# 🏠 Inicio
if opcion == "🏠 Inicio":
    st.image("Songjoongkipng.png", use_container_width=True)
    st.markdown("<h1 style='text-align:center;'>Bienvenid@ a tu app de K-dramas ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Analiza, explora y diviértete con los mejores títulos coreanos 💕</p>", unsafe_allow_html=True)

# 📅 Producción por año
elif opcion == "📅 Producción por año":
    st.subheader("📈 Cantidad de K-dramas producidos por año")
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(x='year_of_release', data=df, order=sorted(df['year_of_release'].dropna().unique()), palette="pastel", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 🎭 Géneros más comunes
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

# ☁️ Nube de palabras
elif opcion == "☁️ Nube de palabras en títulos":
    st.subheader("☁️ Palabras más comunes en los títulos de K-dramas")
    textos = " ".join(df['title'].dropna())
    wc = WordCloud(width=800, height=400, background_color="white", colormap="pink").generate(textos)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

# 🔍 Filtrar por año
elif opcion == "🔍 Filtrar por año":
    st.subheader("📅 Filtrar K-dramas por año de estreno")
    años = sorted(df['year_of_release'].dropna().unique())
    año = st.selectbox("Selecciona un año", años)
    filtrado = df[df['year_of_release'] == año]
    st.success(f"🎬 Se encontraron {len(filtrado)} títulos en {año}.")
    st.dataframe(filtrado[['title', 'genre', 'number_of_episodes']])
    st.image("Lovenextdoor.jpg", caption="Una escena de K-drama", use_container_width=True)

# 🎮 Minijuego
elif opcion == "🎮 Mini juego: ¿Verdadero o falso?":
    st.subheader("🎲 Adivina si el número de episodios es correcto")
    if "puntos" not in st.session_state:
        st.session_state.puntos = 0
        st.session_state.ronda = 1

    if st.session_state.ronda <= 3:
        drama = df[['title', 'number_of_episodes']].dropna().sample(1).iloc[0]
        alterado = drama['number_of_episodes'] + random.choice([-3, -1, 0, +2, +4])
        pregunta = f"'{drama['title']}' tiene {alterado} episodios. ¿Verdadero o falso?"
        st.markdown(f"🔹 Ronda {st.session_state.ronda}")
        st.markdown(f"**{pregunta}**")
        respuesta = st.radio("Selecciona tu respuesta:", ["Verdadero", "Falso"], key=f"ronda_{st.session_state.ronda}")

        if st.button("Responder", key=f"btn_{st.session_state.ronda}"):
            correcto = "Verdadero" if alterado == drama['number_of_episodes'] else "Falso"
            if respuesta == correcto:
                st.success("✅ ¡Correcto!")
                st.session_state.puntos += 1
            else:
                st.error(f"❌ Incorrecto. El número real es {drama['number_of_episodes']}.")
            st.session_state.ronda += 1
    else:
        st.success(f"🎉 Juego terminado. Tu puntaje final fue: {st.session_state.puntos}/3")
        if st.button("Reiniciar juego"):
            st.session_state.puntos = 0
            st.session_state.ronda = 1
        st.image("Collagecuadrado.jpg", caption="¡Gracias por jugar!", use_container_width=True)
