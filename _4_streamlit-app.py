import streamlit as st
import pandas as pd
from _3_metrics import weekday_metrics

st.set_page_config(
    page_title="Patrones Semanales del Tipo de Cambio USD",
    layout="wide"
)

st.title("Patrones Semanales en los Movimientos Diarios del Tipo de Cambio USD")
st.caption("Tipos de referencia diarios · retornos logarítmicos · muestra completa")

df = pd.read_csv("exchange_rates.csv")

weekdays_df = weekday_metrics(df)

weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
weekdays_df["day_name"] = pd.Categorical(
    weekdays_df["day_name"],
    categories=weekday_order,
    ordered=True
)
weekdays_df = weekdays_df.sort_values("day_name")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Retorno diario promedio por día de la semana")
    st.bar_chart(
        weekdays_df.set_index("day_name")["avg_return"]
    )

with col_right:
    st.subheader("¿Señal o ruido?")
    st.dataframe(
        weekdays_df[
            ["day_name", "n_days", "volatility", "t_stat"]
        ],
        hide_index=True
    )

st.subheader("Dirección vs magnitud")
st.scatter_chart(
    weekdays_df,
    x="avg_return",
    y="pct_positive_days"
)

st.markdown("""
### Metodología
- Cambios porcentuales diarios convertidos a retornos logarítmicos  
- Agregación por día de la semana  
- El estadístico *t* mide la señal relativa a la volatilidad  
- Los efectos son descriptivos, no predictivos""")
st.markdown("""""")
st.markdown("""""")
st.markdown("""
###**Conclusión**
Los retornos promedio por día de la semana son pequeños y, salvo el jueves, estadísticamente indistinguibles del ruido. Lunes, martes, miércoles y viernes presentan estadísticos t bajos, lo que indica ausencia de un sesgo sistemático. El jueves destaca con un retorno medio positivo y un t stat superior a 2, sugiriendo un efecto positivo históricamente detectable. No obstante, dada la volatilidad observada, el resultado debe interpretarse como descriptivo y no predictivo.**
""")
