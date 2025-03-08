import streamlit as st
from forex_python.converter import CurrencyRates
from datetime import datetime

st.set_page_config(page_title="Calculadora de Monedas", page_icon="💱")

def main():
    st.title("💱 Calculadora de Monedas")
    
    # Inicializar el convertidor
    c = CurrencyRates()
    
    # Lista de monedas comunes
    monedas = ['USD', 'EUR', 'COP', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD', 'CNY']
    
    # Interfaz de usuario
    col1, col2 = st.columns(2)
    
    with col1:
        cantidad = st.number_input("Cantidad", min_value=0.0, value=1.0)
        moneda_origen = st.selectbox("Moneda de origen", monedas, index=monedas.index('COP'))
    
    with col2:
        moneda_destino = st.selectbox("Moneda de destino", monedas, index=monedas.index('USD'))
        
    # Botón de conversión
    if st.button("Convertir", type="primary"):
        try:
            resultado = c.convert(moneda_origen, moneda_destino, cantidad)
            
            # Mostrar resultado
            st.success(f"{cantidad:,.2f} {moneda_origen} = {resultado:,.2f} {moneda_destino}")
            
            # Mostrar tasa de cambio
            tasa = c.get_rate(moneda_origen, moneda_destino)
            st.info(f"Tasa de cambio: 1 {moneda_origen} = {tasa:,.4f} {moneda_destino}")
            
        except Exception as e:
            st.error("Error al realizar la conversión. Por favor, intente nuevamente.")
    
    # Información adicional
    st.markdown("---")
    st.markdown("""
    ### Información
    - Las tasas de cambio se actualizan en tiempo real
    - Fuente: European Central Bank
    """)

if __name__ == "__main__":
    main()
