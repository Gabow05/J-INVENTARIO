import streamlit as st
from pexels_api import API
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Buscador de Imágenes", page_icon="🔍", layout="wide")

def buscar_imagenes_pexels(query, per_page=10):
    """
    Busca imágenes usando la API de Pexels
    """
    # URL de la API de Pexels
    url = f"https://api.pexels.com/v1/search?query={query}&per_page={per_page}"

    try:
        response = requests.get(
            url,
            headers={
                "Authorization": "Guest" # Modo invitado para pruebas básicas
            }
        )
        if response.status_code == 200:
            return response.json().get('photos', [])
        return []
    except Exception as e:
        st.error(f"Error al buscar imágenes: {str(e)}")
        return []

def main():
    st.markdown("""
    <h1 style='text-align: center; color: #3BA8A8;'>
        🔍 Buscador Mágico de Imágenes ✨
    </h1>
    """, unsafe_allow_html=True)

    # Descripción del servicio
    st.markdown("""
    <div style='padding: 15px; background-color: #f0f8ff; border-radius: 10px; margin-bottom: 20px;'>
        🎯 Encuentra imágenes perfectas para tu negocio
        <br>🖼️ Acceso a millones de imágenes profesionales
        <br>🏷️ Búsqueda inteligente por palabras clave
    </div>
    """, unsafe_allow_html=True)

    # Barra de búsqueda mejorada
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "🔍 Buscar imágenes",
            placeholder="¿Qué tipo de imagen estás buscando?",
            help="Escribe palabras clave como 'naturaleza', 'negocios', 'tecnología', etc."
        )
    with col2:
        num_results = st.select_slider(
            "📊 Número de resultados",
            options=[5, 10, 15, 20],
            value=10
        )

    # Filtros avanzados
    with st.expander("✨ Filtros avanzados"):
        col1, col2 = st.columns(2)
        with col1:
            orientation = st.selectbox(
                "📐 Orientación",
                ["Todas", "Horizontal", "Vertical", "Cuadrada"]
            )
        with col2:
            size = st.selectbox(
                "📏 Tamaño",
                ["Todas", "Grande", "Mediano", "Pequeño"]
            )

    # Búsqueda y visualización de resultados
    if search_query:
        with st.spinner('🔍 Buscando imágenes...'):
            resultados = buscar_imagenes_pexels(search_query, num_results)

            if resultados:
                st.markdown(f"### ✨ Resultados para: '{search_query}'")

                # Mostrar imágenes en un grid
                cols = st.columns(3)
                for idx, imagen in enumerate(resultados):
                    with cols[idx % 3]:
                        try:
                            # Cargar y mostrar imagen
                            img_url = imagen.get('src', {}).get('medium')
                            if img_url:
                                response = requests.get(img_url)
                                img = Image.open(BytesIO(response.content))
                                st.image(img, use_column_width=True)

                                # Información de la imagen
                                st.markdown(f"""
                                    📸 Fotógrafo: {imagen.get('photographer', 'Desconocido')}
                                    <br>📏 Dimensiones: {imagen.get('width')}x{imagen.get('height')}
                                    """, unsafe_allow_html=True)

                                # Botones de acción
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.button(f"⬇️ Descargar", key=f"download_{idx}")
                                with col2:
                                    st.button(f"💾 Guardar", key=f"save_{idx}")
                        except Exception as e:
                            st.error(f"Error al cargar imagen: {str(e)}")
            else:
                st.info("No se encontraron imágenes para tu búsqueda 😔")

    # Tutorial y consejos
    with st.sidebar:
        st.markdown("""
        <div style='padding: 15px; background-color: #f0f8ff; border-radius: 10px;'>
            <h3 style='color: #3BA8A8;'>📝 Tips de búsqueda</h3>
            <ul>
                <li>Usa palabras específicas</li>
                <li>Combina términos relacionados</li>
                <li>Prueba diferentes idiomas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='padding: 15px; background-color: #f0f8ff; border-radius: 10px; margin-top: 20px;'>
            <h3 style='color: #3BA8A8;'>🎯 Búsquedas populares</h3>
        </div>
        """, unsafe_allow_html=True)

        for tema in ["🏢 Negocios", "🌳 Naturaleza", "💻 Tecnología", "🎨 Arte"]:
            if st.button(tema, use_container_width=True):
                search_query = tema.split()[1]

if __name__ == "__main__":
    main()