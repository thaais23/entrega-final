import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import random
from collections import Counter

# 🌸 Configuración general de la app
st.set_page_config(
    page_title="Explora el Universo de los K-dramas",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 Fondo pastel usando markdown y CSS
st.markdown(
    """
    <style>
        body {
            background-color: #fff0f5;
        }
        .stApp {
            background-color: #fff0f5;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 📷 Imagen decorativa de entrada
st.image("Songjoongkipng.png", use_column_width=True)

# 🌺 Título
st.markdown("<h1 style='text-align:center; color:#e91e63;'>Explora el Universo de los K-dramas</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Visualiza, analiza y juega con 350 títulos de K-dramas desde 2003 hasta 2025.</p>", unsafe_allow_html=True)
st.divider()

# 📚 Cargar dataset
df = pd.read_csv("kdrama_DATASET.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# 📷 Imagen decorativa en sidebar
st.sidebar.image("Nevertheless", caption="✨ K-drama vibes", use_column_width=True)

# 📋 Menú principal
opcion = st.sidebar.radio("📌 Elige qué explorar:", [
    "📅 Producción por año",
    "🎭 Géneros más comunes",
    "☁️ Nube de palabras en títulos",
    "🔍 Filtrar por año",
    "🎮 Mini juego: ¿Verdadero o falso?"
])

# 📈 Opción 1: Producción por año
if opcion == "📅 Producción por año":
    st.subheader("📈 Cantidad de K-dramas producidos por año")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(x='year_of_release', data=df, order=sorted(df['year_of_release'].dropna().unique()), palette="pastel", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 🎭 Opción 2: Géneros más comunes
elif opcion == "🎭 Géneros más comunes":
    st.subheader("🎬 Top 10 géneros más frecuentes en K-dramas")
    generos = df['genre'].dropna().str.split(", ")
    generos_flat = [item for sublist in generos for item in sublist]
    conteo = Counter(generos_flat)
    df_gen = pd.DataFrame(conteo.most_common(10), columns=["Género", "Frecuencia"])
    st.bar_chart(df_gen.set_index("Género"))

# ☁️ Opción 3: Nube de palabras
elif opcion == "☁️ Nube de palabras en títulos":
    st.subheader("☁️ Palabras más comunes en los títulos de K-dramas")
    textos = " ".join(df['title'].dropna())
    wc = WordCloud(width=800, height=400, background_color="white", colormap="pink").generate(textos)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

# 🔍 Opción 4: Filtro por año
elif opcion == "🔍 Filtrar por año":
    st.subheader("📅 Filtra los K-dramas por año de estreno")
    años = sorted(df['year_of_release'].dropna().unique())
    año = st.selectbox("Selecciona un año", años)
    filtrado = df[df['year_of_release'] == año]
    st.success(f"🎬 Se encontraron {len(filtrado)} títulos en {año}.")
    st.dataframe(filtrado[['title', 'genre', 'number_of_episodes']])

    # Imagen de ambientación decorativa
    st.image("Lovenextdoor", caption="Una escena de K-drama", use_column_width=False, width=300)

# 🎮 Opción 5: Mini juego interactivo
elif opcion == "🎮 Mini juego: ¿Verdadero o falso?":
    st.subheader("🎲 Adivina el número de episodios... ¿verdadero o falso?")
    if "puntos" not in st.session_state:
        st.session_state.puntos = 0
        st.session_state.ronda = 1

    if st.session_state.ronda <= 3:
        drama = df[['title', 'number_of_episodes']].dropna().sample(1).iloc[0]
        alterado = drama['number_of_episodes'] + random.choice([-3, -1, 0, +2, +4])
        pregunta = f"'{drama['title']}' tiene {alterado} episodios. ¿Verdadero o falso?"
        st.write(f"🔹 Ronda {st.session_state.ronda}")
        respuesta = st.radio(pregunta, ["Verdadero", "Falso"], key=f"ronda_{st.session_state.ronda}")

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
        st.image("Collagecuadrado", caption="¡Gracias por jugar!", use_column_width=False, width=250)
