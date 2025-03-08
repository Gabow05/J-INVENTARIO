import streamlit as st
from pexels_api import API
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Buscador de Imágenes", page_icon="🔍", layout="wide")

# API Key pública de demo de Pexels
PEXELS_API_KEY = "563492ad6f91700001000001f89979b6f6934dc49be8e276f91322c1"

def buscar_imagenes(query, per_page=10):
    """
    Busca imágenes usando la biblioteca Pexels API
    """
    try:
        api = API(PEXELS_API_KEY)
        api.search(query, page=1, results_per_page=per_page)
        photos = api.get_entries()
        return photos
    except Exception as e:
        st.error(f"Error al buscar imágenes: {str(e)}")
        return []

def main():
    st.markdown("""
    <h1 style='text-align: center; color: #3BA8A8;'>
        🔍 Buscador Mágico de Imágenes ✨
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='padding: 15px; background-color: #f0f8ff; border-radius: 10px; margin-bottom: 20px;'>
        🎯 Encuentra imágenes perfectas para tu negocio
        <br>🖼️ Acceso a millones de imágenes profesionales
        <br>🏷️ Búsqueda inteligente por palabras clave
    </div>
    """, unsafe_allow_html=True)

    # Barra de búsqueda
    search_query = st.text_input(
        "🔍 Buscar imágenes",
        placeholder="Por ejemplo: naturaleza, negocios, tecnología...",
        help="Escribe lo que quieras buscar"
    )

    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        num_results = st.slider("📊 Número de resultados", 5, 30, 15)
    with col2:
        orientation = st.selectbox(
            "📐 Orientación",
            ["Todas", "Horizontal", "Vertical", "Cuadrada"]
        )

    if search_query:
        with st.spinner('🔍 Buscando imágenes...'):
            imagenes = buscar_imagenes(search_query, num_results)

            if imagenes:
                st.success(f"✨ Se encontraron {len(imagenes)} imágenes para '{search_query}'")

                # Mostrar imágenes en grid
                cols = st.columns(3)
                for idx, img in enumerate(imagenes):
                    with cols[idx % 3]:
                        try:
                            # Obtener URL de la imagen
                            img_url = img.medium

                            # Mostrar imagen
                            response = requests.get(img_url)
                            image = Image.open(BytesIO(response.content))
                            st.image(image, caption=f"📸 Por: {img.photographer}")

                            # Botones de acción
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button(f"⬇️ Descargar", key=f"down_{idx}"):
                                    st.markdown(f"[Descargar imagen]({img.original})")
                            with col2:
                                if st.button(f"🔍 Ver detalles", key=f"view_{idx}"):
                                    st.write(f"Dimensiones: {img.width}x{img.height}")
                        except Exception as e:
                            st.error(f"Error al cargar imagen: {str(e)}")
            else:
                st.warning("No se encontraron imágenes. Intenta con otras palabras clave 🔍")

    # Sugerencias de búsqueda
    st.sidebar.markdown("""
    <div style='padding: 15px; background-color: #f0f8ff; border-radius: 10px;'>
        <h3 style='color: #3BA8A8;'>🎯 Búsquedas populares</h3>
    </div>
    """, unsafe_allow_html=True)

    sugerencias = ["🏢 Oficina", "🌳 Naturaleza", "💻 Tecnología", "🎨 Arte", "🏃 Deportes"]
    for sugerencia in sugerencias:
        if st.sidebar.button(sugerencia, use_container_width=True):
            search_query = sugerencia.split()[1]

if __name__ == "__main__":
    main()