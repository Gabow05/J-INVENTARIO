import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title="Gestor de Redes Sociales", page_icon="📱", layout="wide")

def main():
    st.title("📱 Gestor de Redes Sociales")
    
    # Sidebar para selección de red social
    st.sidebar.header("Configuración")
    red_social = st.sidebar.selectbox(
        "Seleccionar Red Social",
        ["Facebook", "Instagram", "Twitter"]
    )

    # Pestañas principales
    tab1, tab2, tab3 = st.tabs(["📅 Calendario", "📊 Estadísticas", "⚙️ Configuración"])

    with tab1:
        st.header("Calendario de Publicaciones")
        
        # Formulario para nueva publicación
        with st.form("nueva_publicacion"):
            st.subheader("Nueva Publicación")
            fecha = st.date_input("Fecha de publicación")
            hora = st.time_input("Hora de publicación")
            contenido = st.text_area("Contenido")
            imagen = st.file_uploader("Subir imagen", type=['png', 'jpg', 'jpeg'])
            
            col1, col2 = st.columns(2)
            with col1:
                programar = st.form_submit_button("Programar")
            with col2:
                vista_previa = st.form_submit_button("Vista Previa")

        # Calendario de publicaciones (ejemplo)
        st.subheader("Publicaciones Programadas")
        ejemplo_data = {
            'Fecha': ['2025-03-10', '2025-03-11', '2025-03-12'],
            'Hora': ['10:00', '15:30', '18:00'],
            'Contenido': ['Post 1', 'Post 2', 'Post 3'],
            'Estado': ['Programado', 'Publicado', 'Programado']
        }
        df = pd.DataFrame(ejemplo_data)
        st.dataframe(df, use_container_width=True)

    with tab2:
        st.header("Estadísticas")
        
        # Métricas de ejemplo
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Seguidores", "1,234", "+123")
        with col2:
            st.metric("Interacciones", "456", "+45")
        with col3:
            st.metric("Alcance", "10,234", "+1,023")

        # Gráfico de ejemplo
        datos_ejemplo = {
            'fecha': pd.date_range(start='2025-03-01', end='2025-03-08'),
            'interacciones': [100, 150, 130, 200, 180, 220, 190, 250]
        }
        df_stats = pd.DataFrame(datos_ejemplo)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_stats['fecha'],
            y=df_stats['interacciones'],
            mode='lines+markers',
            name='Interacciones'
        ))
        fig.update_layout(
            title='Interacciones Diarias',
            xaxis_title='Fecha',
            yaxis_title='Interacciones'
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("Configuración de Cuentas")
        
        # Formulario de configuración
        with st.form("config_redes"):
            st.subheader(f"Configuración de {red_social}")
            usuario = st.text_input("Usuario")
            token = st.text_input("Token de API", type="password")
            guardar = st.form_submit_button("Guardar Configuración")

        # Ajustes adicionales
        st.subheader("Ajustes de Publicación")
        st.checkbox("Publicación automática")
        st.checkbox("Notificaciones por email")
        st.select_slider(
            "Frecuencia máxima de publicación",
            options=['1/día', '2/día', '3/día', '4/día', '5/día']
        )

if __name__ == "__main__":
    main()
