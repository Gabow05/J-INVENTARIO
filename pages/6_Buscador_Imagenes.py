import streamlit as st
import os
from PIL import Image
import pandas as pd

st.set_page_config(page_title="Buscador de Imágenes", page_icon="🔍", layout="wide")

def search_images(query, categoria=None):
    """
    Simula una búsqueda de imágenes basada en texto
    """
    resultados = [
        {
            'titulo': '📱 Imagen de producto 1',
            'descripcion': '✨ Fotografía profesional de producto',
            'categoria': 'Productos',
            'tags': ['producto', 'tecnología', 'gadget']
        },
        {
            'titulo': '🎨 Diseño para redes sociales',
            'descripcion': '🎯 Banner promocional optimizado',
            'categoria': 'Marketing',
            'tags': ['marketing', 'social media', 'diseño']
        }
    ]

    if categoria:
        resultados = [r for r in resultados if r['categoria'] == categoria]

    return resultados

def main():
    st.markdown("""
    <h1 style='text-align: center; color: #3BA8A8;'>
        🔍 Buscador Mágico de Imágenes ✨
    </h1>
    """, unsafe_allow_html=True)

    # Descripción del servicio
    st.markdown("""
    <div style='padding: 15px; background-color: #f0f8ff; border-radius: 10px; margin-bottom: 20px;'>
        🎯 Encuentra la imagen perfecta para tu negocio
        <br>🖼️ Biblioteca de imágenes optimizada
        <br>🏷️ Búsqueda inteligente por etiquetas
    </div>
    """, unsafe_allow_html=True)

    # Barra de búsqueda mejorada
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "🔍 Buscar imágenes",
            placeholder="¿Qué tipo de imagen estás buscando?",
            help="Escribe palabras clave para encontrar imágenes"
        )
    with col2:
        categoria = st.selectbox(
            "📁 Categoría",
            ["📌 Todas", "📦 Productos", "📢 Marketing", "🎨 Logos", "🖼️ Banners"]
        )

    # Filtros avanzados con estilo
    with st.expander("✨ Filtros avanzados"):
        col1, col2, col3 = st.columns(3)
        with col1:
            formato = st.multiselect(
                "📄 Formato",
                ["📸 JPG", "🎨 PNG", "✏️ SVG", "🎬 GIF"]
            )
        with col2:
            tamaño = st.select_slider(
                "📏 Tamaño mínimo",
                options=["🔹 Pequeño", "🔸 Mediano", "💠 Grande"]
            )
        with col3:
            fecha = st.date_input("📅 Fecha desde")

    # Área de resultados mejorada
    if search_query:
        resultados = search_images(
            search_query,
            categoria.split(" ")[1] if categoria != "📌 Todas" else None
        )

        st.markdown(f"""
        <h3 style='color: #3BA8A8;'>
            🎯 Resultados para: "{search_query}"
        </h3>
        """, unsafe_allow_html=True)

        # Grid de resultados con estilo
        for resultado in resultados:
            with st.container():
                st.markdown(f"""
                <div style='padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 20px;'>
                    <h4>{resultado['titulo']}</h4>
                    <p>{resultado['descripcion']}</p>
                    <p><strong>📁 Categoría:</strong> {resultado['categoria']}</p>
                    <p><strong>🏷️ Tags:</strong> {', '.join(['#'+tag for tag in resultado['tags']])}</p>
                </div>
                """, unsafe_allow_html=True)

    # Área de carga de imágenes mejorada
    st.markdown("""
    <h3 style='color: #3BA8A8;'>
        📤 Subir Nuevas Imágenes
    </h3>
    """, unsafe_allow_html=True)

    with st.form("upload_form"):
        uploaded_file = st.file_uploader(
            "🖼️ Seleccionar imagen",
            type=['png', 'jpg', 'jpeg'],
            help="Arrastra y suelta tu imagen aquí"
        )

        col1, col2 = st.columns(2)
        with col1:
            titulo = st.text_input("📝 Título de la imagen")
        with col2:
            tags = st.text_input("🏷️ Tags (separados por comas)")

        descripcion = st.text_area("✍️ Descripción")
        submitted = st.form_submit_button("📤 Subir Imagen", use_container_width=True)

    # Historial y categorías en sidebar
    with st.sidebar:
        st.markdown("""
        <div style='padding: 15px; background-color: #f0f8ff; border-radius: 10px;'>
            <h3 style='color: #3BA8A8;'>🕒 Búsquedas Recientes</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        - 🎨 Logo empresa
        - 🖼️ Banner promocional
        - 📦 Productos destacados
        """)

        st.markdown("""
        <div style='padding: 15px; background-color: #f0f8ff; border-radius: 10px; margin-top: 20px;'>
            <h3 style='color: #3BA8A8;'>🏷️ Categorías Populares</h3>
        </div>
        """, unsafe_allow_html=True)

        for cat in ["📦 Productos", "📢 Marketing", "🎨 Logos", "🖼️ Banners"]:
            st.button(cat, use_container_width=True)

if __name__ == "__main__":
    main()