import streamlit as st
import pandas as pd
from src import data_engine as de

# ---------------------------------------------------------------------------
# Configurações da página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Garden Shop – Dashboard de Estoque",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Carregamento de dados (executado uma única vez por sessão)
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_consolidated_data():
    raw = de.load_raw_data()
    consolidated = de.build_consolidated_inventory(raw)
    return consolidated

consolidated_df = get_consolidated_data()

# ---------------------------------------------------------------------------
# Cálculo dos KPIs
# ---------------------------------------------------------------------------
kpis = de.compute_kpis(consolidated_df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Valor total do estoque (custo)", f"US$ {kpis['inventory_value_usd']:,}")
col2.metric("Unidades vendidas (pedidos válidos)", f"{kpis['units_sold_total']:,}")
col3.metric("Produtos em alerta/reposição", f"{kpis['products_in_alert']}")
col4.metric("Produtos em ruptura", f"{kpis['products_in_rupture']}")

st.divider()

# ---------------------------------------------------------------------------
# Barra lateral – filtros
# ---------------------------------------------------------------------------
st.sidebar.header("Filtros")
# Filtro de categoria
category_options = sorted(consolidated_df["category_name"].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Categoria", options=category_options, default=category_options
)
# Filtro de status de alerta (exclui descontinuados se desejar)
alert_options = ["Ruptura", "Crítico", "Alerta", "Observação", "Adequado"]
selected_alerts = st.sidebar.multiselect(
    "Situação de alerta", options=alert_options, default=alert_options
)

filtered_df = de.filter_inventory(
    consolidated_df,
    categories=selected_categories,
    alert_statuses=selected_alerts,
)

# ---------------------------------------------------------------------------
# Tabela de reposição – destaque visual por status
# ---------------------------------------------------------------------------
st.subheader("Produtos em destaque para reposição")
# Definir cores condicionais
def style_alert(row):
    color_map = {
        "Ruptura": "#ff6666",
        "Crítico": "#ffcc66",
        "Alerta": "#ffff99",
        "Observação": "#c2f0c2",
        "Adequado": "#e0e0e0",
        "Descontinuado": "#d9d9d9",
    }
    background = f"background-color: {color_map.get(row['alert_status'], '#ffffff')}"
    return [background] * len(row)

styled = filtered_df.style.apply(style_alert, axis=1)
st.dataframe(styled, hide_index=True, use_container_width=True)

# ---------------------------------------------------------------------------
# Gráfico – Top 5 produtos mais vendidos
# ---------------------------------------------------------------------------
st.subheader("Top 5 produtos mais vendidos (unidades)")
if not filtered_df.empty:
    top5 = (
        filtered_df.sort_values("units_sold", ascending=False)
        .head(5)
        .loc[:, ["product_name", "units_sold", "quantity_on_hand", "alert_status"]]
    )
    chart = st.bar_chart(data=top5.set_index("product_name")["units_sold"])
else:
    st.info("Nenhum produto corresponde aos filtros selecionados.")

# ---------------------------------------------------------------------------
# Informações de contato do fornecedor (coluna opcional para exportação)
# ---------------------------------------------------------------------------
st.caption(
    "*Para cada linha acima, o contato do fornecedor está disponível na coluna ‘supplier_email’. "
    "Caso o e‑mail não conste, será exibido ‘Não informado’.*"
)

# ---------------------------------------------------------------------------
# Footer – referência ao repositório
# ---------------------------------------------------------------------------
st.markdown(
    "---\n" +
    "Projeto desenvolvido por **Júlia Maria de Carvalho Vale** – "
    "[GitHub repository (link a ser adicionado)](https://github.com/your-username/garden-shop-dashboard)"
)