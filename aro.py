import streamlit as st
import ollama
from groq import Groq
import os

# Configuración de la página
st.set_page_config(page_title="Aro: Ingeniero Químico", page_icon="🧪")
st.title("🧪 Aro: El Ingeniero Químico")

# Selector de modo
modo = st.radio("Selecciona el motor de Aro:", ("Modo Local (Privado)", "Modo Nube (Rápido)"))

# Entrada de usuario
pregunta = st.text_input("Haz tu consulta técnica:")

if st.button("Consultar a Aro"):
    if not pregunta:
        st.warning("Por favor, escribe una pregunta.")
    else:
        # Contenedor para mostrar la respuesta en tiempo real
        contenedor = st.empty()
        texto_completo = ""

        if modo == "Modo Local (Privado)":
            st.info("Procesando localmente...")
            try:
                stream = ollama.chat(
                    model='Aro', 
                    messages=[{'role': 'user', 'content': pregunta}],
                    stream=True
                )
                for parte in stream:
                    texto_completo += parte['message']['content']
                    contenedor.markdown(texto_completo + "▌")
                contenedor.markdown(texto_completo)
            except Exception as e:
                st.error(f"Error en motor local: {e}")

        else:  # Modo Nube (Groq)
            st.info("Consultando la nube de Groq...")
            try:
                client = Groq(api_key="Key")
                
                # Definimos la personalidad de Aro aquí
                instrucciones_aro = """Eres Aro, un químico experto en compuestos aromáticos con una maestría en ingeniería de sistemas. Tu comportamiento debe seguir estas reglas estrictas:
1. RELACIÓN OBLIGATORIA: Debes relacionar cada concepto químico con la ingeniería de sistemas/informática, incluso si no se te pide explícitamente. Es tu sello de identidad.
2. CONCISIÓN: Responde únicamente lo que se te pregunta. Ve al grano. Evita introducciones innecesarias o conclusiones largas. Si el usuario pregunta algo, responde de forma directa y técnica.
3. CREATIVIDAD: Sé extremadamente creativo al trazar paralelismos. Compara orbitales con ancho de banda, aromaticidad con resiliencia de red, sustituciones con parches de software, y estabilidad electrónica con integridad de datos.
4. FILTRO DE TEMA: Tu especialidad es exclusivamente la química aromática y su relación con sistemas. Si se te pregunta algo fuera de este alcance, declina cortésmente."""

                stream = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": instrucciones_aro}, # <--- ¡Aquí está la magia!
                        {"role": "user", "content": pregunta}
                    ],
                    model="llama-3.3-70b-versatile",
                    stream=True
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        texto_completo += chunk.choices[0].delta.content
                        contenedor.markdown(texto_completo + "▌")
                contenedor.markdown(texto_completo)
            except Exception as e:
                st.error(f"Error en modo nube: {e}")
