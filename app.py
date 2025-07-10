# MINI JUEGO DEFINITIVO SIN ERRORES
elif opcion == "🎮 Mini juego: ¿Verdadero o falso?":
    st.markdown("<h2 style='color:#e91e63;'>🎲 Mini juego: ¿Verdadero o falso?</h2>", unsafe_allow_html=True)

    if "estado_juego" not in st.session_state:
        st.session_state.estado_juego = {
            "ronda": 1,
            "puntos": 0,
            "drama": None,
            "respuesta": "",
            "resultado": "",
            "mostrar_pregunta": True,
            "juego_terminado": False,
            "siguiente_ronda": False,
            "reiniciar": False
        }

    estado = st.session_state.estado_juego

    if estado["reiniciar"]:
        st.session_state.estado_juego = {
            "ronda": 1,
            "puntos": 0,
            "drama": None,
            "respuesta": "",
            "resultado": "",
            "mostrar_pregunta": True,
            "juego_terminado": False,
            "siguiente_ronda": False,
            "reiniciar": False
        }
        st.experimental_rerun()

    if estado["siguiente_ronda"]:
        estado["ronda"] += 1
        if estado["ronda"] > 3:
            estado["juego_terminado"] = True
        else:
            estado["drama"] = None
            estado["respuesta"] = ""
            estado["resultado"] = ""
            estado["mostrar_pregunta"] = True
        estado["siguiente_ronda"] = False
        st.experimental_rerun()

    if estado["juego_terminado"]:
        st.success(f"🎉 Juego terminado. Tu puntaje fue: {estado['puntos']}/3")
        st.image("Collagecuadrado.jpg", caption="¡Gracias por jugar!", use_container_width=True)
        if st.button("🔄 Volver a jugar"):
            estado["reiniciar"] = True
        st.stop()

    st.markdown(f"<h4 style='color:#444;'>🔹 Ronda {estado['ronda']} de 3</h4>", unsafe_allow_html=True)

    if estado["drama"] is None:
        muestra = df[['title', 'number_of_episodes']].dropna()
        elegido = muestra.sample(1).iloc[0]
        titulo = str(elegido['title'])
        real = int(elegido['number_of_episodes'])
        mostrado = real + random.choice([-3, -2, 0, +2, +3])
        estado["drama"] = {"titulo": titulo, "real": real, "mostrado": mostrado}

    drama = estado["drama"]

    if estado["mostrar_pregunta"]:
        st.markdown(f"""
            <div style='background-color:#fff3f8; padding:25px; border-radius:12px;'>
                <p style='font-size:18px; color:#000;'><b>{drama['titulo']}</b> tiene <b>{drama['mostrado']}</b> episodios.</p>
                <p style='font-size:16px; color:#000;'>¿Crees que eso es <b style='color:#000;'>verdadero</b> o <b style='color:#000;'>falso</b>?</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✔️ Verdadero"):
                estado["respuesta"] = "Verdadero"
        with col2:
            if st.button("❌ Falso"):
                estado["respuesta"] = "Falso"

        if estado["respuesta"]:
            correcta = (
                (estado["respuesta"] == "Verdadero" and drama['mostrado'] == drama['real']) or
                (estado["respuesta"] == "Falso" and drama['mostrado'] != drama['real'])
            )
            if correcta:
                estado["resultado"] = f"✅ ¡Correcto! Tiene {drama['real']} episodios."
                estado["puntos"] += 1
            else:
                estado["resultado"] = f"❌ Incorrecto. Tiene {drama['real']} episodios."
            estado["mostrar_pregunta"] = False
            st.experimental_rerun()

    if not estado["mostrar_pregunta"] and estado["resultado"]:
        st.markdown(f"""
            <div style='background-color:#ffe6ef; padding:15px; border-radius:10px; color:#000; font-size:16px;'>
                {estado["resultado"]}
            </div>
        """, unsafe_allow_html=True)

        if st.button("➡️ Siguiente ronda"):
            estado["siguiente_ronda"] = True
