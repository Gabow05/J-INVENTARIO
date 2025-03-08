import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Calculadora de Monedas", page_icon="💱", layout="wide")

# Tasas de cambio fijas (actualizadas al 8 de marzo 2025)
TASAS = {
    'USD': {
        'EUR': 0.91,
        'GBP': 0.78,
        'JPY': 147.50,
        'CHF': 0.88,
        'CAD': 1.35,
        'AUD': 1.52,
        'CNY': 7.19
    }
}

def calcular_tasa(moneda_origen, moneda_destino, tasa_cop_usd):
    """Calcula la tasa de cambio entre dos monedas"""
    if moneda_origen == moneda_destino:
        return 1.0

    # Manejar conversiones con COP
    if moneda_origen == 'COP' and moneda_destino == 'USD':
        return 1 / tasa_cop_usd
    if moneda_origen == 'USD' and moneda_destino == 'COP':
        return tasa_cop_usd
    if moneda_origen == 'COP':
        return (1 / tasa_cop_usd) * TASAS['USD'][moneda_destino]
    if moneda_destino == 'COP':
        if moneda_origen in TASAS['USD']:
            return tasa_cop_usd / TASAS['USD'][moneda_origen]
        return tasa_cop_usd * (1 / TASAS['USD'][moneda_origen])

    # Si tenemos la tasa directa USD a moneda_destino
    if moneda_origen == 'USD' and moneda_destino in TASAS['USD']:
        return TASAS['USD'][moneda_destino]

    # Si necesitamos la tasa inversa
    if moneda_destino == 'USD' and moneda_origen in TASAS['USD']:
        return 1 / TASAS['USD'][moneda_origen]

    # Si necesitamos hacer una conversión cruzada a través de USD
    if moneda_origen in TASAS['USD'] and moneda_destino in TASAS['USD']:
        tasa_origen_usd = 1 / TASAS['USD'][moneda_origen]
        tasa_usd_destino = TASAS['USD'][moneda_destino]
        return tasa_origen_usd * tasa_usd_destino

def main():
    st.markdown("""
    <h1 style='text-align: center; color: #3BA8A8;'>
        💱 Calculadora Mágica de Divisas ✨
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='padding: 15px; background-color: #f0f8ff; border-radius: 10px; margin-bottom: 20px;'>
        🌍 Convierte fácilmente entre diferentes monedas del mundo
        <br>🔄 Tasas de cambio actualizadas al 8 de marzo 2025
        <br>💡 Soporte para múltiples divisas
        <br>🎯 Tasa COP/USD personalizable
    </div>
    """, unsafe_allow_html=True)

    # Configuración de tasa COP/USD
    st.sidebar.markdown("### 💵 Configuración COP/USD")
    tasa_cop_usd = st.sidebar.number_input(
        "Tasa de cambio COP/USD",
        min_value=1000.0,
        max_value=10000.0,
        value=3900.0,
        step=10.0,
        help="Define la tasa de cambio entre Peso Colombiano y Dólar"
    )

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
            tasa = calcular_tasa(moneda_origen, moneda_destino, tasa_cop_usd)
            resultado = cantidad * tasa

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
            st.info(f"📊 Tasa de cambio: 1 {moneda_origen} = {tasa:,.4f} {moneda_destino}")

        except Exception as e:
            st.error("❌ Error al realizar la conversión. Por favor, intente nuevamente.")

    # Información adicional con estilo
    st.markdown("---")
    st.markdown("""
    <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;'>
        <div style='text-align: center; padding: 15px; background-color: #f0f0f0; border-radius: 10px;'>
            📅 Tasas actualizadas mensualmente
        </div>
        <div style='text-align: center; padding: 15px; background-color: #f0f0f0; border-radius: 10px;'>
            🏦 Tasas de referencia del mercado
        </div>
        <div style='text-align: center; padding: 15px; background-color: #f0f0f0; border-radius: 10px;'>
            💱 Conversiones instantáneas
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()