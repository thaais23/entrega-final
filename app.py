import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import random
from collections import Counter

st.set_page_config(page_title="Explora el Universo de los K-dramas", layout="wide")

# Estilos globales
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #fff0f5;
            color: #222;
        }

        section[data-testid="stSidebar"] {
            background-color: #dddddd !important;
        }

        h1, h2, h3, h4 {
            color: #e91e63 !important;
        }

        .stButton>button {
            background-color: #f8bbd0;
            color: #000;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.5em 1em;
            border: none;
        }

        div.row-widget.stRadio > div {
            flex-direction: row;
        }
        div.row-widget.stRadio label {
            color: #000000 !important;
            font-weight: 600;
            background-color: #fce4ec;
            padding: 10px 15px;
            border-radius: 8px;
            margin: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Cargar dataset
df = pd.read_csv("kdrama_DATASET.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Sidebar
st.sidebar.image("Nevertheless.jpg", caption="✨ K-drama vibes", use_container_width=True)
opcion = st.sidebar.radio("📌 Elige qué explorar:", [
    "🏠 Inicio",
    "📅 Producción por año",
    "🎭 Géneros más comunes",
    "☁️ Nube de palabras en títulos",
    "🔍 Filtrar por año",
    "🎮 Mini juego: ¿Verdadero o falso?"
])

# PÁGINA: INICIO
if opcion == "🏠 Inicio":
    st.image("Songjoongkipng.png", use_container_width=True)
    st.markdown("<h1 style='text-align:center;'>Bienvenid@ a tu app de K-dramas ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Analiza, explora y diviértete con los mejores títulos coreanos 💕</p>", unsafe_allow_html=True)

# PRODUCCIÓN POR AÑO
elif opcion == "📅 Producción por año":
    st.subheader("📈 Cantidad de K-dramas producidos por año")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(x='year_of_release', data=df, order=sorted(df['year_of_release'].dropna().unique()), palette="pastel", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# GÉNEROS MÁS COMUNES
elif opcion == "🎭 Géneros más comunes":
    st.subheader("🎬 Top 10 géneros más frecuentes en K-dramas")
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

# NUBE DE PALABRAS
elif opcion == "☁️ Nube de palabras en títulos":
    st.subheader("☁️ Palabras más comunes en los títulos de K-dramas")
    textos = " ".join(df['title'].dropna())
    wc = WordCloud(width=800, height=400, background_color="white", colormap="pink").generate(textos)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

# FILTRAR POR AÑO
elif opcion == "🔍 Filtrar por año":
    st.subheader("📅 Busca K-dramas por año de estreno")
    años = sorted(df['year_of_release'].dropna().unique())
    año = st.slider("Selecciona el año", int(min(años)), int(max(años)), int(max(años)))
    filtrado = df[df['year_of_release'] == año]
    st.markdown(
        f"<div style='background-color:#ffeef5; padding:15px; border-radius:10px; color:#111; font-weight:600;'>🎬 En {año} se estrenaron <b>{len(filtrado)}</b> títulos.</div>",
        unsafe_allow_html=True
    )
    if not filtrado.empty:
        for index, row in filtrado.iterrows():
            st.markdown(f"""
                <div style='background-color:#ffffff; border-radius:8px; padding:10px; margin-bottom:10px; border:1px solid #f0c3d0'>
                    <b>{row['title']}</b><br>
                    🎭 <i>{row['genre']}</i> &nbsp;&nbsp;|&nbsp;&nbsp; 🎞️ {row['number_of_episodes']} episodios
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No se encontraron resultados para este año.")
    st.image("Lovenextdoor.jpg", caption="Una escena de K-drama", use_container_width=True)

# MINI JUEGO
elif opcion == "🎮 Mini juego: ¿Verdadero o falso?":
    st.markdown("<h2 style='color:#e91e63;'>🎲 Mini juego: ¿Verdadero o falso?</h2>", unsafe_allow_html=True)

    # Inicializar estados
    for clave, valor in {
        "ronda": 1,
        "puntos": 0,
        "drama": None,
        "respuesta": "",
        "resultado": "",
        "mostrar_pregunta": True,
        "juego_terminado": False
    }.items():
        if clave not in st.session_state:
            st.session_state[clave] = valor

    if st.session_state.juego_terminado:
        st.success(f"🎉 Juego terminado. Tu puntaje fue: {st.session_state.puntos}/3")
        st.image("Collagecuadrado.jpg", caption="¡Gracias por jugar!", use_container_width=True)
        if st.button("🔄 Volver a jugar"):
            for clave in ["ronda", "puntos", "drama", "respuesta", "resultado", "mostrar_pregunta", "juego_terminado"]:
                st.session_state[clave] = {
                    "ronda": 1,
                    "puntos": 0,
                    "drama": None,
                    "respuesta": "",
                    "resultado": "",
                    "mostrar_pregunta": True,
                    "juego_terminado": False
                }[clave]
        st.stop()

    st.markdown(f"<h4 style='color:#444;'>🔹 Ronda {st.session_state.ronda} de 3</h4>", unsafe_allow_html=True)

    if st.session_state.drama is None:
        muestra = df[['title', 'number_of_episodes']].dropna()
        elegido = muestra.sample(1).iloc[0]
        titulo = str(elegido['title'])
        real = int(elegido['number_of_episodes'])
        mostrado = real + random.choice([-3, -2, 0, +2, +3])
        st.session_state.drama = {"titulo": titulo, "real": real, "mostrado": mostrado}

    drama = st.session_state.drama

    if st.session_state.mostrar_pregunta:
        st.markdown(f"""
            <div style='background-color:#fff3f8; padding:25px; border-radius:12px;'>
                <p style='font-size:18px; color:#000;'><b>{drama['titulo']}</b> tiene <b>{drama['mostrado']}</b> episodios.</p>
                <p style='font-size:16px; color:#000;'>¿Crees que eso es verdadero o falso?</p>
            </div>
        """, unsafe_allow_html=True)

        respuesta = st.radio("Selecciona tu respuesta", ["Verdadero", "Falso"], index=None, horizontal=True, label_visibility="collapsed")

        if respuesta:
            if st.button("📩 Confirmar respuesta"):
                correcta = (
                    (respuesta == "Verdadero" and drama['mostrado'] == drama['real']) or
                    (respuesta == "Falso" and drama['mostrado'] != drama['real'])
                )
                if correcta:
                    st.session_state.resultado = f"✅ ¡Correcto! Tiene {drama['real']} episodios."
                    st.session_state.puntos += 1
                else:
                    st.session_state.resultado = f"❌ Incorrecto. Tiene {drama['real']} episodios."
                st.session_state.mostrar_pregunta = False

    if not st.session_state.mostrar_pregunta:
        st.markdown(f"""
            <div style='background-color:#ffe6ef; padding:15px; border-radius:10px; color:#000; font-size:16px;'>
                {st.session_state.resultado}
            </div>
        """, unsafe_allow_html=True)

        if st.button("➡️ Siguiente ronda"):
            st.session_state.ronda += 1
            st.session_state.drama = None
            st.session_state.respuesta = ""
            st.session_state.resultado = ""
            st.session_state.mostrar_pregunta = True
            if st.session_state.ronda > 3:
                st.session_state.juego_terminado = True
