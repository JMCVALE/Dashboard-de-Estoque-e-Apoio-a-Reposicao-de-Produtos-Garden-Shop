# app.py
"""Streamlit entry point — Garden Shop Inventory Dashboard.

Execução local:
    streamlit run app.py

Publicação web:
    Utilizar index.html com Stlite (GitHub Pages).
"""

import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

from src import data_engine

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Garden Shop — Dashboard de Estoque",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="metric-container"] {
    background: #f0f7f0;
    border: 1px solid #b7e4c7;
    border-radius: 12px;
    padding: 16px 20px;
}
[data-testid="metric-container"] label { color: #52796f !important; font-weight: 600; }
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #1b4332 !important; font-size: 1.6rem !important; font-weight: 700;
}
.dash-header {
    background: linear-gradient(135deg, #2d6a4f 0%, #40916c 60%, #52b788 100%);
    border-radius: 14px; padding: 24px 32px; margin-bottom: 28px; color: white;
}
.dash-header h1 { margin: 0; font-size: 1.9rem; font-weight: 800; }
.dash-header p  { margin: 6px 0 0; opacity: 0.88; font-size: 1rem; }
[data-testid="stSidebar"] { background: #f0f7f0; }
.badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 0.82rem; font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
BASE_DIR = Path.cwd() / "Garden Shop - bases"

@st.cache_data
def get_data():
    raw = data_engine.load_raw_data(BASE_DIR)
    return data_engine.build_consolidated_inventory(raw)

df_full = get_data()
kpis    = data_engine.compute_kpis(df_full)

# ── Derived KPIs ──────────────────────────────────────────────────────────────
total_value = round(kpis["total_inventory_value"], 2)
total_sold  = int(kpis["total_units_sold"])
n_ruptura   = kpis["alert_counts"].get("Ruptura", 0)
n_alerta    = sum(kpis["alert_counts"].get(s, 0) for s in ["Ruptura", "Crítico", "Alerta"])

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filtros")
    st.markdown("---")

    categorias = ["Todas"] + sorted(df_full["category_name"].dropna().unique().tolist())
    sel_cat    = st.selectbox("📂 Categoria", categorias)

    alertas    = ["Todos", "Ruptura", "Crítico", "Alerta", "Observação", "Adequado", "Descontinuado"]
    sel_alert  = st.selectbox("🚦 Situação de Alerta", alertas)

    busca      = st.text_input("🔎 Buscar produto", placeholder="Ex: Tomato, Hanging…")

    st.markdown("---")
    st.markdown("### 📋 Legenda de Status")
    legenda = {
        "🔴 Ruptura":       "Estoque zerado",
        "🟠 Crítico":       "< 50% do mínimo",
        "🟡 Alerta":        "50–99% do mínimo",
        "🟢 Observação":    "100–150% do mínimo",
        "🔵 Adequado":      "> 150% do mínimo",
        "⚪ Descontinuado": "Item inativo",
    }
    for k, v in legenda.items():
        st.markdown(f"**{k}** — {v}")

    st.markdown("---")
    st.caption("Garden Shop · Dashboard v1.0")
    st.caption("IA Aplicada — Júlia Maria de Carvalho Vale")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <h1>🌿 Garden Shop — Dashboard de Gestão de Estoque</h1>
  <p>Monitoramento em tempo real de estoque, reposição e indicadores operacionais</p>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Valor Total em Estoque",       f"US$ {total_value:,.2f}")
c2.metric("📦 Unidades Vendidas",            str(total_sold))
c3.metric("⚠️ Produtos em Alerta/Ruptura",  str(n_alerta))
c4.metric("🚨 Produtos em Ruptura",          str(n_ruptura))

st.markdown("<br>", unsafe_allow_html=True)

# ── Apply filters ─────────────────────────────────────────────────────────────
df_view = df_full.copy()
if sel_cat   != "Todas":  df_view = df_view[df_view["category_name"] == sel_cat]
if sel_alert != "Todos":  df_view = df_view[df_view["alert_status"]   == sel_alert]
if busca.strip():
    df_view = df_view[df_view["product_name"].str.contains(busca.strip(), case=False, na=False)]

# ── Reorder Table ─────────────────────────────────────────────────────────────
st.subheader("🛒 Tabela Operacional de Reposição e Alertas")

SEVERITY = {"Ruptura": 1, "Crítico": 2, "Alerta": 3, "Observação": 4, "Adequado": 5, "Descontinuado": 6}
BADGE_STYLE = {
    "Ruptura":       "background:#ffccd5;color:#6b0f1a;",
    "Crítico":       "background:#ffe8cc;color:#7c4700;",
    "Alerta":        "background:#fff3cd;color:#6b5900;",
    "Observação":    "background:#d4edda;color:#155724;",
    "Adequado":      "background:#cce5ff;color:#004085;",
    "Descontinuado": "background:#e2e3e5;color:#383d41;",
}
ROW_COLOURS = {
    "Ruptura":       "#ffccd5",
    "Crítico":       "#ffe8cc",
    "Alerta":        "#fff3cd",
    "Observação":    "#d4edda",
    "Adequado":      "#cce5ff",
    "Descontinuado": "#e2e3e5",
}

if df_view.empty:
    st.info("ℹ️ Nenhum produto encontrado com os filtros selecionados.")
else:
    display_cols = [
        "product_name", "category_name", "alert_status",
        "quantity_on_hand", "reorder_level", "reorder_deficit",
        "units_sold", "total_cost_value", "supplier_name", "supplier_email",
    ]
    tbl = (
        df_view[display_cols]
        .copy()
        .assign(_sev=df_view["alert_status"].map(SEVERITY))
        .sort_values(["_sev", "reorder_deficit"], ascending=[True, False])
        .drop(columns=["_sev"])
        .reset_index(drop=True)
    )
    tbl.columns = [
        "Produto", "Categoria", "Status",
        "Estoque Atual", "Nível Mínimo", "Déficit",
        "Und. Vendidas", "Valor em Estoque (US$)", "Fornecedor", "E-mail Fornecedor",
    ]

    def row_color(row):
        bg = ROW_COLOURS.get(row["Status"], "white")
        return [f"background-color:{bg}" for _ in row]

    styled = (
        tbl.style
        .apply(row_color, axis=1)
        .format({
            "Estoque Atual": "{:.0f}",
            "Nível Mínimo":  "{:.0f}",
            "Déficit":       "{:.0f}",
            "Und. Vendidas": "{:.0f}",
            "Valor em Estoque (US$)": "US$ {:,.2f}",
        })
    )
    st.dataframe(styled, hide_index=True, use_container_width=True, height=420)

st.markdown("---")

# ── Charts ────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("📊 Top 10 — Produtos Mais Vendidos vs. Estoque")
    top10 = (
        df_full.sort_values("units_sold", ascending=False)
        .head(10)[["product_name", "units_sold", "quantity_on_hand"]]
        .reset_index(drop=True)
    )
    top10_melted = top10.melt("product_name", var_name="Métrica", value_name="Unidades")
    top10_melted["Métrica"] = top10_melted["Métrica"].map({
        "units_sold": "Unidades Vendidas", "quantity_on_hand": "Estoque Atual"
    })

    chart = (
        alt.Chart(top10_melted)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("product_name:N", sort=None, title="Produto",
                    axis=alt.Axis(labelAngle=-35, labelLimit=120)),
            y=alt.Y("Unidades:Q", title="Unidades"),
            color=alt.Color("Métrica:N",
                scale=alt.Scale(range=["#40916c", "#b7e4c7"]),
                legend=alt.Legend(title="Legenda")),
            xOffset="Métrica:N",
            tooltip=["product_name:N", "Métrica:N", "Unidades:Q"],
        )
        .properties(height=360)
    )
    st.altair_chart(chart, use_container_width=True)

with col_right:
    st.subheader("📋 Valor por Categoria")
    cat_agg = (
        df_full.groupby("category_name")
        .agg(
            Produtos=("product_id", "count"),
            Valor_Total=("total_cost_value", "sum"),
        )
        .reset_index()
        .sort_values("Valor_Total", ascending=False)
        .rename(columns={"category_name": "Categoria", "Valor_Total": "Valor (US$)"})
    )
    cat_agg["Valor (US$)"] = cat_agg["Valor (US$)"].map(lambda x: f"US$ {x:,.2f}")
    st.dataframe(cat_agg, hide_index=True, use_container_width=True, height=360)

st.markdown("---")

# ── Priority Alert cards ───────────────────────────────────────────────────────
st.subheader("🚨 Ação Imediata — Produtos Prioritários para Reposição")
critical = df_full[
    df_full["alert_status"].isin(["Ruptura", "Crítico"]) & (~df_full["discontinued"])
].sort_values(["alert_status", "reorder_deficit"], ascending=[True, False])

if critical.empty:
    st.success("✅ Nenhum produto em situação de ruptura ou criticidade!")
else:
    for _, row in critical.iterrows():
        badge_style = BADGE_STYLE.get(row["alert_status"], "")
        email_txt   = row.get("supplier_email", "Não informado")
        st.markdown(f"""
        <div style="border:1px solid #dee2e6;border-radius:10px;padding:16px 20px;margin-bottom:12px;background:#fff;">
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
            <span class="badge" style="{badge_style}">{row['alert_status']}</span>
            <strong style="font-size:1.05rem;">{row['product_name']}</strong>
            <span style="color:#6c757d;font-size:0.9rem;">— {row['category_name']}</span>
          </div>
          <div style="display:flex;gap:32px;flex-wrap:wrap;font-size:0.92rem;color:#343a40;">
            <span>📦 Estoque atual: <strong>{int(row['quantity_on_hand'])}</strong></span>
            <span>📉 Nível mínimo: <strong>{int(row['reorder_level'])}</strong></span>
            <span>🔻 Déficit: <strong style="color:#c0392b;">{int(row['reorder_deficit'])}</strong> unid.</span>
            <span>🏭 Fornecedor: <strong>{row['supplier_name']}</strong></span>
            <span>✉️ <a href="mailto:{email_txt}" style="color:#2d6a4f;">{email_txt}</a></span>
          </div>
        </div>
        """, unsafe_allow_html=True)

st.caption("Versão 1.0 · Garden Shop Dashboard · Disciplina IA Aplicada · Júlia Maria de Carvalho Vale")
