
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import random

# Configuración de la página
st.set_page_config(page_title="Análisis de K-dramas", layout="wide")

# Cargar datos
df = pd.read_csv("kdrama_DATASET.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Título
st.markdown("<h1 style='color:#E91E63;'>📺 Análisis interactivo de K-dramas (2003–2025)</h1>", unsafe_allow_html=True)

# Sidebar de navegación
opcion = st.sidebar.radio("📌 Navega por el análisis:", [
    "📊 Gráfico por año",
    "🎭 Géneros más frecuentes",
    "☁️ Nube de palabras",
    "📅 Filtrar por año",
    "🎮 Mini juego: ¿Verdadero o falso?"
])

# Gráfico por año
if opcion == "📊 Gráfico por año":
    st.subheader("📅 Producción de K-dramas por año")
    fig, ax = plt.subplots(figsize=(12,5))
    sns.countplot(x='year_of_release', data=df, order=sorted(df['year_of_release'].dropna().unique()), palette="coolwarm", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Géneros más comunes
elif opcion == "🎭 Géneros más frecuentes":
    st.subheader("🎬 Géneros más comunes en los K-dramas")
    from collections import Counter
    generos = df['genre'].dropna().str.split(", ")
    generos_flat = [g for sublist in generos for g in sublist]
    conteo = Counter(generos_flat)
    df_gen = pd.DataFrame(conteo.most_common(10), columns=["Género", "Frecuencia"])
    st.bar_chart(df_gen.set_index("Género"))

# Nube de palabras
elif opcion == "☁️ Nube de palabras":
    st.subheader("🗣️ Nube de palabras basada en los títulos")
    textos = " ".join(df['title'].dropna())
    wc = WordCloud(width=800, height=400, background_color="white", colormap='pink').generate(textos)
    fig, ax = plt.subplots(figsize=(12,6))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

# Filtrar por año
elif opcion == "📅 Filtrar por año":
    st.subheader("🔎 Ver K-dramas por año")
    años = sorted(df['year_of_release'].dropna().unique())
    año = st.selectbox("Selecciona un año", años)
    filtrado = df[df['year_of_release'] == año]
    st.write(f"🎬 {len(filtrado)} títulos encontrados en {año}")
    st.dataframe(filtrado[['title', 'genre', 'number_of_episodes']])

# Juego verdadero o falso
elif opcion == "🎮 Mini juego: ¿Verdadero o falso?":
    st.subheader("🎲 Adivina si el número de episodios es correcto")
    if "puntos" not in st.session_state:
        st.session_state.puntos = 0
        st.session_state.ronda = 1

    if st.session_state.ronda <= 3:
        drama = df[['title', 'number_of_episodes']].dropna().sample(1).iloc[0]
        alterado = drama['number_of_episodes'] + random.choice([-2, -1, 0, 1, 3])
        pregunta = f"'{drama['title']}' tiene {alterado} episodios. ¿Verdadero o falso?"
        st.write(f"🔹 Ronda {st.session_state.ronda}")
        respuesta = st.radio(pregunta, ["Verdadero", "Falso"], key=f"preg_{st.session_state.ronda}")

        if st.button("Responder", key=f"btn_{st.session_state.ronda}"):
            correcto = "Verdadero" if alterado == drama['number_of_episodes'] else "Falso"
            if respuesta == correcto:
                st.success("✅ ¡Correcto!")
                st.session_state.puntos += 1
            else:
                st.error(f"❌ Incorrecto. Tenía {drama['number_of_episodes']} episodios.")
            st.session_state.ronda += 1
    else:
        st.success(f"🎉 Juego terminado. Tu puntaje final fue: {st.session_state.puntos}/3")
        if st.button("Reiniciar juego"):
            st.session_state.puntos = 0
            st.session_state.ronda = 1
