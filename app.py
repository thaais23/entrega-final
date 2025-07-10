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
elif opcion == "🎮 Mini juego: ¿Verdadero o falso?":
    st.markdown("<h2 style='color:#e91e63;'>🎲 Mini juego: ¿Verdadero o falso?</h2>", unsafe_allow_html=True)

    if "puntos" not in st.session_state:
        st.session_state.puntos = 0
    if "ronda" not in st.session_state:
        st.session_state.ronda = 1
    if "juego_terminado" not in st.session_state:
        st.session_state.juego_terminado = False
    if "mostrar_resultado" not in st.session_state:
        st.session_state.mostrar_resultado = False
    if "resultado_mensaje" not in st.session_state:
        st.session_state.resultado_mensaje = ""
    if "resultado_correcto" not in st.session_state:
        st.session_state.resultado_correcto = False

    if st.session_state.ronda <= 3 and not st.session_state.juego_terminado:
        st.markdown(f"<h4 style='color:#555'>🔹 Ronda {st.session_state.ronda} de 3</h4>", unsafe_allow_html=True)

        if "drama_actual" not in st.session_state:
            drama = df[['title', 'number_of_episodes']].dropna().sample(1).iloc[0]
            alterado = drama['number_of_episodes'] + random.choice([-3, -1, 0, +2, +4])
            st.session_state.drama_actual = drama
            st.session_state.episodios_mostrados = alterado

        st.markdown(f"""
            <div style='background-color:#fff3f8; padding:20px; border-radius:10px; margin-top:10px; margin-bottom:20px;'>
                <p style='font-size:18px; color:#111;'><b>'{st.session_state.drama_actual['title']}'</b> tiene <b>{st.session_state.episodios_mostrados}</b> episodios.<br>
                ¿Verdadero o falso?</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        if not st.session_state.mostrar_resultado:
            with col1:
                if st.button("✅ VERDADERO"):
                    if st.session_state.episodios_mostrados == st.session_state.drama_actual['number_of_episodes']:
                        st.session_state.resultado_mensaje = "¡Correcto!"
                        st.session_state.puntos += 1
                        st.session_state.resultado_correcto = True
                    else:
                        st.session_state.resultado_mensaje = f"Incorrecto. Tiene {st.session_state.drama_actual['number_of_episodes']} episodios."
                        st.session_state.resultado_correcto = False
                    st.session_state.mostrar_resultado = True

            with col2:
                if st.button("❌ FALSO"):
                    if st.session_state.episodios_mostrados != st.session_state.drama_actual['number_of_episodes']:
                        st.session_state.resultado_mensaje = "¡Correcto!"
                        st.session_state.puntos += 1
                        st.session_state.resultado_correcto = True
                    else:
                        st.session_state.resultado_mensaje = f"Incorrecto. Tiene {st.session_state.drama_actual['number_of_episodes']} episodios."
                        st.session_state.resultado_correcto = False
                    st.session_state.mostrar_resultado = True

        if st.session_state.mostrar_resultado:
            if st.session_state.resultado_correcto:
                st.success(st.session_state.resultado_mensaje)
            else:
                st.error(st.session_state.resultado_mensaje)

            if st.button("➡️ Siguiente ronda"):
                st.session_state.ronda += 1
                st.session_state.mostrar_resultado = False
                st.session_state.resultado_mensaje = ""
                st.session_state.resultado_correcto = False
                st.session_state.pop("drama_actual", None)

    elif st.session_state.ronda > 3:
        st.session_state.juego_terminado = True
        st.markdown(f"""
            <div style='background-color:#ffeef5; padding:20px; border-radius:10px;'>
                <h3 style='color:#000;'>🎉 Juego terminado</h3>
                <p style='font-size:16px;'>Tu puntaje final fue: <b>{st.session_state.puntos}/3</b></p>
            </div>
        """, unsafe_allow_html=True)
        st.image("Collagecuadrado.jpg", caption="¡Gracias por jugar!", use_container_width=True)

        if st.button("🔄 Volver a jugar"):
            st.session_state.puntos = 0
            st.session_state.ronda = 1
            st.session_state.juego_terminado = False
            st.session_state.mostrar_resultado = False
            st.session_state.resultado_mensaje = ""
            st.session_state.resultado_correcto = False
            st.session_state.pop("drama_actual", None)
