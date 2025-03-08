import streamlit as st
import pandas as pd
from utils.data_manager import load_data
import numpy as np

st.set_page_config(page_title="Calculadora de Descuentos", page_icon="💰", layout="wide")

def calcular_descuentos(precio):
    """
    Calcula tres niveles de descuento para un precio dado
    """
    # Descuento mínimo (5%)
    descuento_minimo = precio * 0.05
    precio_minimo = precio - descuento_minimo
    
    # Descuento favorable (10%)
    descuento_favorable = precio * 0.10
    precio_favorable = precio - descuento_favorable
    
    # Descuento máximo (15%)
    descuento_maximo = precio * 0.15
    precio_maximo = precio - descuento_maximo
    
    return {
        'minimo': {'porcentaje': 5, 'descuento': descuento_minimo, 'precio_final': precio_minimo},
        'favorable': {'porcentaje': 10, 'descuento': descuento_favorable, 'precio_final': precio_favorable},
        'maximo': {'porcentaje': 15, 'descuento': descuento_maximo, 'precio_final': precio_maximo}
    }

def main():
    st.markdown("""
    <h1 style='text-align: center; color: #3BA8A8;'>
        💰 Calculadora de Descuentos ✨
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='padding: 15px; background-color: #f0f8ff; border-radius: 10px; margin-bottom: 20px;'>
        🎯 Calcula descuentos seguros para tus productos
        <br>💡 Obtén recomendaciones basadas en el análisis de inventario
        <br>📊 Visualiza el impacto en tus ganancias
    </div>
    """, unsafe_allow_html=True)

    # Entrada del precio
    precio = st.number_input(
        "💵 Precio del producto",
        min_value=1000.0,
        max_value=10000000.0,
        value=50000.0,
        step=1000.0,
        help="Ingresa el precio del producto para calcular los descuentos"
    )

    # Cálculo de descuentos
    if st.button("🧮 Calcular Descuentos", use_container_width=True):
        descuentos = calcular_descuentos(precio)
        
        # Mostrar resultados
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='padding: 20px; background-color: #e6ffe6; border-radius: 10px; text-align: center;'>
                <h3>🟢 Descuento Mínimo</h3>
                <h2>5%</h2>
                <hr>
                <p>Descuento: ${:,.0f}</p>
                <p>Precio Final: ${:,.0f}</p>
                <small>✅ Descuento seguro, ideal para productos de alta demanda</small>
            </div>
            """.format(
                descuentos['minimo']['descuento'],
                descuentos['minimo']['precio_final']
            ), unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style='padding: 20px; background-color: #fff2e6; border-radius: 10px; text-align: center;'>
                <h3>🟡 Descuento Favorable</h3>
                <h2>10%</h2>
                <hr>
                <p>Descuento: ${:,.0f}</p>
                <p>Precio Final: ${:,.0f}</p>
                <small>✅ Buen balance entre atractivo y rentabilidad</small>
            </div>
            """.format(
                descuentos['favorable']['descuento'],
                descuentos['favorable']['precio_final']
            ), unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div style='padding: 20px; background-color: #ffe6e6; border-radius: 10px; text-align: center;'>
                <h3>🔴 Descuento Máximo</h3>
                <h2>15%</h2>
                <hr>
                <p>Descuento: ${:,.0f}</p>
                <p>Precio Final: ${:,.0f}</p>
                <small>⚠️ Usar solo en casos especiales o liquidación</small>
            </div>
            """.format(
                descuentos['maximo']['descuento'],
                descuentos['maximo']['precio_final']
            ), unsafe_allow_html=True)

        # Recomendaciones basadas en el inventario
        st.markdown("### 📊 Análisis y Recomendaciones")
        
        try:
            df = load_data()
            if df is not None:
                productos_similares = df[
                    (df['precio'] >= precio * 0.8) & 
                    (df['precio'] <= precio * 1.2)
                ]
                
                if not productos_similares.empty:
                    st.info(f"""
                    📌 Productos similares en inventario: {len(productos_similares)}
                    
                    Recomendaciones basadas en el análisis:
                    - El precio promedio de productos similares es: ${productos_similares['precio'].mean():,.0f}
                    - Descuento recomendado: {descuentos['favorable']['porcentaje']}%
                    """)
                else:
                    st.info("No se encontraron productos similares en el inventario para comparar.")
        except Exception as e:
            st.warning("No se pudo acceder a los datos del inventario para recomendaciones.")

        # Consejos adicionales
        st.markdown("""
        ### 💡 Consejos para Aplicar Descuentos
        
        - **5% (Mínimo)**: Ideal para productos populares o de alta rotación
        - **10% (Favorable)**: Buena opción para promociones regulares
        - **15% (Máximo)**: Reservar para:
            - Liquidación de inventario
            - Productos con baja rotación
            - Eventos especiales
        """)

if __name__ == "__main__":
    main()
