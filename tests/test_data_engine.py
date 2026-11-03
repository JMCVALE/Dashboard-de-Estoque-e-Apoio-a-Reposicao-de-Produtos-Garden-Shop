"""Suíte de testes automatizados para o motor de dados Garden Shop.

Valida os requisitos contábeis, de regra de negócio e de integridade:
- REQ-001: Leitura das tabelas CSV
- REQ-002: Exclusão de cancelados e 86 unidades totais
- REQ-003: Valor patrimonial a custo exatamente US$ 4.763,00
- REQ-004: Classificação de criticidade e 5 produtos em necessidade de reposição
- REQ-005: Tratamento de produtos descontinuados sem alerta de reposição
- REQ-006: Garantia de exatamente 24 produtos na consolidação
- REQ-007: Filtros dinâmicos
- REQ-008: E-mails de fornecedores ausentes tratados com valor amigável
"""

import pytest
from src.data_engine import (
    load_raw_data,
    calculate_sales_summary,
    classify_inventory_status,
    calculate_reorder_deficit,
    build_consolidated_inventory,
    compute_kpis,
    filter_inventory,
)


@pytest.fixture(scope="module")
def raw_data():
    return load_raw_data()


@pytest.fixture(scope="module")
def consolidated_df(raw_data):
    return build_consolidated_inventory(raw_data)


def test_data_loader_loads_all_tables(raw_data):
    """REQ-001: Todas as tabelas essenciais devem ser carregadas."""
    expected_tables = ["products", "categories", "suppliers", "orders", "order_items"]
    for table in expected_tables:
        assert table in raw_data, f"Tabela {table} ausente nos dados brutos"
        assert not raw_data[table].empty, f"Tabela {table} está vazia"


def test_consolidated_inventory_has_exactly_24_products(consolidated_df):
    """REQ-006: Consolidação deve ter exatamente 24 produtos, sem duplicação de linhas."""
    assert len(consolidated_df) == 24
    assert consolidated_df["product_id"].nunique() == 24


def test_sales_calculation_excludes_cancelled(raw_data, consolidated_df):
    """REQ-002: Pedidos cancelados devem ser excluídos. Total de unidades vendidas deve ser rigorosamente 86."""
    sales_summary = calculate_sales_summary(raw_data["orders"], raw_data["order_items"])
    total_units_sold = sales_summary["units_sold"].sum()
    assert total_units_sold == 86, f"Esperado 86 unidades vendidas válidas, obtido {total_units_sold}"

    # No consolidated_df a soma também deve ser exatamente 86
    assert consolidated_df["units_sold"].sum() == 86

    # Pruning Shears (product_id 9): order 17 tem status 'cancelled' com 1 unidade.
    # Total em order_items: order 7 (1 unid) + order 17 (1 unid, cancelado).
    # Unidades válidas computadas devem ser rigorosamente 1.
    pruning_shears = consolidated_df[consolidated_df["product_name"] == "Pruning Shears"]
    assert not pruning_shears.empty
    assert pruning_shears.iloc[0]["units_sold"] == 1


def test_total_inventory_value_equals_4763(consolidated_df):
    """REQ-003: O valor patrimonial do estoque a custo deve somar exatamente US$ 4.763,00."""
    total_cost = consolidated_df["total_cost_value"].sum()
    assert round(total_cost, 2) == 4763.00, f"Esperado 4763.00, obtido {total_cost}"


def test_alert_classification_categories():
    """REQ-004: Validação das faixas de criticidade de estoque para produtos ativos."""
    # Ruptura: qoh == 0
    assert classify_inventory_status(quantity_on_hand=0, reorder_level=10, discontinued=False) == "Ruptura"
    # Crítico: ratio < 0.5
    assert classify_inventory_status(quantity_on_hand=4, reorder_level=10, discontinued=False) == "Crítico"
    # Alerta: 0.5 <= ratio < 1.0
    assert classify_inventory_status(quantity_on_hand=5, reorder_level=10, discontinued=False) == "Alerta"
    assert classify_inventory_status(quantity_on_hand=9, reorder_level=10, discontinued=False) == "Alerta"
    # Observação: 1.0 <= ratio <= 1.5
    assert classify_inventory_status(quantity_on_hand=10, reorder_level=10, discontinued=False) == "Observação"
    assert classify_inventory_status(quantity_on_hand=15, reorder_level=10, discontinued=False) == "Observação"
    # Adequado: ratio > 1.5
    assert classify_inventory_status(quantity_on_hand=16, reorder_level=10, discontinued=False) == "Adequado"


def test_discontinued_product_has_no_reorder_alert(consolidated_df):
    """REQ-005: Produtos descontinuados não devem gerar alerta de compra nem déficit."""
    discontinued_items = consolidated_df[consolidated_df["discontinued"]]
    assert len(discontinued_items) > 0

    for _, row in discontinued_items.iterrows():
        assert row["alert_status"] == "Descontinuado"
        assert row["reorder_deficit"] == 0


def test_five_products_require_reorder(consolidated_df):
    """Critério do AGENTS.md e PRD: exatamente 5 produtos ativos exigem reposição imediata."""
    reorder_items = consolidated_df[consolidated_df["reorder_deficit"] > 0]
    assert len(reorder_items) == 5, f"Esperados 5 itens com déficit de reposição, encontrados {len(reorder_items)}"

    # Verifica se os status desses itens são Ruptura, Crítico ou Alerta
    valid_statuses = {"Ruptura", "Crítico", "Alerta"}
    for _, row in reorder_items.iterrows():
        assert row["alert_status"] in valid_statuses
        assert row["quantity_on_hand"] < row["reorder_level"]


def test_supplier_join_and_missing_emails(consolidated_df):
    """REQ-008: Junção com fornecedores preenche e-mails nulos com 'Não informado'."""
    assert not consolidated_df["supplier_name"].isnull().any()
    assert not consolidated_df["supplier_email"].isnull().any()
    assert "Não informado" in consolidated_df["supplier_email"].values


def test_filter_by_category(consolidated_df):
    """REQ-007: Filtro por categoria deve isolar corretamente os registros."""
    category_name = "Seeds & Bulbs"
    filtered_df = filter_inventory(consolidated_df, category=category_name)
    assert len(filtered_df) > 0
    assert (filtered_df["category_name"] == category_name).all()

    # Filtro inexistente
    empty_df = filter_inventory(consolidated_df, category="Categoria Inexistente")
    assert len(empty_df) == 0


def test_compute_kpis_accuracy(consolidated_df):
    """Valida cálculo de KPIs consolidados."""
    kpis = compute_kpis(consolidated_df)
    assert kpis["total_inventory_value"] == 4763.00
    assert kpis["total_units_sold"] == 86
    assert kpis["total_products"] == 24
    assert kpis["total_reorder_items"] == 5
    assert kpis["total_deficit_units"] > 0
    assert kpis["total_suggested_investment"] > 0
