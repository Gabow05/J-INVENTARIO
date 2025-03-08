import streamlit as st
import pandas as pd
from utils.data_manager import load_data
import numpy as np

st.set_page_config(page_title="Calculadora de Descuentos", page_icon="💰", layout="wide")

def calcular_precio_mayorista(precio_publico):
    """
    Calcula el precio mayorista basado en el precio al público
    Asume un 30% de utilidad y 5% de transporte
    """
    factor_mayorista = 1 - 0.35  # 35% total entre utilidad y transporte
    return precio_publico * factor_mayorista

def analizar_descuento(precio_publico, porcentaje_descuento):
    """
    Analiza si un descuento es seguro basado en el precio mayorista
    """
    precio_mayorista = calcular_precio_mayorista(precio_publico)
    precio_con_descuento = precio_publico * (1 - porcentaje_descuento/100)
    margen = ((precio_con_descuento - precio_mayorista) / precio_mayorista) * 100

    return {
        'precio_final': precio_con_descuento,
        'descuento_valor': precio_publico - precio_con_descuento,
        'margen_porcentaje': margen,
        'es_seguro': margen >= 10  # Consideramos seguro si mantiene al menos 10% de margen
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
        <br>💡 Basado en el precio mayorista (costo + transporte)
        <br>📊 Análisis de rentabilidad incluido
    </div>
    """, unsafe_allow_html=True)

    # Entrada del precio y descuento
    col1, col2 = st.columns(2)

    with col1:
        precio = st.number_input(
            "💵 Precio del producto",
            min_value=1000.0,
            max_value=10000000.0,
            value=50000.0,
            step=1000.0,
            help="Ingresa el precio al público del producto"
        )

    with col2:
        descuento = st.number_input(
            "📊 Porcentaje de descuento",
            min_value=0.0,
            max_value=15.0,
            value=5.0,
            step=0.5,
            help="Ingresa el porcentaje de descuento deseado (máximo 15%)"
        )

    # Cálculo y análisis
    if st.button("🧮 Analizar Descuento", use_container_width=True):
        precio_mayorista = calcular_precio_mayorista(precio)
        analisis = analizar_descuento(precio, descuento)

        # Mostrar resultados
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div style='padding: 20px; background-color: #f8f9fa; border-radius: 10px;'>
                <h3>💰 Análisis de Precios</h3>
                <hr>
            """, unsafe_allow_html=True)

            st.write(f"Precio público: ${precio:,.0f}")
            st.write(f"Precio mayorista: ${precio_mayorista:,.0f}")
            st.write(f"Precio con descuento: ${analisis['precio_final']:,.0f}")
            st.write(f"Valor del descuento: ${analisis['descuento_valor']:,.0f}")

        with col2:
            color = "green" if analisis['es_seguro'] else "red"
            icon = "✅" if analisis['es_seguro'] else "⚠️"

            st.markdown(f"""
            <div style='padding: 20px; background-color: #f8f9fa; border-radius: 10px;'>
                <h3>📊 Análisis de Rentabilidad</h3>
                <hr>
                <p>Margen de ganancia: <span style='color: {color};'>{analisis['margen_porcentaje']:.1f}%</span></p>
                <p>{icon} Este descuento es {'seguro' if analisis['es_seguro'] else 'riesgoso'}</p>
            </div>
            """, unsafe_allow_html=True)

        # Recomendaciones
        st.markdown("### 💡 Recomendaciones")

        if analisis['es_seguro']:
            st.success(f"""
            ✅ El descuento del {descuento}% es seguro para este producto:
            - Mantiene un margen de ganancia saludable del {analisis['margen_porcentaje']:.1f}%
            - El precio final (${analisis['precio_final']:,.0f}) está por encima del precio mayorista
            """)
        else:
            st.warning(f"""
            ⚠️ Este descuento podría ser riesgoso:
            - El margen de ganancia ({analisis['margen_porcentaje']:.1f}%) es bajo
            - Considera un descuento menor para mantener la rentabilidad
            - Descuento máximo recomendado: {((precio - precio_mayorista * 1.1) / precio * 100):.1f}%
            """)

        # Gráfico de análisis
        st.markdown("### 📊 Desglose de Precios")
        data = {
            'Componente': ['Precio Mayorista', 'Margen sin Descuento', 'Descuento'],
            'Valor': [
                precio_mayorista,
                precio - precio_mayorista - analisis['descuento_valor'],
                analisis['descuento_valor']
            ]
        }
        df = pd.DataFrame(data)
        st.bar_chart(df.set_index('Componente'))

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

        # Consejos adicionales (moved to after inventory analysis)
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