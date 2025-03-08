import streamlit as st
from forex_python.converter import CurrencyRates
from datetime import datetime

st.set_page_config(page_title="Calculadora de Monedas", page_icon="💱", layout="wide")

def main():
    st.markdown("""
    <h1 style='text-align: center; color: #3BA8A8;'>
        💱 Calculadora Mágica de Divisas ✨
    </h1>
    """, unsafe_allow_html=True)

    # Agregar descripción con estilo
    st.markdown("""
    <div style='padding: 15px; background-color: #f0f8ff; border-radius: 10px; margin-bottom: 20px;'>
        🌍 Convierte fácilmente entre diferentes monedas del mundo
        <br>🔄 Tasas de cambio en tiempo real
        <br>💡 Soporte para múltiples divisas
    </div>
    """, unsafe_allow_html=True)

    # Inicializar el convertidor
    c = CurrencyRates()

    # Lista de monedas con emojis
    monedas = {
        'USD': '🇺🇸 USD (Dólar)',
        'EUR': '🇪🇺 EUR (Euro)',
        'COP': '🇨🇴 COP (Peso)',
        'GBP': '🇬🇧 GBP (Libra)',
        'JPY': '🇯🇵 JPY (Yen)',
        'CHF': '🇨🇭 CHF (Franco)',
        'CAD': '🇨🇦 CAD (Dólar)',
        'AUD': '🇦🇺 AUD (Dólar)',
        'CNY': '🇨🇳 CNY (Yuan)'
    }

    # Interfaz de usuario mejorada
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💵 Moneda de Origen")
        cantidad = st.number_input("Cantidad 💰", min_value=0.0, value=1.0, step=0.1)
        moneda_origen = st.selectbox(
            "De:",
            options=list(monedas.keys()),
            format_func=lambda x: monedas[x],
            index=list(monedas.keys()).index('COP')
        )

    with col2:
        st.markdown("### 💴 Moneda de Destino")
        moneda_destino = st.selectbox(
            "A:",
            options=list(monedas.keys()),
            format_func=lambda x: monedas[x],
            index=list(monedas.keys()).index('USD')
        )

    # Botón de conversión con estilo
    if st.button("💫 Convertir", type="primary", use_container_width=True):
        try:
            resultado = c.convert(moneda_origen, moneda_destino, cantidad)

            # Mostrar resultado con estilo
            st.markdown(f"""
            <div style='padding: 20px; background-color: #e6ffe6; border-radius: 10px; text-align: center; font-size: 24px;'>
                {cantidad:,.2f} {moneda_origen} = 
                <span style='color: #00802b; font-weight: bold;'>
                    {resultado:,.2f} {moneda_destino}
                </span>
            </div>
            """, unsafe_allow_html=True)

            # Mostrar tasa de cambio
            tasa = c.get_rate(moneda_origen, moneda_destino)
            st.info(f"📊 Tasa de cambio: 1 {moneda_origen} = {tasa:,.4f} {moneda_destino}")

        except Exception as e:
            st.error("❌ Error al realizar la conversión. Por favor, intente nuevamente.")

    # Información adicional con estilo
    st.markdown("---")
    st.markdown("""
    <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;'>
        <div style='text-align: center; padding: 15px; background-color: #f0f0f0; border-radius: 10px;'>
            🔄 Actualización en tiempo real
        </div>
        <div style='text-align: center; padding: 15px; background-color: #f0f0f0; border-radius: 10px;'>
            🏦 Datos del Banco Central Europeo
        </div>
        <div style='text-align: center; padding: 15px; background-color: #f0f0f0; border-radius: 10px;'>
            📈 Tasas precisas y confiables
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()