import streamlit as st
import pandas as pd
import math
from utils.data_manager import load_data

st.set_page_config(page_title="Calculadora de Descuentos", page_icon="🧮", layout="wide")

def calcular_categorizacion(precio):
    """Categoriza el producto según su precio"""
    if precio < 50000:
        return "pequeño", (5, 10)
    elif precio < 200000:
        return "mediano", (10, 15)
    else:
        return "grande", (15, 20)

def analizar_descuento(precio, porcentaje_descuento):
    """Analiza si un descuento es seguro para el negocio"""
    precio_final = precio * (1 - porcentaje_descuento/100)
    descuento_valor = precio - precio_final

    # Análisis de seguridad del descuento
    categoria, rango = calcular_categorizacion(precio)
    es_seguro = porcentaje_descuento <= rango[1]

    return {
        "precio_final": precio_final,
        "descuento_valor": descuento_valor,
        "es_seguro": es_seguro,
        "razon": f"El descuento está {'dentro' if es_seguro else 'fuera'} del rango recomendado ({rango[0]}-{rango[1]}%)"
    }

def main():
    st.title("🧮 Calculadora de Descuentos")

    st.markdown("""
    Esta herramienta le ayuda a calcular y analizar descuentos para sus productos, 
    ofreciendo recomendaciones para mantener márgenes saludables.
    """)

    # Inventario para selección de productos
    inventario_df = load_data()
    product_from_inventory = False
    precio = 0.0

    # Opción para seleccionar un producto del inventario
    if inventario_df is not None and not inventario_df.empty:
        product_from_inventory = st.checkbox("Seleccionar producto del inventario")

        if product_from_inventory:
            # Búsqueda de productos
            search = st.text_input("🔍 Buscar producto", "")
            filtered_df = inventario_df

            if search:
                filtered_df = inventario_df[
                    inventario_df['producto'].str.contains(search, case=False, na=False) |
                    inventario_df['codigo'].str.contains(search, case=False, na=False) |
                    inventario_df['referencia'].str.contains(search, case=False, na=False)
                ]

            if not filtered_df.empty:
                options = filtered_df['producto'].tolist()
                selected_product = st.selectbox("Seleccione un producto", options)

                selected_row = filtered_df[filtered_df['producto'] == selected_product].iloc[0]
                precio = float(selected_row['precio'])

                st.info(f"""
                **Producto seleccionado:** {selected_product}
                **Referencia:** {selected_row['referencia']}
                **Código:** {selected_row['codigo']}
                **Precio:** ${precio:,.0f}
                **Cantidad disponible:** {selected_row['cantidad']}
                """)
            else:
                st.warning("No se encontraron productos que coincidan con la búsqueda.")

    # Si no se selecciona del inventario, permitir ingreso manual
    if not product_from_inventory:
        precio = st.number_input("💰 Precio del producto", min_value=0.0, value=100000.0, step=1000.0)

    # Definir categoría y rango de descuento recomendado
    categoria, rango_descuento = calcular_categorizacion(precio)

    # Slider para descuento
    descuento = st.slider(
        "📉 Porcentaje de descuento", 
        min_value=0, 
        max_value=50, 
        value=rango_descuento[0],
        help=f"Rango recomendado: {rango_descuento[0]}-{rango_descuento[1]}%"
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
        analisis = analizar_descuento(precio, descuento)

        # Mostrar resultados
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div style='padding: 20px; background-color: #f8f9fa; border-radius: 10px;'>
                <h3>💰 Análisis de Precios</h3>
                <hr>
            """, unsafe_allow_html=True)

            st.write(f"Precio público: ${precio:,.0f}")
            st.write(f"Precio con descuento: ${analisis['precio_final']:,.0f}")
            st.write(f"Valor del descuento: ${analisis['descuento_valor']:,.0f}")
            st.markdown(f"<h4 style='color: #1E88E5; text-align: center; margin-top: 15px;'>Descuento aplicado: <b>{descuento}%</b></h4>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            color = "green" if analisis['es_seguro'] else "red"
            icon = "✅" if analisis['es_seguro'] else "⚠️"

            st.markdown(f"""
            <div style='padding: 20px; background-color: #f8f9fa; border-radius: 10px;'>
                <h3>🔍 Evaluación del Descuento</h3>
                <hr>
                <p style='color: {color}; font-weight: bold;'>
                    {icon} {analisis['razon']}
                </p>
            """, unsafe_allow_html=True)

            # Mostrar margen estimado
            margen_estimado = (analisis['precio_final'] / precio - 0.6) * 100  # Asumiendo costo = 60% del precio

            if margen_estimado > 15:
                margen_color = "green"
                margen_icon = "✅"
            elif margen_estimado > 10:
                margen_color = "orange"
                margen_icon = "⚠️"
            else:
                margen_color = "red"
                margen_icon = "❌"

            st.markdown(f"""
                <p>Margen estimado: <span style='color: {margen_color}; font-weight: bold;'>{margen_icon} {margen_estimado:.1f}%</span></p>
                </div>
            """, unsafe_allow_html=True)

        # Comparación visual
        st.markdown("### 📊 Comparación de Precios")

        data = {
            'Componente': ['Precio original', 'Descuento', 'Precio final'],
            'Valor': [precio, analisis['descuento_valor'], analisis['precio_final']]
        }

        df = pd.DataFrame(data)
        st.bar_chart(df.set_index('Componente'))

        # Lista de descuentos favorables por producto del inventario
        st.markdown("### 📋 Descuentos Recomendados por Producto")

        try:
            inv_df = load_data()
            if inv_df is not None and not inv_df.empty:
                # Calcular los rangos de descuento para cada producto
                descuentos_df = pd.DataFrame()
                descuentos_df['producto'] = inv_df['producto']
                descuentos_df['referencia'] = inv_df['referencia']
                descuentos_df['codigo'] = inv_df['codigo']
                descuentos_df['precio'] = inv_df['precio']

                # Calcular categoría y rangos
                descuentos_df['categoria'] = descuentos_df['precio'].apply(
                    lambda x: calcular_categorizacion(x)[0]
                )
                descuentos_df['min_descuento'] = descuentos_df['precio'].apply(
                    lambda x: calcular_categorizacion(x)[1][0]
                )
                descuentos_df['max_descuento'] = descuentos_df['precio'].apply(
                    lambda x: calcular_categorizacion(x)[1][1]
                )

                # Mostrar tabla de descuentos
                st.dataframe(
                    descuentos_df[['producto', 'referencia', 'codigo', 'precio', 'min_descuento', 'max_descuento']],
                    column_config={
                        'producto': 'Producto',
                        'referencia': 'Referencia',
                        'codigo': 'Código',
                        'precio': st.column_config.NumberColumn('Precio ($)', format="$%d"),
                        'min_descuento': st.column_config.NumberColumn('Descuento Mínimo (%)', format="%d%%"),
                        'max_descuento': st.column_config.NumberColumn('Descuento Máximo (%)', format="%d%%")
                    },
                    use_container_width=True,
                    hide_index=True
                )

                # Agregar filtro de búsqueda para esta tabla
                search_product = st.text_input("🔍 Buscar producto para ver descuentos recomendados")
                if search_product:
                    filtered_discounts = descuentos_df[
                        descuentos_df['producto'].str.contains(search_product, case=False, na=False) |
                        descuentos_df['codigo'].str.contains(search_product, case=False, na=False) |
                        descuentos_df['referencia'].str.contains(search_product, case=False, na=False)
                    ]

                    if not filtered_discounts.empty:
                        st.dataframe(
                            filtered_discounts[['producto', 'referencia', 'codigo', 'precio', 'min_descuento', 'max_descuento']],
                            column_config={
                                'producto': 'Producto',
                                'referencia': 'Referencia',
                                'codigo': 'Código',
                                'precio': st.column_config.NumberColumn('Precio ($)', format="$%d"),
                                'min_descuento': st.column_config.NumberColumn('Descuento Mínimo (%)', format="%d%%"),
                                'max_descuento': st.column_config.NumberColumn('Descuento Máximo (%)', format="%d%%")
                            },
                            use_container_width=True,
                            hide_index=True
                        )
                    else:
                        st.info("No se encontraron productos que coincidan con la búsqueda.")
            else:
                st.info("No hay datos de inventario disponibles para mostrar descuentos recomendados.")
        except Exception as e:
            st.error(f"Error al calcular descuentos recomendados: {str(e)}")

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
            st.error(f"Error al buscar productos similares: {str(e)}")

if __name__ == "__main__":
    main()