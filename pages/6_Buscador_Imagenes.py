import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import random

st.set_page_config(page_title="Buscador de Imágenes", page_icon="🔍", layout="wide")

def get_random_image_category(category, index):
    """
    Obtiene una imagen de Lorem Picsum basada en una categoría
    """
    categories = {
        "naturaleza": range(100, 200),
        "personas": range(200, 300),
        "tecnologia": range(300, 400),
        "animales": range(400, 500),
        "arquitectura": range(500, 600),
        "arte": range(600, 700)
    }

    # Si la categoría existe, usa su rango, si no, usa un rango aleatorio
    id_range = categories.get(category.lower(), range(1, 1000))
    image_id = random.choice(list(id_range))
    return f"https://picsum.photos/seed/{image_id}/400/300"

def main():
    st.markdown("""
    <h1 style='text-align: center; color: #3BA8A8;'>
        🔍 Buscador de Imágenes ✨
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='padding: 15px; background-color: #f0f8ff; border-radius: 10px; margin-bottom: 20px;'>
        🎯 Encuentra imágenes perfectas para tu negocio
        <br>🖼️ Biblioteca de imágenes de alta calidad
        <br>🏷️ Búsqueda por categorías
    </div>
    """, unsafe_allow_html=True)

    # Barra de búsqueda
    search_query = st.text_input(
        "🔍 Buscar imágenes",
        placeholder="Ejemplo: naturaleza, tecnología, arte...",
        help="Escribe una categoría para encontrar imágenes relacionadas"
    )

    # Área de visualización
    if search_query:
        st.markdown(f"### ✨ Mostrando resultados para: {search_query}")

        # Crear un grid de imágenes
        cols = st.columns(3)
        for i in range(6):  # Mostrar 6 imágenes
            with cols[i % 3]:
                try:
                    # Obtener URL de imagen basada en la categoría
                    img_url = get_random_image_category(search_query, i)
                    response = requests.get(img_url)

                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content))
                        st.image(
                            img, 
                            caption=f"Imagen #{i+1}",
                            use_container_width=True
                        )

                        # Botones de acción
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"⬇️ Descargar", key=f"down_{i}"):
                                st.markdown(f"[Descargar imagen]({img_url})")
                        with col2:
                            if st.button(f"🔍 Ver original", key=f"view_{i}"):
                                st.markdown(f"[Ver imagen original]({img_url})")
                except Exception as e:
                    st.error(f"Error al cargar imagen: {str(e)}")
    else:
        # Categorías sugeridas
        st.markdown("""
        <div style='padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin: 20px 0;'>
            <h3>✨ Categorías populares</h3>
            <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;'>
                <div>🌳 Naturaleza</div>
                <div>💻 Tecnología</div>
                <div>🎨 Arte</div>
                <div>🏢 Arquitectura</div>
                <div>🐾 Animales</div>
                <div>👥 Personas</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Pie de página
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        🖼️ Imágenes proporcionadas por Lorem Picsum | Alta calidad y libres de derechos
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()