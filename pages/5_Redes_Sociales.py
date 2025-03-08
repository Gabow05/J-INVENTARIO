import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title="Centro de Mensajes", page_icon="💬", layout="wide")

def main():
    st.markdown("""
    <h1 style='text-align: center; color: #3BA8A8;'>
        💬 Centro de Mensajes Unificado ✨
    </h1>
    """, unsafe_allow_html=True)

    # Panel de control
    st.sidebar.markdown("""
    <div style='padding: 15px; background-color: #f0f8ff; border-radius: 10px;'>
        <h3 style='color: #3BA8A8;'>🎯 Redes Conectadas</h3>
    </div>
    """, unsafe_allow_html=True)

    # Estado de conexión de redes sociales
    redes = {
        "Facebook": {"conectado": False, "icono": "📘"},
        "Instagram": {"conectado": False, "icono": "📸"},
        "Twitter": {"conectado": False, "icono": "🐦"}
    }

    # Botones de conexión para cada red social
    for red, info in redes.items():
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            if info["conectado"]:
                st.success(f"{info['icono']} {red} conectado")
            else:
                if st.button(f"Conectar {info['icono']} {red}", use_container_width=True):
                    st.info(f"Conectando con {red}...")
                    # Aquí iría la lógica de autenticación OAuth

    # Pestañas principales
    tab1, tab2 = st.tabs([
        "💬 Bandeja de Mensajes",
        "📊 Estadísticas"
    ])

    with tab1:
        # Filtros de mensajes
        col1, col2, col3 = st.columns(3)
        with col1:
            red_seleccionada = st.selectbox(
                "🌐 Filtrar por red social",
                ["Todas", "📘 Facebook", "📸 Instagram", "🐦 Twitter"]
            )
        with col2:
            estado = st.selectbox(
                "📫 Estado",
                ["Todos", "No leídos", "Respondidos", "Pendientes"]
            )
        with col3:
            busqueda = st.text_input("🔍 Buscar en mensajes")

        # Área de mensajes
        st.markdown("### 📥 Mensajes Recientes")

        # Ejemplo de mensajes
        mensajes = [
            {
                "red": "📘 Facebook",
                "usuario": "Juan Pérez",
                "mensaje": "¿Tienen disponible el producto X?",
                "fecha": "2025-03-08 10:30",
                "estado": "No leído"
            },
            {
                "red": "📸 Instagram",
                "usuario": "María García",
                "mensaje": "¿Cuál es el horario de atención?",
                "fecha": "2025-03-08 09:15",
                "estado": "Respondido"
            }
        ]

        for mensaje in mensajes:
            with st.container():
                st.markdown(f"""
                <div style='padding: 15px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 10px;'>
                    <h4>{mensaje['red']} - {mensaje['usuario']}</h4>
                    <p>{mensaje['mensaje']}</p>
                    <small>⏰ {mensaje['fecha']} | 📌 {mensaje['estado']}</small>
                </div>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns([2,2,1])
                with col1:
                    st.text_input("💭 Responder", key=f"resp_{mensaje['usuario']}")
                with col2:
                    st.button("📤 Enviar", key=f"send_{mensaje['usuario']}")
                with col3:
                    st.button("⭐ Marcar como importante", key=f"star_{mensaje['usuario']}")

    with tab2:
        st.markdown("### 📊 Resumen de Actividad")

        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Mensajes Nuevos", "15", "+3")
        with col2:
            st.metric("Tiempo Respuesta", "8 min", "-2 min")
        with col3:
            st.metric("Satisfacción", "95%", "+2%")

        # Gráfico de actividad
        fechas = pd.date_range(start='2025-03-01', end='2025-03-08')
        datos = pd.DataFrame({
            'fecha': fechas,
            'mensajes': [12, 15, 10, 18, 20, 15, 17, 15]
        })

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=datos['fecha'],
            y=datos['mensajes'],
            mode='lines+markers',
            name='Mensajes',
            line=dict(color='#3BA8A8', width=3),
            marker=dict(size=8)
        ))
        fig.update_layout(
            title='📈 Volumen de Mensajes',
            xaxis_title='Fecha',
            yaxis_title='Cantidad de Mensajes'
        )
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()