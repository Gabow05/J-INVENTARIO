import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Buscador de Imágenes", page_icon="🔍", layout="wide")

def buscar_imagenes(query, per_page=10):
    """
    Busca imágenes usando la API pública de Pixabay
    """
    try:
        # API pública de Pixabay
        url = "https://pixabay.com/api/"
        params = {
            "key": "no-key",  # API pública modo demo
            "q": query,
            "per_page": per_page,
            "image_type": "photo"
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get('hits', [])
        return []
    except Exception as e:
        print(f"Error en búsqueda: {str(e)}")
        return []

def main():
    st.markdown("""
    <h1 style='text-align: center; color: #3BA8A8;'>
        🔍 Buscador de Imágenes ✨
    </h1>
    """, unsafe_allow_html=True)

    # Barra de búsqueda mejorada
    search_query = st.text_input(
        "🔍 Buscar imágenes",
        placeholder="Por ejemplo: paisajes, animales, tecnología...",
        help="Escribe palabras clave para encontrar imágenes"
    )

    # Área de visualización
    if search_query:
        # Mostrar imágenes de ejemplo (ya que no tenemos API key)
        st.info("🎨 Mostrando imágenes de ejemplo:")

        # Crear un grid de imágenes de ejemplo
        cols = st.columns(3)
        for i in range(6):  # Mostrar 6 imágenes de ejemplo
            with cols[i % 3]:
                # URL de imagen de ejemplo
                img_url = f"https://picsum.photos/400/300?random={i}"
                try:
                    response = requests.get(img_url)
                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content))
                        st.image(img, caption=f"Imagen de ejemplo #{i+1}", use_column_width=True)

                        # Botones de acción
                        col1, col2 = st.columns(2)
                        with col1:
                            st.button(f"⬇️ Descargar", key=f"down_{i}")
                        with col2:
                            st.button(f"🔍 Ver detalles", key=f"view_{i}")
                except Exception as e:
                    st.error(f"Error al cargar imagen: {str(e)}")
    else:
        # Mostrar sugerencias de búsqueda
        st.markdown("""
        <div style='padding: 20px; background-color: #f0f8ff; border-radius: 10px; margin: 20px 0;'>
            <h3>✨ Sugerencias de búsqueda</h3>
            <ul>
                <li>🌳 Naturaleza y paisajes</li>
                <li>🐾 Animales</li>
                <li>🏢 Negocios y oficinas</li>
                <li>💻 Tecnología</li>
                <li>🎨 Arte y diseño</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Pie de página
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        🖼️ Imágenes proporcionadas por Lorem Picsum
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()