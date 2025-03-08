import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title="Gestor de Redes Sociales", page_icon="📱", layout="wide")

def main():
    st.markdown("""
    <h1 style='text-align: center; color: #3BA8A8;'>
        📱 Centro de Control de Redes Sociales ✨
    </h1>
    """, unsafe_allow_html=True)

    # Sidebar mejorado
    st.sidebar.markdown("""
    <div style='padding: 15px; background-color: #f0f8ff; border-radius: 10px;'>
        <h3 style='color: #3BA8A8;'>🎯 Panel de Control</h3>
    </div>
    """, unsafe_allow_html=True)

    red_social = st.sidebar.selectbox(
        "🌐 Seleccionar Red Social",
        ["📘 Facebook", "📸 Instagram", "🐦 Twitter"]
    )

    # Pestañas principales con estilo
    tab1, tab2, tab3 = st.tabs([
        "📅 Calendario de Publicaciones",
        "📊 Estadísticas y Métricas",
        "⚙️ Configuración"
    ])

    with tab1:
        st.markdown("""
        <h3 style='color: #3BA8A8;'>📅 Planificador de Contenido</h3>
        """, unsafe_allow_html=True)

        # Formulario para nueva publicación
        with st.form("nueva_publicacion", clear_on_submit=True):
            st.markdown("### ✍️ Nueva Publicación")
            fecha = st.date_input("📆 Fecha de publicación")
            hora = st.time_input("⏰ Hora de publicación")
            contenido = st.text_area("💭 Contenido", placeholder="Escribe tu mensaje aquí...")
            imagen = st.file_uploader("🖼️ Subir imagen", type=['png', 'jpg', 'jpeg'])

            cols = st.columns(2)
            with cols[0]:
                programar = st.form_submit_button("📅 Programar", use_container_width=True)
            with cols[1]:
                vista_previa = st.form_submit_button("👁️ Vista Previa", use_container_width=True)

        # Calendario de publicaciones con estilo
        st.markdown("""
        <h4 style='color: #3BA8A8;'>📋 Publicaciones Programadas</h4>
        """, unsafe_allow_html=True)

        ejemplo_data = pd.DataFrame({
            'Fecha': ['2025-03-10', '2025-03-11', '2025-03-12'],
            'Hora': ['10:00', '15:30', '18:00'],
            'Contenido': ['¡Nuevo producto!', 'Oferta especial', 'Evento próximo'],
            'Estado': ['🟢 Programado', '✅ Publicado', '🟡 Pendiente']
        })

        st.dataframe(
            ejemplo_data,
            use_container_width=True,
            column_config={
                "Fecha": st.column_config.DateColumn("📅 Fecha"),
                "Hora": st.column_config.TextColumn("⏰ Hora"),
                "Contenido": st.column_config.TextColumn("💭 Contenido"),
                "Estado": st.column_config.TextColumn("📌 Estado")
            }
        )

    with tab2:
        st.markdown("""
        <h3 style='color: #3BA8A8;'>📊 Panel de Métricas</h3>
        """, unsafe_allow_html=True)

        # Métricas con estilo
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div style='padding: 20px; background-color: #e6f3ff; border-radius: 10px; text-align: center;'>
                <h2>👥 1,234</h2>
                <p>Seguidores</p>
                <small style='color: green;'>↑ +123 esta semana</small>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style='padding: 20px; background-color: #fff2e6; border-radius: 10px; text-align: center;'>
                <h2>❤️ 456</h2>
                <p>Interacciones</p>
                <small style='color: green;'>↑ +45 esta semana</small>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style='padding: 20px; background-color: #e6ffe6; border-radius: 10px; text-align: center;'>
                <h2>👁️ 10,234</h2>
                <p>Alcance</p>
                <small style='color: green;'>↑ +1,023 esta semana</small>
            </div>
            """, unsafe_allow_html=True)

        # Gráfico interactivo mejorado
        datos_ejemplo = pd.DataFrame({
            'fecha': pd.date_range(start='2025-03-01', end='2025-03-08'),
            'interacciones': [100, 150, 130, 200, 180, 220, 190, 250]
        })

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=datos_ejemplo['fecha'],
            y=datos_ejemplo['interacciones'],
            mode='lines+markers',
            name='Interacciones',
            line=dict(color='#3BA8A8', width=3),
            marker=dict(size=8)
        ))
        fig.update_layout(
            title='📈 Evolución de Interacciones',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title='📅 Fecha',
            yaxis_title='👍 Interacciones'
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("""
        <h3 style='color: #3BA8A8;'>⚙️ Ajustes de Cuenta</h3>
        """, unsafe_allow_html=True)

        # Formulario de configuración mejorado
        with st.form("config_redes"):
            st.subheader(f"🔧 Configuración de {red_social}")
            usuario = st.text_input("👤 Usuario")
            token = st.text_input("🔑 Token de API", type="password")
            guardar = st.form_submit_button("💾 Guardar Configuración", use_container_width=True)

        # Ajustes adicionales con estilo
        st.markdown("""
        <h4 style='color: #3BA8A8;'>🎛️ Preferencias de Publicación</h4>
        """, unsafe_allow_html=True)

        st.checkbox("🤖 Publicación automática")
        st.checkbox("📧 Notificaciones por email")
        st.select_slider(
            "📊 Frecuencia máxima de publicación",
            options=['1/día', '2/día', '3/día', '4/día', '5/día'],
            value='3/día'
        )

if __name__ == "__main__":
    main()