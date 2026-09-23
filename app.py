import io
from google.generativeai import GenerativeModel
import google.generativeai as genai
import pandas as pd
from PIL import Image
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="App Calidad y Calorías - Verano", page_icon="📸", layout="wide"
)

st.title("📸 Tu App de Calorías con Cámara e IA")
st.markdown("Saca una foto a tu plato y deja que la IA calcule por ti.")

# Configuración de la API Key de Gemini en la barra lateral
st.sidebar.header("1. Configuración de IA")
api_key = st.sidebar.text_input(
    "Ingresa tu Gemini API Key",
    type="password",
    help="Necesaria para que la cámara analice las fotos.",
)

if not api_key:
    st.warning(
        "⚠️ Por favor, ingresa tu API Key de Google Gemini en la barra lateral"
        " para activar la función de la cámara con IA."
    )
    st.info(
        "💡 Puedes obtener una clave gratuita en [Google AI Studio]"
        " (aistudio.google.com) en menos de 1 minuto."
    )
else:
    genai.configure(api_key=api_key)

    # --- SECCIÓN: CÁMARA E IA ---
    st.subheader("2. Escanea tu Plato con la Cámara")
    foto_plato = st.camera_input("Apunta al plato de comida")

    if foto_plato is not None:
        imagen = Image.open(foto_plato)
        st.image(imagen, caption="Plato capturado", use_container_width=True)

        if st.button("✨ Analizar Calorías con IA", type="primary"):
            with st.spinner("Analizando ingredientes y calculando calorías..."):
                try:
                    # Usamos Gemini para analizar la imagen
                    model = GenerativeModel("gemini-1.5-flash")
                    prompt = (
                        "Analiza esta imagen de comida destinada a una dieta"
                        " de definición para el verano. Identifica el"
                        " plato/alimento, estima las calorías totales (kcal) y"
                        " los gramos de proteína de forma realista. Sé muy"
                        " conciso en la respuesta."
                    )
                    respuesta = model.generate_content([prompt, imagen])

                    st.success("¡Análisis completado!")
                    st.markdown("### 📊 Resultado:")
                    st.write(respuesta.text)

                except Exception as e:
                    st.error(
                        f"Hubo un error al procesar la imagen con la IA: {e}"
                    )