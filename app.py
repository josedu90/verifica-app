import streamlit as st
from PIL import Image, ExifTags
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Verificador 316ads",
    page_icon="🛡️",
    layout="centered"
)

st.markdown("""
<style>
.big-font { font-size:20px !important; font-weight: bold; color: #2E86C1; }
.warning { color: #E74C3C; font-weight: bold; }
.success { color: #27AE60; font-weight: bold; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Verifica-Info")
st.markdown("### Herramienta Forense por 316ads")
st.info("Sube una imagen para detectar si es antigua o si tiene metadatos manipulados.")

def get_exif_data(image):
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = ExifTags.TAGS.get(tag, tag)
            if decoded == "DateTimeOriginal":
                exif_data['Fecha Original'] = value
            if decoded == "Model":
                exif_data['Dispositivo'] = value
            if decoded == "Software":
                exif_data['Software'] = value
    return exif_data

uploaded_file = st.file_uploader("Sube foto o captura aquí:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen analizada", use_column_width=True)

    st.markdown("---")
    st.markdown('<p class="big-font">🔍 Informe Técnico:</p>', unsafe_allow_html=True)

    exif = get_exif_data(image)

    if exif:
        if 'Fecha Original' in exif:
            fecha = exif['Fecha Original']
            st.write(f"📅 **Fecha de captura:** {fecha}")
            try:
                dt_obj = datetime.strptime(fecha, '%Y:%m:%d %H:%M:%S')
                if dt_obj.year < 2024:
                    st.markdown('<p class="warning">⚠️ ALERTA: Imagen ANTIGUA.</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p class="success">✅ La imagen es reciente.</p>', unsafe_allow_html=True)
            except:
                pass
        else:
            st.warning("⚠️ Sin fecha en metadatos.")

        if 'Software' in exif:
            st.markdown(f'<p class="warning">⚠️ SOFTWARE DETECTADO: {exif["Software"]}</p>', unsafe_allow_html=True)
    else:
        st.error("❌ Sin metadatos. Posible captura de pantalla o imagen reenviada.")

    st.markdown("---")
    st.markdown("### 🕵️ Verificación Visual")
    st.markdown("[🔎 Buscar esta imagen en Google Lens](https://lens.google.com/)", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Desarrollado por 316ads")
    st.markdown("Expertos en Inteligencia Artificial y Marketing.")
    st.markdown("[Visitar sitio web](https://316ads.com)")
