import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import random
from collections import Counter

st.set_page_config(page_title="Explora el Universo de los K-dramas", layout="wide")

# Estilos personalizados
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

        .stSelectbox label, .stSlider label {
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
# Filtrar por año
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

# Mini juego reorganizado y sin errores
# Estilo de texto para radio
elif opcion == "🎮 Mini juego: ¿Verdadero o falso?":
    st.markdown("<h2 style='color:#e91e63;'>🎲 Mini juego: ¿Verdadero o falso?</h2>", unsafe_allow_html=True)

    # Inicializar estados
    if "ronda" not in st.session_state:
        st.session_state.ronda = 1
        st.session_state.puntos = 0
        st.session_state.drama = None
        st.session_state.respuesta = ""
        st.session_state.resultado = ""
        st.session_state.mostrar_pregunta = True
        st.session_state.juego_terminado = False

    # Reset juego si ya terminó
    if st.session_state.juego_terminado:
        st.success(f"🎉 Juego terminado. Tu puntaje fue: {st.session_state.puntos}/3")
        st.image("Collagecuadrado.jpg", caption="¡Gracias por jugar!", use_container_width=True)
        if st.button("🔄 Volver a jugar"):
            st.session_state.ronda = 1
            st.session_state.puntos = 0
            st.session_state.drama = None
            st.session_state.respuesta = ""
            st.session_state.resultado = ""
            st.session_state.mostrar_pregunta = True
            st.session_state.juego_terminado = False
        st.stop()

    # Mostrar ronda
    st.markdown(f"<h4 style='color:#444;'>🔹 Ronda {st.session_state.ronda} de 3</h4>", unsafe_allow_html=True)

    # Seleccionar drama si no existe
    if st.session_state.drama is None:
        muestra = df[['title', 'number_of_episodes']].dropna()
        elegido = muestra.sample(1).iloc[0]
        titulo = str(elegido['title'])
        real = int(elegido['number_of_episodes'])
        mostrado = real + random.choice([-3, -2, 0, +2, +3])
        st.session_state.drama = {
            "titulo": titulo,
            "real": real,
            "mostrado": mostrado
        }

    drama = st.session_state.drama

    # Mostrar pregunta
    if st.session_state.mostrar_pregunta:
        st.markdown(f"""
            <div style='background-color:#fff3f8; padding:25px; border-radius:12px;'>
                <p style='font-size:18px; color:#000;'><b>{drama['titulo']}</b> tiene <b>{drama['mostrado']}</b> episodios.</p>
                <p style='font-size:16px; color:#000;'>¿Crees que eso es verdadero o falso?</p>
            </div>
        """, unsafe_allow_html=True)

        respuesta = st.radio(
            "Selecciona tu respuesta",
            ["Verdadero", "Falso"],
            index=None,
            horizontal=True,
            label_visibility="collapsed"
        )

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

    # Mostrar resultado
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
