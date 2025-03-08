import streamlit as st
import pandas as pd
from utils.data_manager import load_data
import time

st.set_page_config(page_title="Inventario", page_icon="📦", layout="wide")

def main():
    st.title("📦 Gestión de Inventario")

    # Load data
    df = load_data()
    try:
        if df is None or df.empty:
            st.info("📝 No hay datos de inventario disponibles. Por favor, importe datos en la sección de Configuración.")
            return
    except Exception as e:
        st.error("Error al cargar datos. Por favor, intente nuevamente.")
        return

    # Búsqueda y filtros
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        search = st.text_input("🔍 Buscar por nombre o código", "")
    with col2:
        precio_min = st.number_input("💰 Precio mínimo", 0.0, value=0.0, step=1000.0)
    with col3:
        precio_max = st.number_input("💰 Precio máximo", 0.0, value=float(df['precio'].max()), step=1000.0)

    hide_zero = st.checkbox("🚫 Ocultar productos agotados", value=False)

    # Optimizar filtros
    @st.cache_data(ttl=300)
    def filter_dataframe(df, search, precio_min, precio_max, hide_zero):
        # Usar método más eficiente para filtrar
        filtered_df = df.copy()
        
        if hide_zero:
            filtered_df = filtered_df[filtered_df['cantidad'] > 0]
            
        if search:
            # Convertir a minúsculas para búsqueda más rápida
            search = search.lower()
            mask = (
                filtered_df['producto'].str.lower().str.contains(search, na=False) |
                filtered_df['codigo'].str.lower().str.contains(search, na=False) |
                filtered_df['referencia'].str.lower().str.contains(search, na=False)
            )
            filtered_df = filtered_df[mask]
            
        # Aplicar filtros de precio
        filtered_df = filtered_df[
            (filtered_df['precio'] >= precio_min) & 
            (filtered_df['precio'] <= precio_max)
        ]
        
        return filtered_df
    
    # Aplicar filtros con caché
    filtered_df = filter_dataframe(df, search, precio_min, precio_max, hide_zero)

    # Mostrar métricas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📦 Total Productos", len(filtered_df))
    with col2:
        valor_total = (filtered_df['precio'] * filtered_df['cantidad']).sum()
        st.metric("💵 Valor Total", f"${valor_total:,.2f}")
    with col3:
        agotados = len(filtered_df[filtered_df['cantidad'] == 0])
        st.metric("⚠️ Productos Agotados", agotados)
    with col4:
        st.metric("💰 Precio Promedio", f"${filtered_df['precio'].mean():,.2f}")

    # Mostrar tabla de inventario
    # Usar una función más eficiente para el estilo
    @st.cache_data(ttl=300)
    def get_styled_df(df):
        def highlight_agotados(row):
            if row['cantidad'] <= 0:
                return ['background-color: #ffebee; color: #c62828'] * len(row)
            elif row['cantidad'] < 5:
                return ['background-color: #fff3e0; color: #ef6c00'] * len(row)
            return [''] * len(row)
        
        # Limitar a las columnas principales para mejorar rendimiento
        display_df = df[['producto', 'referencia', 'codigo', 'cantidad', 'precio']]
        return display_df.style.apply(highlight_agotados, axis=1)
    
    # Mostrar solo las primeras 1000 filas con paginación para mejor rendimiento
    if len(filtered_df) > 1000:
        st.warning(f"Mostrando las primeras 1000 filas de {len(filtered_df)} productos filtrados.")
        display_df = filtered_df.head(1000)
    else:
        display_df = filtered_df
    
    st.dataframe(
        get_styled_df(display_df),
        use_container_width=True,
        hide_index=True,
        column_config={
            "producto": st.column_config.TextColumn(
                "Producto",
                width="large",
            ),
            "referencia": st.column_config.TextColumn(
                "Referencia",
                width="medium",
            ),
            "codigo": st.column_config.TextColumn(
                "Código",
                width="medium",
            ),
            "cantidad": st.column_config.NumberColumn(
                "Cantidad",
                help="🔴 Rojo: Agotado | 🟠 Naranja: Stock bajo",
                format="%d",
            ),
            "precio": st.column_config.NumberColumn(
                "Precio",
                format="$%,.0f",
            ),
        }
    )

    # Estadísticas adicionales
    st.markdown("### 📊 Resumen de Inventario")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💎 Top 5 Productos más caros")
        top_expensive = filtered_df.nlargest(5, 'precio')[['producto', 'precio']]
        st.dataframe(top_expensive, hide_index=True)

    with col2:
        st.markdown("#### ⚠️ Productos con stock bajo (menos de 5 unidades)")
        low_stock = filtered_df[filtered_df['cantidad'] < 5][['producto', 'cantidad']]
        st.dataframe(low_stock, hide_index=True)

if __name__ == "__main__":
    main()