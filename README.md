# 🌿 Garden Shop — Dashboard de Gestão de Estoque e Reposição

> **Disciplina:** Inteligência Artificial Aplicada / Gestão de Dados e Decisão  
> **Responsável:** Júlia Maria de Carvalho Vale  
> **Versão:** 1.0 · Status: **Aprovado**

Dashboard analítico e operacional interativo para gestão de estoque da **Garden Shop**, uma loja virtual de produtos de jardinagem. Permite ao gestor de compras identificar produtos em ruptura, críticos e com necessidade de reposição em menos de 10 segundos, com dados de fornecedor e déficit de unidades prontos para ação.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Execução Local](#-instalação-e-execução-local)
- [Testes Automatizados](#-testes-automatizados)
- [Deploy no GitHub Pages](#-deploy-no-github-pages)
- [Regras de Negócio e Critérios de Qualidade](#-regras-de-negócio-e-critérios-de-qualidade)
- [Arquitetura e Dados](#-arquitetura-e-dados)
- [Documentação do Projeto](#-documentação-do-projeto)

---

## 🌱 Visão Geral

A **Garden Shop** opera com dados distribuídos em múltiplos arquivos CSV relacionais. Sem uma visão consolidada, o gestor de compras precisa inspecionar planilhas manualmente, gerando risco de ruptura de estoque e decisões lentas.

Este dashboard resolve o problema consolidando cinco tabelas relacionais em uma única interface interativa que exibe:

| KPI | Valor de Referência |
|:----|:-------------------:|
| 💰 Valor Total do Estoque (a custo) | **US$ 4.763,00** |
| 🚨 Produtos em Alerta/Ruptura (ativos) | **5 produtos** |
| 📦 Unidades Vendidas (pedidos válidos) | **86 unidades** |

> **Nota:** Pedidos com status `cancelled` são rigorosamente excluídos de todos os cálculos de demanda.

---

## ✨ Funcionalidades

- **4 KPIs** em cards de destaque: Valor em Estoque, Itens em Alerta, Itens em Ruptura e Volume Vendido
- **Filtros interativos** por Categoria, Status de Pedido e Nível de Alerta
- **Tabela operacional de reposição** com status colorido por criticidade:
  - 🔴 **Ruptura** — estoque = 0 (ex: *Hanging Basket*)
  - 🟠 **Crítico** — estoque < 50% do nível mínimo (ex: *Hand Cultivator*, *Tomato Seeds 'Roma'*)
  - 🟡 **Alerta** — estoque entre 50% e 100% do nível mínimo
  - 🔵 **Observação** — estoque entre 100% e 150% do nível mínimo
  - 🟢 **Adequado** — estoque > 150% do nível mínimo
  - ⚫ **Descontinuado** — item inativo (sem recomendação de reposição)
- **Déficit calculado** por produto (quantidade a pedir para atingir o nível mínimo)
- **Dados de fornecedor** (nome e e-mail de contato) diretamente na tabela de ação
- **Gráfico** com os produtos mais vendidos e estoque remanescente
- **Compatibilidade dupla:** execução local via Streamlit e web via GitHub Pages (Stlite/WebAssembly)

---

## 📁 Estrutura do Projeto

```
LISTA 2/
├── Garden Shop - bases/        # 📊 CSVs originais (somente leitura)
│   ├── categories.csv          #   8 categorias de produto
│   ├── customers.csv           #   Clientes (fora do escopo)
│   ├── orders.csv              #   24 pedidos
│   ├── order_items.csv         #   48 itens de pedido
│   ├── products.csv            #   24 produtos
│   └── suppliers.csv           #   6 fornecedores
├── templates/                  # 📄 Templates originais da disciplina (NÃO MODIFICAR)
├── src/
│   ├── __init__.py
│   └── data_engine.py          # ⚙️ Lógica de negócio e processamento de dados
├── tests/
│   ├── __init__.py
│   └── test_data_engine.py     # 🧪 Testes unitários com pytest
├── app.py                      # 🖥️ Dashboard Streamlit (execução local)
├── index.html                  # 🌐 Versão web estática (GitHub Pages via Stlite)
├── generate_index.py           # 🔧 Script auxiliar para geração do index.html
├── requirements.txt            # 📦 Dependências Python
├── PRD.md                      # 📝 Documento de Requisitos do Produto
├── SPEC.md                     # 📐 Especificação Técnica de Software
└── AGENTS.md                   # 🤖 Diretrizes para agentes de IA
```

---

## 🔧 Pré-requisitos

- **Python 3.10+**
- `pip` (gerenciador de pacotes Python)

Dependências principais:

| Biblioteca | Versão mínima | Finalidade |
|:-----------|:-------------:|:-----------|
| `streamlit` | ≥ 1.30.0 | Interface do dashboard |
| `pandas` | ≥ 2.0.0 | Processamento e junção de dados |
| `pytest` | ≥ 7.0.0 | Testes automatizados |

---

## 🚀 Instalação e Execução Local

**1. Clone o repositório**

```bash
git clone https://github.com/JMCVALE/Dashboard-de-Estoque-e-Apoio-a-Reposicao-de-Produtos-Garden-Shop/.git
cd garden-shop-dashboard
```

**2. Instale as dependências**

```bash
pip install -r requirements.txt
```

**3. Execute o dashboard**

```bash
streamlit run app.py
```

O dashboard abrirá automaticamente no navegador em `https://jmcvale.github.io/Dashboard-de-Estoque-e-Apoio-a-Reposicao-de-Produtos-Garden-Shop/`.

<img width="1092" height="805" alt="image" src="https://github.com/user-attachments/assets/596bb42b-63f4-4c20-8386-8ec6f622cb56" />

---

## 🧪 Testes Automatizados

A suíte de testes valida todas as regras de negócio críticas antes de qualquer deploy.

```bash
pytest tests/ -v
```

### Cobertura de testes

| Teste | Regra validada |
|:------|:---------------|
| `test_data_loader_loads_all_tables` | Carregamento correto das 5 tabelas CSV |
| `test_sales_calculation_excludes_cancelled` | Exclusão estrita de pedidos cancelados |
| `test_total_inventory_value_equals_4763` | Valor patrimonial exato = **US$ 4.763,00** |
| `test_alert_classification_categories` | Classificação correta de criticidade |
| `test_discontinued_product_has_no_reorder_alert` | Descontinuados fora do alerta de reposição |
| `test_reorder_deficit_formula` | Fórmula de déficit: `reorder_level − quantity_on_hand` |
| `test_filter_by_category` | Filtragem dinâmica por categoria |
| `test_supplier_join_and_missing_emails` | Junção com fornecedores e tratamento de e-mails ausentes |

> ✅ **Critério de qualidade:** todos os testes devem passar com **0 falhas** para que a entrega seja considerada válida.

---

## 🌐 Deploy no GitHub Pages

O dashboard possui uma versão web estática que roda diretamente no navegador via **Stlite** (Streamlit + Pyodide/WebAssembly), sem necessidade de servidor Python.

**Passos para publicar:**

1. Faça o commit de todos os arquivos, incluindo a pasta `Garden Shop - bases/` com os CSVs
2. No GitHub, acesse **Settings → Pages**
3. Em **Source**, selecione: *Branch: `main`* → *Folder: `(root)`* → **Save**
4. Aguarde alguns minutos e acesse a URL gerada:

```
https://jmcvale.github.io/Dashboard-de-Estoque-e-Apoio-a-Reposicao-de-Produtos-Garden-Shop/
```

> ⚠️ Se aparecer a mensagem *"Failed to fetch…"*, verifique se a pasta de CSVs foi incluída no commit.


## 📏 Regras de Negócio e Critérios de Qualidade

### Regras de negócio implementadas

| ID | Regra |
|:---|:------|
| **RN-001** | Pedidos com `order_status == 'cancelled'` são excluídos do cômputo de vendas |
| **RN-002** | Status válidos: `shipped` (concluídos), `processing` e `pending` (em andamento) |
| **RN-003** | Produtos descontinuados (`discontinued == True`) não geram alerta de reposição, mas compõem o valor patrimonial do estoque |
| **RN-004** | Reposição necessária quando `quantity_on_hand < reorder_level` |
| **RN-005** | Valor de estoque sempre calculado a preço de custo: `quantity_on_hand × cost` |
| **RN-006** | Déficit = `reorder_level − quantity_on_hand` (apenas para ativos abaixo do nível) |

### Critérios de aceitação

Uma entrega só é válida quando **todos** os critérios abaixo são satisfeitos:

- [x] Todos os testes em `pytest tests/ -v` passam com **0 falhas**
- [x] Valor patrimonial do estoque = exatamente **US$ 4.763,00**
- [x] Volume de unidades vendidas (pedidos válidos) = **86 unidades**
- [x] Os **5 produtos ativos** que exigem reposição são listados com seus déficits corretos
- [x] Dashboard carrega sem exceções no Streamlit local **e** no GitHub Pages

---

## 🏗️ Arquitetura e Dados

### Fluxo de dados

```
products.csv ──┐
categories.csv ─┤
suppliers.csv ──┤──► build_consolidated_inventory ──► DataFrame (24 produtos)
                │                                          │
orders.csv ─────┤                                     ┌───┴─────────────┐
order_items.csv ┘──► calculate_sales_summary          │                 │
                     (exclui 'cancelled')         compute_kpis     Filtros + UI
                                                       │                 │
                                                  Cards KPIs       Tabela + Gráficos
```

### Fontes de dados

| Arquivo | Registros | Descrição |
|:--------|:---------:|:----------|
| `products.csv` | 24 | Catálogo de produtos (23 ativos, 1 descontinuado) |
| `categories.csv` | 8 | Categorias de produto |
| `suppliers.csv` | 6 | Fornecedores e dados de contato |
| `orders.csv` | 24 | Pedidos de clientes |
| `order_items.csv` | 48 | Itens por pedido |

### Módulo `src/data_engine.py`

| Função | Responsabilidade |
|:-------|:----------------|
| `load_raw_data(data_dir)` | Lê e sanitiza todos os CSVs |
| `calculate_sales_summary(orders_df, order_items_df)` | Agrega vendas válidas por produto |
| `build_consolidated_inventory(raw_data)` | Une todas as tabelas (exatamente 24 linhas) |
| `compute_kpis(consolidated_df)` | Extrai métricas globais (valor, alertas, etc.) |
| `filter_inventory(df, category, status_alerta)` | Aplica filtros interativos do usuário |

---

## 📚 Documentação do Projeto

| Documento | Conteúdo |
|:----------|:---------|
| [`PRD.md`](PRD.md) | Requisitos do produto, jornada do usuário e regras de negócio |
| [`SPEC.md`](SPEC.md) | Especificação técnica, fórmulas, contratos de dados e plano de testes |
| [`AGENTS.md`](AGENTS.md) | Diretrizes para agentes de IA e desenvolvedores |

---

## 📎 Abordagem de Desenvolvimento

Este projeto adota uma combinação de **SDD (Spec-Driven Development)** e **TDD (Test-Driven Development)**:

- **SDD:** O `PRD.md` e a `SPEC.md` orientam todo o escopo. Nenhuma regra é codificada sem documentação prévia na especificação técnica.
- **TDD:** As regras de negócio são traduzidas em testes unitários automatizados com `pytest` *antes ou em conjunto* com a implementação, garantindo 100% de precisão nos cálculos.

---

<div align="center">
  <sub>Garden Shop Dashboard · Desenvolvido por Júlia Maria de Carvalho Vale · 2026</sub>
</div>
