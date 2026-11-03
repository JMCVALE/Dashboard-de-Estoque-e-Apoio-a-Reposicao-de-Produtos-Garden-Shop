# PRD — Product Requirements Document

> **Objetivo:** definir o problema, os usuários, os objetivos e os requisitos do produto antes de iniciar a implementação do Dashboard de Estoque da Garden Shop.

## 1. Identificação do projeto

- **Nome do projeto:** Dashboard de Gestão de Estoque e Apoio à Reposição — Garden Shop
- **Versão do documento:** 1.0
- **Status:** Aprovado
- **Responsável:** Júlia Maria de Carvalho Vale
- **Data:** 2026-11-02

## 2. Visão geral

### 2.1. Contexto

A **Garden Shop** é uma loja virtual de produtos de jardinagem que comercializa vasos, sementes, ferramentas, adubos e acessórios. A operação depende de dados distribuídos em arquivos relacionais brutos (`products.csv`, `categories.csv`, `suppliers.csv`, `orders.csv` e `order_items.csv`). O gestor de compras e estoque precisa inspecionar manualmente múltiplas planilhas para descobrir quais itens estão em falta e quais fornecedores contatar, gerando lentidão e riscos de ruptura de estoque.

### 2.2. Problema

Atualmente, não existe uma visão única consolidada para a tomada de decisão sobre reposição de estoque. As principais dificuldades enfrentadas são:
1. Risco de ruptura de produtos de alta demanda sem alerta prévio;
2. Dificuldade de calcular o valor financeiro do estoque imobilizado a preço de custo;
3. Insegurança no relacionamento entre vendas e itens pendentes de reposição, correndo o risco de duplicar saldos ou incluir vendas canceladas na demanda;
4. Falta de clareza sobre qual fornecedor contatar para cada item que precisa ser reposto.

### 2.3. Solução proposta

Desenvolvimento de um dashboard analítico e operacional interativo construído em **Streamlit** (com suporte à execução no navegador via **Stlite** no GitHub Pages e execução local padrão), permitindo ao gestor:
- Visualizar imediatamente indicadores-chave de desempenho (KPIs): Total de Capital Imobilizado a Custo (US$) e Total de Produtos em Situação de Alerta/Ruptura;
- Filtrar itens por Categoria e por Situação do Pedido;
- Consultar uma Tabela Prioritária de Reposição ordenada pelo grau de criticidade e pelo volume de vendas;
- Analisar um gráfico de distribuição de estoque e itens mais vendidos.

### 2.4. Proposta de valor

Transformar o estoque em uma lista de ação direta: em menos de 10 segundos, o gestor enxerga o que repor primeiro, com qual fornecedor falar, qual o déficit exato de unidades e qual o valor financeiro do estoque.

## 3. Objetivos e resultados esperados

### 3.1. Objetivos

1. Consolidar os dados operacionais em uma visão única, sem duplicar registros de estoque nem inflar demandas com pedidos cancelados.
2. Identificar com exatidão produtos em situação de ruptura (`quantity_on_hand == 0`) e críticos (`quantity_on_hand < reorder_level`), desconsiderando produtos descontinuados da recomendação de reposição.
3. Exibir o valor total do estoque avaliado a custo com precisão contábil (referência da base: US$ 4.763,00).
4. Facilitar o acionamento dos fornecedores exibindo dados de contato e déficit de compra.

### 3.2. Indicadores de sucesso

| Indicador | Situação atual | Meta | Como medir |
| :--- | :--- | :--- | :--- |
| Tempo para identificar itens em ruptura | Minutos em planilhas manuais | < 5 segundos | Tempo de carga do dashboard e leitura do KPI/Tabela |
| Acurácia no cálculo do valor em estoque | Discrepâncias por fórmulas manuais | 100% de precisão | Concordância exata com a soma de `quantity_on_hand * cost` dos 24 produtos |
| Risco de compra indevida de descontinuados | Médio (produtos descontinuados misturados) | Zero compras indevidas | Bloqueio de alerta e marcação visual "Descontinuado" |
| Precisão no cálculo de demanda vendida | Inclusão indevida de cancelados | 100% de vendas válidas | Exclusão estrita do status `cancelled` nos agregadores |

### 3.3. Critérios de sucesso

- O dashboard carrega localmente e na web de forma interativa.
- Todos os 24 produtos da base são carregados e classificados corretamente (23 ativos e 1 descontinuado).
- Os 5 produtos ativos que exigem reposição são listados em ordem de criticidade.
- Os testes unitários automatizados validam todas as fórmulas antes do deploy.

## 4. Usuários e necessidades

### 4.1. Público-alvo

* **Gestor de Compras e Estoque (Usuário Principal):** Responsável por monitorar os níveis de estoque, emitir ordens de compra e negociar com fornecedores.
* **Operador de E-commerce / Logística:** Responsável por acompanhar a disponibilidade de itens para expedição.

### 4.2. Necessidades dos usuários

- *Como gestor de compras*, quero ver os produtos com estoque abaixo do nível mínimo, para que eu possa emitir pedidos de reposição antes do esgotamento total.
- *Como gestor de compras*, quero filtrar por categoria e fornecedor, para agrupar as compras em um único pedido comercial.
- *Como diretor financeiro*, quero saber o valor imobilizado do estoque a custo, para controlar o capital de giro da empresa.
- *Como gestor de estoque*, quero ter certeza de que pedidos cancelados não distorçam a demanda real dos produtos.

### 4.3. Jornada principal

1. O usuário abre o dashboard no navegador.
2. Observa nos cartões superiores o **Valor Total em Estoque** (US$ 4.763,00) e a quantidade de **Produtos em Alerta/Ruptura** (5 produtos ativos).
3. Utiliza os filtros laterais (filtro por Categoria ou busca de produto).
4. Consulta a tabela de ação ordenada, que destaca o item em ruptura (*Hanging Basket*, 0 unid.) e os itens críticos (*Hand Cultivator* e *Tomato Seeds 'Roma'*), visualizando o fornecedor associado e o déficit de reposição.
5. Copia/exporta os dados ou utiliza o e-mail do fornecedor listado para solicitar reposição imediata.

## 5. Escopo do produto

### 5.1. Incluído no escopo (MVP - Versão 1.0)

- Carregamento e higienização das tabelas: `products.csv`, `categories.csv`, `suppliers.csv`, `orders.csv` e `order_items.csv`.
- Cálculo de 4 KPIs no topo:
  1. Valor Total do Estoque a Custo (US$);
  2. Total de Itens em Alerta de Reposição (ativos abaixo do nível mínimo);
  3. Total de Itens em Ruptura de Estoque (zerados);
  4. Volume Total de Itens Vendidos (pedidos efetivos).
- Filtros interativos:
  - Filtro por Categoria de Produto;
  - Filtro por Status do Pedido (para análise de demanda: todos os não cancelados vs. apenas entregues);
  - Filtro por Nível de Alerta (Todos, Apenas Reposição Necessária, Descontinuados).
- Visualizações:
  - Tabela dinâmica de reposição e alerta com cores por status;
  - Gráfico de barras com o Top Produtos Mais Vendidos e sua relação com o estoque.
- Validação por testes automatizados com `pytest`.
- Compatibilidade para rodar localmente (`streamlit run app.py`) e empacotamento para publicação no GitHub Pages via Stlite.

### 5.2. Fora do escopo

- Gestão cadastral de clientes (`customers.csv` deliberadamente não utilizada).
- Módulo de edição ou escrita nos arquivos CSV originais (os arquivos são somente leitura).
- Autenticação e controle de níveis de acesso por usuário.
- Previsão de demanda por IA ou simulação de lead‑time de fornecedores (não suportado pelos dados atuais).

## 12. Implantação no GitHub Pages (Stlite)

1. **Estrutura de diretórios** – a pasta `Garden Shop - bases/` contendo os CSVs deve estar no *root* do repositório.
2. **Arquivo `index.html`** – já contém o bootstrap que monta o Stlite apontando para o diretório corrente (`.`). Nenhum código Python adicional é necessário.
3. **Habilitar GitHub Pages** – Settings → Pages → Source → *Branch: main* → *Folder: (root)* → Save.
4. **URL pública** – será `https://<seu‑usuario>.github.io/garden-shop-dashboard/`.
5. **Teste** – ao abrir a URL, o dashboard deve renderizar os KPIs, filtros, tabela e gráfico sem erros. Caso haja mensagem "Failed to fetch …", verifique se a pasta de CSVs foi commitada.

## 13. Critérios de aceitação final

- Todos os testes (`pytest tests/ -v`) passam com 0 falhas.
- O valor patrimonial do estoque exibido no dashboard é exatamente **US$ 4 763,00**.
- O volume de unidades vendidas exibido é **86 unidades**.
- Os 5 produtos críticos são destacados com seus déficits corretos.
- O dashboard carrega sem exceções tanto localmente (`streamlit run app.py`) quanto na URL do GitHub Pages.


### 5.1. Incluído no escopo (MVP - Versão 1.0)

- Carregamento e higienização das tabelas: `products.csv`, `categories.csv`, `suppliers.csv`, `orders.csv` e `order_items.csv`.
- Cálculo de 4 KPIs no topo:
  1. Valor Total do Estoque a Custo (US$);
  2. Total de Itens em Alerta de Reposição (ativos abaixo do nível mínimo);
  3. Total de Itens em Ruptura de Estoque (zerados);
  4. Volume Total de Itens Vendidos (pedidos efetivos).
- Filtros interativos:
  - Filtro por Categoria de Produto;
  - Filtro por Status do Pedido (para análise de demanda: todos os não cancelados vs. apenas entregues);
  - Filtro por Nível de Alerta (Todos, Apenas Reposição Necessária, Descontinuados).
- Visualizações:
  - Tabela dinâmica de reposição e estoque com status colorido (Ruptura, Crítico, Alerta, Adequado, Descontinuado) e déficit calculado;
  - Gráfico de barras com o Top Produtos Vendidos e sua relação com o estoque atual.
- Validação por testes automatizados (`pytest`).
- Compatibilidade para rodar localmente (`streamlit run app.py`) e deploy no GitHub Pages via Stlite.

### 5.2. Fora do escopo

- Gestão cadastral de clientes (`customers.csv` deliberadamente não utilizada, conforme aprovado na Lista 01).
- Módulo de edição ou escrita nos arquivos CSV originais (os arquivos são somente leitura).
- Autenticação e controle de níveis de acesso por usuário.
- Previsão de demanda por inteligência artificial / machine learning ou simulação de lead time de fornecedores (não suportado pelos dados atuais).

### 5.3. Premissas

- Os arquivos CSV estão no diretório `Garden Shop - bases/` com codificação UTF-8 ou compatível.
- A coluna `quantity_on_hand` representa o saldo físico real disponível no momento presente.
- A tabela `orders` define a validade das vendas através da coluna `order_status`.

### 5.4. Restrições

- Não utilizar dados fictícios que contradigam o dicionário `garden_shop_dicionario_dados.xlsx`.
- Preservar integridade dos arquivos originais.
- Não usar a cor vermelha nas entregas de relatórios conforme instrução da disciplina.

## 6. Requisitos funcionais

| ID | Requisito | Prioridade | Critério de aceitação |
| :--- | :--- | :--- | :--- |
| **RF-001** | Carregar dados dos arquivos CSV da Garden Shop | Must | Todas as 5 tabelas relevantes lidas sem erro e tipadas corretamente. |
| **RF-002** | Excluir pedidos cancelados do cômputo de vendas | Must | Pedidos com `order_status == 'cancelled'` são desconsiderados no volume e receita vendidos. |
| **RF-003** | Calcular valor total do estoque a custo | Must | Soma exata de `quantity_on_hand * cost` dos 24 produtos, totalizando US$ 4.763,00. |
| **RF-004** | Classificar status de alerta do produto | Must | Classificar em Ruptura (estoque = 0), Crítico (<50% do nível), Alerta (50% a <100%), Observação (100% a 150%) e Adequado (>150%). |
| **RF-005** | Isolar produtos descontinuados de reposição | Must | Produtos com `discontinued == True` não aparecem como sugestão de compra nem no contador de alerta ativo. |
| **RF-006** | Calcular déficit de reposição | Must | Para itens abaixo do nível: `reorder_level - quantity_on_hand`; para itens adequados ou descontinuados: 0. |
| **RF-007** | Filtrar produtos por categoria | Must | Ao selecionar uma ou mais categorias, tabela e métricas refletem a seleção imediatamente. |
| **RF-008** | Exibir fornecedor e contato associados | Must | Tabela de reposição exibe o nome do fornecedor e e-mail correspondente via junção por `supplier_id`. |
| **RF-009** | Gráfico de relação vendas vs. estoque | Should | Exibir visualmente os itens mais vendidos e o estoque remanescente. |

## 7. Requisitos não funcionais

| ID | Categoria | Requisito | Critério de verificação |
| :--- | :--- | :--- | :--- |
| **RNF-001** | Desempenho | Tempo de carregamento inicial menor que 2 segundos localmente | Medição em execução do Streamlit. |
| **RNF-002** | Portabilidade | Funcionar em ambiente local Python e em GitHub Pages | Execução via `streamlit run` e via arquivo web estático `index.html` (Stlite). |
| **RNF-003** | Confiabilidade | Ausência de duplicação em junções de tabelas | Teste automatizado garantindo que a base consolidada possua exatamente 24 produtos. |
| **RNF-004** | Usabilidade | Interface intuitiva, responsiva e legível | Indicadores em cards de destaque e tabela com rolagem e busca. |

## 8. Dados e integrações

- **Fontes de dados:**
  - `products.csv` (24 registros)
  - `categories.csv` (8 registros)
  - `suppliers.csv` (6 registros)
  - `orders.csv` (24 registros)
  - `order_items.csv` (48 registros)
- **Entradas:** Arquivos CSV na pasta local do projeto.
- **Saídas:** Interface web interativa do dashboard e métricas exportáveis.
- **Dados sensíveis:** Não há (dados anonimizados de loja fictícia).

## 9. Regras de negócio

- **RN-001 (Pedidos cancelados):** Vendas com status `cancelled` devem ser rigorosamente excluídas do cômputo de unidades vendidas.
- **RN-002 (Pedidos válidos):** Vendas com status `shipped` são concluídas; `processing` e `pending` são demandas em andamento que consomem estoque.
- **RN-003 (Produtos descontinuados):** Produtos com `discontinued == True` não entram no indicador de produtos a repor nem geram déficit de compra, mas continuam compondo o valor patrimonial do estoque.
- **RN-004 (Critério de reposição):** Um produto ativo necessita de reposição se `quantity_on_hand < reorder_level`.
- **RN-005 (Cálculo do valor de estoque):** Sempre calculado a preço de custo (`quantity_on_hand * cost`).
- **RN-006 (Déficit de estoque):** Para produtos ativos abaixo do nível, `deficit = reorder_level - quantity_on_hand`.

## 10. Experiência e interface

- **Plataforma:** Aplicação Web Streamlit (execução local) e GitHub Pages (Stlite WebAssembly).
- **Layout:**
  - Barra lateral com seletores de categoria, status de pedido e pesquisa.
  - Linha superior com 4 cartões de métricas (KPIs).
  - Seção central com a Tabela Operacional de Reposição e Alertas.
  - Seção gráfica com distribuição de categorias e produtos mais demandados.

## 11. Critérios de conclusão do produto

O produto estará pronto quando:
1. Os 3 documentos (`PRD.md`, `SPEC.md`, `AGENTS.md`) estiverem completos e aderentes ao projeto.
2. A suíte de testes com `pytest` cobrir as regras de negócio e passar com 100% de sucesso.
3. O dashboard executar perfeitamente exibindo os dados da Garden Shop.
4. O repositório no GitHub contiver os arquivos do projeto e a captura de tela (print) comprobatória do dashboard ativo.
