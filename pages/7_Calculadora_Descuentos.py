
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

def determinar_categoria_producto(precio):
    """
    Determina la categoría del producto basado en su precio
    """
    if precio < 20000:
        return "pequeño", (1, 7)
    elif precio < 100000:
        return "mediano", (7, 12)
    else:
        return "grande", (10, 15)

def analizar_descuento(precio_publico, porcentaje_descuento):
    """
    Analiza si un descuento es seguro basado en el precio mayorista
    """
    precio_mayorista = calcular_precio_mayorista(precio_publico)
    precio_con_descuento = precio_publico * (1 - porcentaje_descuento/100)
    margen = ((precio_con_descuento - precio_mayorista) / precio_mayorista) * 100

    categoria, rango_descuento = determinar_categoria_producto(precio_publico)
    
    return {
        'precio_final': precio_con_descuento,
        'descuento_valor': precio_publico - precio_con_descuento,
        'margen_porcentaje': margen,
        'es_seguro': margen >= 10,  # Consideramos seguro si mantiene al menos 10% de margen
        'categoria': categoria,
        'rango_descuento': rango_descuento
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

    # Determinar la categoría del producto y su rango de descuento recomendado
    categoria, rango_descuento = determinar_categoria_producto(precio)
    
    with col2:
        descuento = st.number_input(
            f"📊 Porcentaje de descuento (Recomendado: {rango_descuento[0]}-{rango_descuento[1]}%)",
            min_value=0.0,
            max_value=15.0,
            value=float(rango_descuento[0]),
            step=0.5,
            help=f"Para productos {categoria}s (${precio:,.0f}), se recomienda un descuento entre {rango_descuento[0]}-{rango_descuento[1]}%"
        )

    # Mostrar indicador de categoría
    cat_colors = {
        "pequeño": "#7FD8BE",  # Verde claro
        "mediano": "#FFC857",  # Amarillo
        "grande": "#E9724C"    # Naranja
    }
    
    st.markdown(f"""
    <div style='margin-bottom: 20px; padding: 10px; background-color: {cat_colors[categoria]}; 
         border-radius: 5px; text-align: center;'>
        <strong>Categoría de producto:</strong> {categoria.upper()} 
        (Rango de descuento recomendado: {rango_descuento[0]}-{rango_descuento[1]}%)
    </div>
    """, unsafe_allow_html=True)

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

            # Evaluar si el descuento está dentro del rango recomendado
            dentro_rango = rango_descuento[0] <= descuento <= rango_descuento[1]
            rango_icon = "✅" if dentro_rango else "⚠️"
            rango_color = "green" if dentro_rango else "orange"

            st.markdown(f"""
            <div style='padding: 20px; background-color: #f8f9fa; border-radius: 10px;'>
                <h3>📊 Análisis de Rentabilidad</h3>
                <hr>
                <p>Margen de ganancia: <span style='color: {color};'>{analisis['margen_porcentaje']:.1f}%</span></p>
                <p>{icon} Este descuento es {'seguro' if analisis['es_seguro'] else 'riesgoso'} para el margen</p>
                <p>{rango_icon} <span style='color: {rango_color};'>{'Dentro' if dentro_rango else 'Fuera'} del rango recomendado</span> para productos {categoria}s</p>
            </div>
            """, unsafe_allow_html=True)

        # Recomendaciones
        st.markdown("### 💡 Recomendaciones")

        if analisis['es_seguro'] and dentro_rango:
            st.success(f"""
            ✅ El descuento del {descuento}% es óptimo para este producto {categoria}:
            - Mantiene un margen de ganancia saludable del {analisis['margen_porcentaje']:.1f}%
            - Está dentro del rango recomendado ({rango_descuento[0]}-{rango_descuento[1]}%)
            - El precio final (${analisis['precio_final']:,.0f}) está por encima del precio mayorista
            """)
        elif analisis['es_seguro'] and not dentro_rango:
            st.warning(f"""
            ⚠️ El descuento es seguro pero no es el óptimo para un producto {categoria}:
            - El margen de ganancia ({analisis['margen_porcentaje']:.1f}%) es saludable
            - Sin embargo, está fuera del rango recomendado ({rango_descuento[0]}-{rango_descuento[1]}%)
            - Considera ajustar el descuento al rango sugerido para esta categoría
            """)
        else:
            st.error(f"""
            ⚠️ Este descuento es riesgoso:
            - El margen de ganancia ({analisis['margen_porcentaje']:.1f}%) es demasiado bajo
            - Considera un descuento menor para mantener la rentabilidad
            - Para productos {categoria}s, mantente en el rango {rango_descuento[0]}-{rango_descuento[1]}%
            - Descuento máximo seguro recomendado: {((precio - precio_mayorista * 1.1) / precio * 100):.1f}%
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
        st.markdown("### 📊 Productos Similares en Inventario")
        
        try:
            inv_df = load_data()
            if inv_df is not None:
                # Asegurarse de que las columnas necesarias existen
                if all(col in inv_df.columns for col in ['producto', 'precio', 'cantidad']):
                    productos_similares = inv_df[
                        (inv_df['precio'] >= precio * 0.8) & 
                        (inv_df['precio'] <= precio * 1.2)
                    ]
                    
                    if not productos_similares.empty:
                        st.info(f"""
                        📌 Productos similares en inventario: {len(productos_similares)}
                        
                        Información de productos similares:
                        - Precio promedio: ${productos_similares['precio'].mean():,.0f}
                        - Cantidad total disponible: {productos_similares['cantidad'].sum()} unidades
                        """)
                        
                        # Mostrar productos similares
                        st.dataframe(
                            productos_similares[['producto', 'referencia', 'codigo', 'cantidad', 'precio']].head(5),
                            use_container_width=True,
                            hide_index=True
                        )
                    else:
                        st.info("No se encontraron productos similares en el inventario para comparar.")
                else:
                    st.info("El formato del inventario no permite realizar comparaciones de productos similares.")
        except Exception as e:
            st.warning(f"No se pudo acceder a los datos del inventario: {str(e)}")

        # Consejos adicionales según la categoría
        st.markdown(f"""
        ### 💡 Consejos para Productos {categoria.capitalize()}s
        """)
        
        if categoria == "pequeño":
            st.markdown("""
            - **1-3% (Descuento Mínimo)**: Ideal para productos de uso diario o esenciales
            - **4-5% (Descuento Estándar)**: Para promociones regulares o compras por cantidad
            - **6-7% (Descuento Máximo)**: Reservar para:
                - Liquidación de productos de baja rotación
                - Eventos especiales o fin de temporada
            """)
        elif categoria == "mediano":
            st.markdown("""
            - **7-8% (Descuento Mínimo)**: Para atraer atención a productos específicos
            - **9-10% (Descuento Estándar)**: Buena opción para promociones destacadas
            - **11-12% (Descuento Máximo)**: Reservar para:
                - Estrategias de venta cruzada (compre uno, descuento en el segundo)
                - Reducir inventario de productos con menor rotación
            """)
        else:  # grande
            st.markdown("""
            - **10-11% (Descuento Mínimo)**: Para destacar productos premium
            - **12-13% (Descuento Estándar)**: Promociones atractivas en productos de alto valor
            - **14-15% (Descuento Máximo)**: Estrategias especiales:
                - Productos antiguos en inventario que necesitan rotación
                - Eventos exclusivos o ventas flash
                - Clientes VIP o compras de gran volumen
            """)

if __name__ == "__main__":
    main()
