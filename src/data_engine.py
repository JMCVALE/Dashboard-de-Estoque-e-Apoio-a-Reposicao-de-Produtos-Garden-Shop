"""Motor de processamento de dados e regras de negócio da Garden Shop.

Seguindo as especificações de SPEC.md e PRD.md:
- REQ-001: Carregamento tolerante e higienização das tabelas.
- REQ-002: Exclusão rigorosa de pedidos com status == 'cancelled'.
- REQ-003: Cálculo do valor total de estoque a custo (exatamente US$ 4.763,00).
- REQ-004: Classificação de criticidade de estoque (Ruptura, Crítico, Alerta, Observação, Adequado, Descontinuado).
- REQ-005: Cálculo de déficit de reposição para itens não descontinuados abaixo do ponto de pedido.
- REQ-006: Garantia de exatamente 24 produtos consolidados sem duplicações.
"""

from pathlib import Path
from typing import Dict, Optional, Union
import pandas as pd


def get_default_data_dir() -> Path:
    """Retorna o diretório base das tabelas CSV."""
    candidates = [
        Path("Garden Shop - bases"),
        Path.cwd() / "Garden Shop - bases",
        Path.cwd().parent / "Garden Shop - bases",
        Path("."),
    ]
    for candidate in candidates:
        if (candidate / "products.csv").exists():
            return candidate
    return Path("Garden Shop - bases")


def load_raw_data(data_dir: Optional[Union[str, Path]] = None) -> Dict[str, pd.DataFrame]:
    """Carrega todas as tabelas CSV sanitizando os tipos básicos.

    Tabelas: products, categories, suppliers, orders, order_items.
    """
    if data_dir is None:
        base_path = get_default_data_dir()
    else:
        base_path = Path(data_dir)

    products = pd.read_csv(base_path / "products.csv")
    categories = pd.read_csv(base_path / "categories.csv")
    suppliers = pd.read_csv(base_path / "suppliers.csv")
    orders = pd.read_csv(base_path / "orders.csv")
    order_items = pd.read_csv(base_path / "order_items.csv")

    # Padronização e higienização de orders: mapear status para order_status se necessário
    if "status" in orders.columns and "order_status" not in orders.columns:
        orders["order_status"] = orders["status"]

    # Higienização de suppliers: padronizar nome de e-mail e nome
    if "contact_email" in suppliers.columns and "supplier_email" not in suppliers.columns:
        suppliers["supplier_email"] = suppliers["contact_email"].fillna("Não informado")
    elif "email" in suppliers.columns:
        suppliers["supplier_email"] = suppliers["email"].fillna("Não informado")

    if "name" in suppliers.columns and "supplier_name" not in suppliers.columns:
        suppliers["supplier_name"] = suppliers["name"]

    # Higienização de tipos em products
    if "discontinued" in products.columns:
        # Se for string 'True'/'False' ou boolean
        products["discontinued"] = products["discontinued"].astype(str).str.lower().isin(["true", "1", "t"])
    if "cost" in products.columns:
        products["cost"] = products["cost"].astype(float)
    if "price" in products.columns:
        products["price"] = products["price"].astype(float)
    if "quantity_on_hand" in products.columns:
        products["quantity_on_hand"] = products["quantity_on_hand"].astype(int)
    if "reorder_level" in products.columns:
        products["reorder_level"] = products["reorder_level"].astype(int)

    return {
        "products": products,
        "categories": categories,
        "suppliers": suppliers,
        "orders": orders,
        "order_items": order_items,
    }


def calculate_sales_summary(orders_df: pd.DataFrame, order_items_df: pd.DataFrame) -> pd.DataFrame:
    """Calcula unidades vendidas e receita por produto, excluindo pedidos cancelados (REQ-002)."""
    orders = orders_df.copy()
    status_col = "order_status" if "order_status" in orders.columns else "status"

    # Filtra apenas pedidos não cancelados
    valid_orders = orders[orders[status_col].astype(str).str.lower() != "cancelled"]

    # Junção com itens de pedido
    valid_items = order_items_df.merge(
        valid_orders[["order_id", status_col]],
        on="order_id",
        how="inner"
    )

    if valid_items.empty:
        return pd.DataFrame(columns=["product_id", "units_sold", "revenue"])

    if "unit_price" in valid_items.columns:
        valid_items["item_revenue"] = valid_items["quantity"] * valid_items["unit_price"]
    else:
        valid_items["item_revenue"] = 0.0

    sales_summary = (
        valid_items.groupby("product_id")
        .agg(
            units_sold=("quantity", "sum"),
            revenue=("item_revenue", "sum")
        )
        .reset_index()
    )

    return sales_summary


def classify_inventory_status(quantity_on_hand: int, reorder_level: int, discontinued: bool) -> str:
    """Aplica a regra de classificação de alertas de reposição (REQ-004)."""
    if discontinued:
        return "Descontinuado"

    if quantity_on_hand == 0:
        return "Ruptura"

    ratio = quantity_on_hand / reorder_level if reorder_level > 0 else 999.0

    if ratio < 0.5:
        return "Crítico"
    elif ratio < 1.0:
        return "Alerta"
    elif ratio <= 1.5:
        return "Observação"
    else:
        return "Adequado"


def calculate_reorder_deficit(quantity_on_hand: int, reorder_level: int, discontinued: bool) -> int:
    """Calcula o déficit de unidades para atingir o nível de reposição (REQ-005)."""
    if discontinued:
        return 0
    if quantity_on_hand < reorder_level:
        return int(reorder_level - quantity_on_hand)
    return 0


def build_consolidated_inventory(raw_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Constrói a tabela consolidada de produtos (24 linhas) com dados cadastrais, fornecedores e vendas."""
    products = raw_data["products"].copy()
    categories = raw_data["categories"].copy()
    suppliers = raw_data["suppliers"].copy()
    orders = raw_data["orders"].copy()
    order_items = raw_data["order_items"].copy()

    # Vendas consolidadas previamente agrupadas por product_id para evitar duplicação (REQ-006)
    sales_summary = calculate_sales_summary(orders, order_items)

    # Left join com categories
    df = products.merge(
        categories[["category_id", "category_name"]],
        on="category_id",
        how="left"
    )

    # Normalização de colunas de fornecedores
    supp_cols = ["supplier_id", "supplier_name"]
    if "supplier_email" in suppliers.columns:
        supp_cols.append("supplier_email")
    elif "contact_email" in suppliers.columns:
        suppliers["supplier_email"] = suppliers["contact_email"]
        supp_cols.append("supplier_email")

    if "state" in suppliers.columns:
        supp_cols.append("state")

    df = df.merge(
        suppliers[supp_cols],
        on="supplier_id",
        how="left"
    )

    # Left join com sales_summary
    df = df.merge(sales_summary, on="product_id", how="left")

    # Tratamento de valores nulos
    df["units_sold"] = df["units_sold"].fillna(0).astype(int)
    df["revenue"] = df["revenue"].fillna(0.0).round(2).astype(float)
    df["supplier_email"] = df["supplier_email"].fillna("Não informado")
    df["supplier_name"] = df["supplier_name"].fillna("Não informado")

    # Cálculos derivados
    df["total_cost_value"] = (df["quantity_on_hand"] * df["cost"]).round(2)
    df["total_retail_value"] = (df["quantity_on_hand"] * df["price"]).round(2)
    df["margin_unit"] = (df["price"] - df["cost"]).round(2)
    df["reorder_ratio"] = (df["quantity_on_hand"] / df["reorder_level"]).round(2)

    # Status de alerta e déficit
    df["alert_status"] = df.apply(
        lambda r: classify_inventory_status(r["quantity_on_hand"], r["reorder_level"], r["discontinued"]),
        axis=1
    )
    df["reorder_deficit"] = df.apply(
        lambda r: calculate_reorder_deficit(r["quantity_on_hand"], r["reorder_level"], r["discontinued"]),
        axis=1
    )
    df["suggested_investment"] = (df["reorder_deficit"] * df["cost"]).round(2)

    return df


def compute_kpis(df: pd.DataFrame) -> Dict[str, Union[int, float]]:
    """Calcula métricas e KPIs consolidados do inventário."""
    total_inventory_value = round(float(df["total_cost_value"].sum()), 2)
    total_retail_value = round(float(df["total_retail_value"].sum()), 2)
    total_physical_units = int(df["quantity_on_hand"].sum())
    total_units_sold = int(df["units_sold"].sum())

    total_products = len(df)
    active_products = int((~df["discontinued"]).sum())
    discontinued_products = int(df["discontinued"].sum())

    # Contagem de status
    status_counts = df["alert_status"].value_counts().to_dict()
    ruptura_count = status_counts.get("Ruptura", 0)
    critico_count = status_counts.get("Crítico", 0)
    alerta_count = status_counts.get("Alerta", 0)
    observacao_count = status_counts.get("Observação", 0)
    adequado_count = status_counts.get("Adequado", 0)

    # Itens que precisam de reposição imediata (Ruptura + Crítico + Alerta)
    needs_reorder_df = df[df["reorder_deficit"] > 0]
    total_reorder_items = len(needs_reorder_df)
    total_deficit_units = int(needs_reorder_df["reorder_deficit"].sum())
    total_suggested_investment = round(float(needs_reorder_df["suggested_investment"].sum()), 2)

    return {
        "total_inventory_value": total_inventory_value,
        "total_retail_value": total_retail_value,
        "total_physical_units": total_physical_units,
        "total_units_sold": total_units_sold,
        "total_products": total_products,
        "active_products": active_products,
        "discontinued_products": discontinued_products,
        "ruptura_count": ruptura_count,
        "critico_count": critico_count,
        "alerta_count": alerta_count,
        "observacao_count": observacao_count,
        "adequado_count": adequado_count,
        "total_reorder_items": total_reorder_items,
        "total_deficit_units": total_deficit_units,
        "total_suggested_investment": total_suggested_investment,
    }


def filter_inventory(
    df: pd.DataFrame,
    category: Optional[str] = None,
    status_alerta: Optional[str] = None,
    hide_discontinued: bool = False,
    search_query: Optional[str] = None,
) -> pd.DataFrame:
    """Aplica filtros ao DataFrame consolidado."""
    filtered = df.copy()

    if category and category != "Todas":
        filtered = filtered[filtered["category_name"] == category]

    if status_alerta and status_alerta != "Todos":
        filtered = filtered[filtered["alert_status"] == status_alerta]

    if hide_discontinued:
        filtered = filtered[~filtered["discontinued"]]

    if search_query:
        query = search_query.strip().lower()
        filtered = filtered[
            filtered["product_name"].str.lower().str.contains(query)
            | filtered["supplier_name"].str.lower().str.contains(query)
        ]

    return filtered
