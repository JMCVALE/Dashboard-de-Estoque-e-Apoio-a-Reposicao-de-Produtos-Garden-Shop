# PRD — Product Requirements Document

> **Objetivo:** definir o problema, os usuários, os objetivos e os requisitos do produto antes de iniciar a implementação.

## 1. Identificação do projeto

- **Nome do projeto:** Dashboard de Estoque e Apoio à Reposição de Produtos — Garden Shop
- **Versão do documento:** 1.0 (implementado)
- **Responsável:** Júlia Maria de Carvalho Vale
- **Data:** 2026-10-27

> Documento redigido com apoio de IA generativa (Claude), a partir da proposta da Lista 1, do enunciado da Lista 2, do dicionário de dados e da base Garden Shop.

## 2. Visão geral

### 2.1. Contexto

A Garden Shop é uma loja virtual de produtos de jardinagem (plantas, sementes, ferramentas, vasos, fertilizantes e outros). 
A empresa mantém uma base com produtos, categorias, fornecedores, pedidos e itens de pedido. Hoje, quem cuida da operação e das compras precisa cruzar essas tabelas manualmente para saber o que repor. 
Este PRD continua a proposta de dashboard da Lista 1 e define a primeira versão a ser implementada na Lista 2.

### 2.2. Problema

A equipe de gestão não consegue identificar rapidamente:
- quais produtos estão abaixo do nível de reposição, zerados ou com estoque muito baixo; 
- quais vendem bem e correm risco de faltar; em que ordem agir e com qual fornecedor falar; 
- quanto dinheiro está parado em estoque.

Ao cruzar as tabelas à mão, há três erros fáceis de cometer: 
- contar pedido cancelado como venda;
- recomendar reposição de produto descontinuado e duplicar o estoque ao juntar `products` com `order_items`. 

Sem resolver isso, as compras são decididas por impressão e não por dados, com risco de ruptura de itens que vendem e de capital parado em itens que não precisam de reposição.

### 2.3. Solução proposta

Um dashboard que transforma o estoque em uma **lista de ação**: o gestor abre a página e vê, em poucos segundos, quais produtos precisam de reposição, em que ordem de prioridade, de qual fornecedor e com qual impacto financeiro. Ele apoia uma única decisão: **"o que repor primeiro e com quem falar?"**. Não analisa clientes, campanhas nem desempenho comercial.

### 2.4. Proposta de valor

Reduzir o cruzamento manual de cinco tabelas a uma leitura rápida e confiável, com as regras de negócio (cancelados, descontinuados, estoque como posição atual) já aplicadas e explicadas na própria tela.

## 3. Objetivos e resultados esperados

### 3.1. Objetivos

- **OBJ-01:** mostrar quantos e quais produtos ativos precisam de reposição, em ordem de prioridade.
- **OBJ-02:** destacar produtos em ruptura ou com estoque muito baixo.
- **OBJ-03:** relacionar o estoque com as vendas efetivas, sem contar pedidos cancelados.
- **OBJ-04:** indicar o fornecedor e o contato de cada produto a repor.
- **OBJ-05:** informar o valor do estoque a custo, por total e por categoria.
- **OBJ-06:** evitar decisões erradas por regra mal aplicada (cancelados, descontinuados e duplicação de estoque).

### 3.2. Indicadores de sucesso

A gestão não definiu metas numéricas, e este PRD não inventa nenhuma. A tabela propõe como medir.

| Indicador | Situação atual | Meta | Como medir |
| --- | --- | --- | --- |
| Tempo para identificar os produtos a repor | Cruzamento manual de cinco tabelas | Não definida pela gestão | A pessoa responsável encontra a lista priorizada ao abrir o painel, sem ajuda |
| Correção dos números exibidos | Sujeita aos três erros da seção 2.2 | Todos os critérios de aceitação da seção 6 conferidos | Comparar o painel com os cálculos feitos sobre os CSVs e com os testes automatizados |

### 3.3. Critérios de sucesso

- Com os filtros padrão, o painel mostra os mesmos valores calculados à mão sobre os CSVs (seção 6).
- A lista de reposição indica os cinco produtos ativos abaixo do nível, na ordem de prioridade, com fornecedor e contato.
- Pedidos cancelados e produtos descontinuados nunca distorcem os números ou as recomendações.

## 4. Usuários e necessidades

### 4.1. Público-alvo

- **Gestor ou responsável por operação e compras (principal):** abre o painel, lê os cartões, consulta a tabela de prioridade e filtra por categoria ou fornecedor.
- **Gestão financeira (secundário):** consulta o valor do estoque a custo.

O usuário não é técnico. O painel deve ser lido rapidamente, com poucos elementos e foco em decisão, e não em exploração livre de dados.

### 4.2. Necessidades dos usuários

- Como gestor de compras, quero ver os produtos abaixo do nível de reposição em ordem de prioridade, para decidir o que comprar primeiro.
- Como gestor de compras, quero ver o fornecedor e o e-mail de cada produto a repor, para saber com quem falar.
- Como gestor de compras, quero filtrar por fornecedor, para montar o pedido de um fornecedor de cada vez.
- Como gestor de operação, quero saber quais produtos vendem bem e estão em risco, para evitar ruptura dos itens mais procurados.
- Como gestor de operação, quero ver quais categorias concentram produtos a repor, para direcionar a atenção da equipe.
- Como gestão financeira, quero saber o valor do estoque a custo, para saber quanto capital está imobilizado.

### 4.3. Jornada principal

1. O gestor abre o dashboard com os dados já carregados.
2. Lê os cartões: quantos produtos precisam de reposição, quantos estão em ruptura ou críticos e qual o valor do estoque.
3. Consulta a tabela de prioridade, do produto mais urgente ao menos urgente, e filtra por categoria ou fornecedor.
4. Usa o fornecedor e o contato da tabela para iniciar a reposição.

## 5. Escopo do produto

### 5.1. Incluído no escopo

- Dashboard funcional que carrega os CSVs originais (`products`, `categories`, `suppliers`, `orders`, `order_items`), sem alterá-los.
- Indicadores, filtros, gráficos e tabela de prioridade descritos na seção 6.
- Regras de negócio da seção 9, com verificação por testes.
- Mensagens para situações sem dados, dados inválidos e filtros sem resultado.

### 5.2. Fora do escopo

- **Cobertura de estoque em dias e giro:** exigem histórico de movimentação, que a base não tem.
- **Previsão de demanda ou de ruptura:** 24 pedidos entre 15/01/2024 e 14/06/2024 não sustentam previsão confiável.
- **Sugestão de quantidade de compra:** não há estoque-alvo nem prazo de entrega; mostra-se só o déficit mínimo até o nível de reposição.
- **Uso de `shipped_date` como prazo de entrega do fornecedor:** é o envio ao cliente, não a entrega do fornecedor à loja.
- **Análise de clientes, estados e cupons:** não ajuda a decidir reposição; `customers.csv` não é carregado.
- **Curva ABC e margem por produto:** não foram pedidas e o volume de vendas é pequeno; ficam como evolução futura.
- **Versão 1.0 simplificada em relação à Lista 1:** duas abas, busca por produto, exportação da lista, filtro cruzado por clique e cortes de alerta ajustáveis ficam para uma versão futura (ver DP-003).
- **Hospedagem na internet, login e edição de dados:** o painel é de leitura e pode rodar localmente.

### 5.3. Premissas

- `quantity_on_hand` representa o estoque atual de cada produto.
- `reorder_level` é o nível de reposição oficial da empresa.
- O custo cadastrado (`cost`) é único por produto.
- Os CSVs originais são a fonte de dados e não são alterados.
- Os pedidos vão de 15/01/2024 a 14/06/2024; o estoque é uma posição atual, sem data de referência.

### 5.4. Restrições

- **Orçamento:** não aplicável.
- **Prazo:** o definido pelo professor para a Lista 2 (data não informada nos materiais).
- **Infraestrutura:** execução local; hospedagem na internet não é obrigatória.
- **Tecnologia:** pendente de decisão (DP-001).
- **Operação:** a base não tem histórico de movimentação de estoque nem prazo de entrega dos fornecedores. A interface não pode usar a cor vermelha, reservada às correções do professor.

## 6. Requisitos funcionais

Os critérios de aceitação usam valores calculados sobre os CSVs originais, com os filtros padrão (todas as categorias e fornecedores, status `shipped`, `processing` e `pending` marcados, descontinuados ocultos), salvo quando indicado. Verificação: **T** = teste automatizado; **M** = conferência manual no painel. O status "verificado" só vale depois da execução.

### 6.1. Indicadores

| ID | Requisito | Prioridade | Critério de aceitação |
| --- | --- | --- | --- |
| RF-001 | O sistema deve exibir **produtos ativos abaixo do nível** (estoque < nível de reposição) | Must | Mostra **5 de 23**: Pothos 'Golden', Tomato Seeds 'Roma', Hand Cultivator, Hanging Basket e Orchid Food. O Bird Feeder (descontinuado) não é contado. Não muda ao alterar status ou período (T) |
| RF-002 | O sistema deve exibir **produtos em ruptura** (estoque = 0) | Must | Mostra **1** (Hanging Basket) (T) |
| RF-003 | O sistema deve exibir **produtos em nível crítico** (estoque abaixo de 50% do nível, exceto ruptura) | Must | Mostra **2**: Tomato Seeds 'Roma' (12,5%) e Hand Cultivator (30%) (T) |
| RF-004 | O sistema deve exibir o **valor do estoque a custo** (Σ estoque × custo) | Must | Mostra **US$ 4.763,00**, sendo US$ 4.731,00 de ativos e US$ 32,00 de descontinuado. O Fiddle-Leaf Fig entra **uma única vez**, com US$ 252,00 (14 × 18), mesmo com 4 itens de pedido (T) |
| RF-005 | O sistema deve exibir as **unidades vendidas efetivas** (itens de pedidos não cancelados) | Must | Mostra **86** unidades. O Pruning Shears mostra **1** unidade: o pedido 17 (cancelado) não é somado (T) |
| RF-006 | O sistema deve exibir o **déficit total para o nível** (Σ déficit dos ativos abaixo do nível) | Should | Mostra **60** unidades (T) |
| RF-007 | O sistema deve exibir as **unidades em pedidos em aberto** (`pending` e `processing`) | Should | Mostra **21** unidades (9 pendentes e 12 em processamento) (T) |
| RF-008 | O sistema deve exibir os **fornecedores com itens a repor** | Should | Mostra **4 de 6** (SunGrow Nurseries, Bloomfield Seeds, Ironwood Tools e Terra Pots Co) (T) |

### 6.2. Filtros

| ID | Requisito | Prioridade | Critério de aceitação |
| --- | --- | --- | --- |
| RF-009 | O sistema deve permitir filtrar por **categoria** | Must | Com Tools: apenas produtos de Tools, valor a custo US$ 448,50 e **1** produto abaixo do nível (Hand Cultivator). Cartões, gráficos e tabela atualizam juntos (T) |
| RF-010 | O sistema deve permitir filtrar por **fornecedor** | Should | Com SunGrow Nurseries: **2** produtos abaixo do nível (Pothos 'Golden' e Orchid Food) (T) |
| RF-011 | O sistema deve permitir filtrar por **nível de alerta** (ruptura, crítico, alerta, observação, adequado) | Should | Com ruptura e crítico: a tabela mostra **3** produtos (Hanging Basket, Tomato Seeds 'Roma' e Hand Cultivator) (T) |
| RF-012 | O sistema deve permitir filtrar as vendas por **status do pedido** (`shipped`, `processing`, `pending`); `cancelled` não pode ser selecionado | Must | Só com `shipped`: **65** unidades vendidas e **0** em aberto; contagens de estoque (5, 1, 2) e valor (US$ 4.763,00) não mudam. Sem nenhum status: vendas = 0 e aviso "nenhum status selecionado" (T/M) |
| RF-013 | O sistema deve permitir **incluir descontinuados** (desligado por padrão) | Must | Ligado, o Bird Feeder (4/6) aparece como "descontinuado — não repor", sem déficit e sem posição de prioridade; "abaixo do nível" continua **5** (T) |
| RF-014 | O sistema deve permitir filtrar as vendas por **período do pedido** (`order_date`, de / até) | Should | Com 01/07/2024 a 31/07/2024 (sem pedidos): vendas = 0; estoque, alertas, déficit e valor iguais ao padrão. Com data inicial após a final: aviso "período inválido: data inicial após a final" e estoque visível (T/M) |
| RF-015 | O sistema deve oferecer um botão **"Limpar filtros"** | Could | Ao clicar, todos os filtros voltam ao padrão e os valores voltam aos da RF-001 a RF-008 (M) |

### 6.3. Visualizações

| ID | Requisito | Prioridade | Critério de aceitação |
| --- | --- | --- | --- |
| RF-016 | O sistema deve exibir a **tabela de prioridade de reposição** com posição, produto, categoria, fornecedor, contato, estoque, nível, razão estoque/nível, déficit, unidades vendidas, unidades em aberto e nível de alerta | Must | Ordem e valores: 1. Hanging Basket (0/10, Ruptura, déficit 10, 0 vendidas); 2. Tomato Seeds 'Roma' (5/40, Crítico, 35, 4); 3. Hand Cultivator (3/10, Crítico, 7, 2); 4. Pothos 'Golden' (8/12, Alerta, 4, 5); 5. Orchid Food (6/10, Alerta, 4, 2). Hand Cultivator mostra "sem e-mail cadastrado" no contato (T/M) |
| RF-017 | O sistema deve exibir **barras horizontais de estoque × nível de reposição** por produto, com cor pelo nível de alerta | Must | Cada produto aparece uma vez, com marcação do nível; os 5 produtos abaixo do nível se distinguem dos demais pela cor e pelo texto do nível (M) |
| RF-018 | O sistema deve exibir **barras do valor do estoque a custo por categoria** | Should | Houseplants 1.747,00; Seeds & Bulbs 664,50; Soil & Compost 599,00; Tools 448,50; Pots & Planters 401,00; Watering 351,00; Outdoor Decor 288,00; Fertilizer 264,00 (T) |
| RF-019 | O sistema deve exibir **barras de unidades vendidas por produto**, com cor pelo nível de alerta de estoque | Should | Sunflower Seeds (12) e Terracotta Pot 8in (9) lideram e aparecem como estoque adequado; Pothos 'Golden' (5) aparece em alerta (T/M) |
| RF-020 | O sistema deve exibir a **situação dos produtos ativos por categoria** (barras empilhadas) | Should | Produtos abaixo do nível: Fertilizer 1 de 2; Seeds & Bulbs 1 de 3; Tools 1 de 3; Pots & Planters 1 de 3; Houseplants 1 de 5; Soil & Compost, Watering e Outdoor Decor 0 (T) |
| RF-021 | O sistema deve exibir uma **dispersão de estoque ÷ nível × unidades vendidas** | Could | Os 5 produtos abaixo do nível ficam à esquerda da linha de 100%; ao desmarcar `processing` e `pending`, os pontos descem (M) |
| RF-022 | O sistema deve exibir **avisos de contexto**: "Estoque: posição atual", período e status aplicados às vendas, pedidos cancelados desconsiderados e registros inválidos descartados | Must | Aparece "1 pedido cancelado desconsiderado (US$ 22,00)". Para Hanging Basket, aparece o aviso de que venda zero com estoque zerado não indica falta de demanda (M) |
| RF-023 | O sistema deve tratar **filtros sem resultado** | Must | Com categoria Tools + fornecedor Terra Pots Co (sem produtos): cartões mostram 0 e US$ 0,00, gráficos e tabela somem e aparece "Nenhum produto atende aos filtros selecionados" (T) |

### 6.4. Entrega mínima

A Lista 2 exige ao menos dois indicadores, um filtro e uma tabela ou gráfico útil. Os requisitos **Must** ultrapassam esse mínimo. Se o prazo apertar, a entrega mínima coerente é: RF-001, RF-004, RF-009, RF-016 e RF-022.

## 7. Requisitos não funcionais

| ID | Categoria | Requisito | Critério de verificação |
| --- | --- | --- | --- |
| RNF-001 | Confiabilidade | Se faltar um CSV ou uma coluna obrigatória, o painel mostra mensagem dizendo qual arquivo ou coluna falta, e não números errados | Teste com arquivo e coluna ausentes |
| RNF-002 | Confiabilidade | Registros inválidos (ex.: item de pedido com produto inexistente, quantidade ou data não numérica) saem do cálculo e são registrados nos avisos de qualidade dos dados | Teste com registro inválido criado em memória |
| RNF-003 | Manutenibilidade | As regras de negócio podem ser verificadas por testes automatizados sobre um recorte dos CSVs, sem depender da interface | Execução dos testes |
| RNF-004 | Usabilidade | Um usuário não técnico entende a situação do estoque sem treinamento: cartões no topo, tabela de prioridade em destaque, textos em português | Avaliação com a pessoa que usa o painel |
| RNF-005 | Usabilidade | Cada nível de alerta aparece escrito, além da cor, e nenhum elemento usa a cor vermelha | Conferência visual no painel |

Desempenho e segurança não foram incluídos: a base tem 24 produtos e 48 itens de pedido, e o painel é local, de leitura e sem login.

## 8. Dados e integrações

- **Fontes de dados:** `products.csv`, `categories.csv`, `suppliers.csv`, `orders.csv`, `order_items.csv` e o dicionário `garden_shop_dicionario_dados.xlsx`. O `customers.csv` não é usado.
- **Entradas:** os CSVs originais, sem alteração.
  - `products`: `product_id`, `product_name`, `category_id`, `supplier_id`, `cost`, `quantity_on_hand`, `reorder_level`, `discontinued`.
  - `categories`: `category_id`, `category_name`.
  - `suppliers`: `supplier_id`, `supplier_name`, `contact_email`.
  - `orders`: `order_id`, `order_date`, `status`.
  - `order_items`: `order_id`, `product_id`, `quantity`, `unit_price`.
- **Relacionamentos:** `order_items.product_id → products.product_id`; `order_items.order_id → orders.order_id`; `products.category_id → categories.category_id`; `products.supplier_id → suppliers.supplier_id`.
- **Saídas:** o painel com cartões, filtros, gráficos e a tabela de prioridade.
- **Integrações:** nenhuma.
- **Dados sensíveis:** não há; os e-mails são de fornecedores.
- **Retenção e descarte:** não aplicável; os arquivos originais são preservados.
- **Formatos:** o dicionário descreve datas como DD/MM/AAAA e booleanos como TRUE/FALSE, mas os arquivos trazem AAAA-MM-DD e `true`/`false`. A leitura deve aceitar o formato real dos arquivos.

**Retrato da base (conferido nos CSVs):**

| Item | Valor |
| --- | --- |
| Produtos | 24 (23 ativos e 1 descontinuado: Bird Feeder) |
| Pedidos | 24, de 15/01/2024 a 14/06/2024: 17 `shipped`, 3 `processing`, 3 `pending` e 1 `cancelled` |
| Itens de pedido | 48; 86 unidades em pedidos não cancelados (65 enviadas, 12 em processamento, 9 pendentes) |
| Pedido cancelado | Pedido 17: 1 unidade de Pruning Shears, US$ 22,00 |
| Fornecedores | 6; 5 com produtos (RootWorks Supply não tem nenhum); Ironwood Tools e RootWorks Supply sem e-mail |
| Produtos sem venda | Hanging Basket (estoque zero) e Bird Feeder (descontinuado) |

## 9. Regras de negócio

- **RN-001:** itens de pedidos com status `cancelled` **nunca** contam como venda, unidade vendida ou pedido em aberto. O painel avisa quantos pedidos foram desconsiderados.
- **RN-002:** `shipped`, `processing` e `pending` contam como **venda efetiva** por padrão. `pending` e `processing` também são "em aberto". Justificativa: se só `shipped` contasse, um produto com vários pedidos ainda não enviados pareceria ter baixa demanda justamente quando o estoque está sendo consumido. O filtro RF-012 permite ver só as enviadas.
- **RN-003:** produtos com `discontinued = true` **não entram em alertas, na contagem de abaixo do nível, no déficit nem na prioridade de reposição**. Continuam contando no valor do estoque (capital imobilizado) e, com o filtro RF-013, aparecem rotulados "descontinuado — não repor".
- **RN-004:** produto ativo está **abaixo do nível** quando `quantity_on_hand < reorder_level`.
- **RN-005:** razão = estoque ÷ nível de reposição. **Ruptura:** estoque = 0. **Crítico:** razão < 50%. **Alerta:** 50% ≤ razão < 100%. **Observação:** 100% ≤ razão ≤ 150%. **Adequado:** razão > 150%. Os cortes são fixos na versão 1.0.
- **RN-006:** valor do estoque = Σ `quantity_on_hand` × `cost`, **a custo** e não a preço de venda, considerando todos os produtos (ativos e descontinuados).
- **RN-007:** déficit = `reorder_level − quantity_on_hand`, apenas para produtos ativos abaixo do nível. É a quantidade **mínima** para voltar ao nível, e não uma sugestão de compra, porque a base não informa estoque-alvo nem prazo de entrega.
- **RN-008:** ordem de prioridade: primeiro pelo nível de alerta (ruptura, crítico, alerta, observação, adequado); dentro de cada nível, por unidades vendidas (maior primeiro). O desempate de empates restantes será definido na SPEC (DP-005).
- **RN-009:** o **estoque é sempre a posição atual** (`quantity_on_hand`). Status do pedido e período filtram **apenas as vendas** (RF-005, RF-007, RF-019, RF-021 e o desempate da prioridade). Estoque, nível de alerta, déficit e valor não mudam com esses filtros.
- **RN-010:** venda zero com estoque zerado **não** significa ausência de demanda, pois sem estoque o produto não podia vender. O painel evita essa conclusão para itens em ruptura.
- **RN-011:** cada produto aparece **uma única vez**. As vendas são somadas por produto **antes** de serem relacionadas ao cadastro, para que estoque e valor nunca sejam multiplicados pelo número de itens de pedido.

## 10. Fluxos e exceções

### 10.1. Fluxo principal

Os dados são carregados e validados; o painel aplica os filtros padrão; calcula indicadores, gráficos e tabela; e o usuário refina com os filtros, que atualizam tudo ao mesmo tempo.

### 10.2. Fluxos alternativos

- **Filtros sem nenhum produto:** cartões mostram 0 (valor US$ 0,00), gráficos e tabela somem e aparece "Nenhum produto atende aos filtros selecionados" (RF-023).
- **Período sem pedidos ou com data inicial depois da final:** vendas ficam 0, com aviso do motivo; o estoque continua visível (RF-014).
- **Nenhum status de pedido selecionado:** vendas ficam 0, com aviso; o estoque continua visível (RF-012).
- **Produto sem nenhuma venda:** aparece com 0 unidades vendidas; se estiver em ruptura, mostra o aviso da RN-010.
- **Fornecedor sem e-mail:** a coluna Contato mostra "sem e-mail cadastrado", como alerta de cadastro a completar.
- **Produto descontinuado abaixo do nível:** só aparece com o filtro RF-013, rotulado "descontinuado — não repor", sem déficit.

### 10.3. Tratamento de erros

- **Arquivo CSV ausente:** mensagem informando qual arquivo falta; nenhum número é exibido (RNF-001).
- **Coluna obrigatória ausente:** mensagem informando arquivo e coluna (RNF-001).
- **Item de pedido com produto inexistente, ou valor inválido (data, quantidade, estoque não numérico):** o registro sai do cálculo e é registrado nos avisos de qualidade dos dados (RNF-002). Dados nunca são corrigidos silenciosamente.

## 11. Experiência e interface

- **Plataforma:** painel que roda localmente; a forma de execução depende da tecnologia (DP-001).
- **Referências visuais:** wireframes da Lista 1, simplificados para uma única página.
- **Acessibilidade:** semáforo com a mesma paleta em todo o painel: roxo (ruptura), âmbar (crítico), amarelo (alerta), azul (observação), verde (adequado) e cinza (descontinuado). Cada nível aparece também escrito. Sem vermelho.
- **Estados da interface:** carregando, com dados, vazio (filtro sem resultado), aviso (período inválido ou nenhum status) e erro (arquivo ou coluna ausente).
- **Compatibilidade:** execução local em navegador moderno ou ambiente definido na tecnologia escolhida (DP-001).
- **Nota fixa:** "Estoque: posição atual. O período e o status filtram apenas as vendas."

## 12. Riscos e dependências

| Risco ou dependência | Impacto | Mitigação |
| --- | --- | --- |
| Contar `cancelled` como venda | Alto | RN-001 e teste do RF-005 |
| Recomendar reposição de descontinuado | Alto | RN-003 e teste do RF-013 |
| Duplicar estoque ao juntar `products` e `order_items` | Alto | RN-011 e teste do RF-004 (Fiddle-Leaf Fig) |
| Interpretar o período das vendas como data do estoque | Médio | RN-009, nota fixa e teste do RF-014 |
| Ruptura lida como "produto sem demanda" | Médio | RN-010 e aviso do RF-022 |
| Dicionário diferente dos arquivos (datas e booleanos) | Médio | Leitura que aceita o formato real, verificada nos testes |
| Pedidos `pending` e `processing` podem já ter baixado o estoque (não se sabe) | Médio | "Em aberto" aparece separado e não é subtraído do estoque |
| Poucos dados (24 pedidos, muitos empates de vendas) | Médio | Vendas como critério secundário, sem conclusão de tendência |
| Prazo curto | Médio | Prioridades Must/Should/Could e entrega mínima da seção 6.4 |

## 13. Entregáveis

- Dashboard funcional em repositório GitHub, com os dados e os arquivos necessários para executá-lo.
- `PRD.md`, `SPEC.md` e `AGENTS.md`, mantidos também no repositório.
- Testes das regras de cálculo, com dois indicadores validados à mão sobre um recorte dos CSVs.
- Instruções de instalação, execução e teste (no `AGENTS.md`).
- Print legível do dashboard em execução, com indicadores, filtro e visualização.

## 14. Critérios de conclusão do produto

O produto estará pronto quando:

- Os requisitos obrigatórios (Must) tiverem sido implementados.
- Os critérios de aceitação da seção 6 tiverem sido verificados: os marcados com T por teste e os marcados com M no painel.
- Os testes pertinentes tiverem sido executados, incluindo cancelados, descontinuados, produto sem vendas, filtro sem resultado e duplicação de estoque.
- A documentação necessária estiver atualizada e coerente com o código.
- Os riscos críticos da seção 12 tiverem sido tratados.
- O procedimento de execução tiver sido validado.

## 15. Relação com os documentos técnicos

- **Especificação de referência:** `SPEC.md` (a elaborar; cada RF, RN e RNF deste documento será referenciado nela)
- **Instruções gerais para agentes:** `AGENTS.md` (a elaborar; inclui a abordagem de implementação)
- **Instruções para Claude Code:** `CLAUDE.md` (não exigido na Lista 2)

## 16. Decisões pendentes

| ID | Questão | Responsável | Status |
| --- | --- | --- | --- |
| DP-001 | Tecnologia do dashboard (por exemplo Python com Streamlit, ou HTML com JavaScript) | Júlia | Pendente |
| DP-002 | Abordagem de implementação (SDD, TDD ou combinação), a registrar no `AGENTS.md`. Proposta: combinação | Júlia | Pendente |
| DP-003 | Confirmar a simplificação de escopo em relação à Lista 1 (seção 5.2) e as prioridades Must/Should/Could | Júlia | Pendente |
| DP-004 | Confirmar que `shipped`, `processing` e `pending` contam como venda por padrão (RN-002), como na Lista 1 | Júlia | Proposta (vem da Lista 1) |
| DP-005 | Critério de desempate da prioridade quando nível de alerta e unidades vendidas empatam | Júlia | Pendente (definir na SPEC) |

## 17. Histórico de alterações

| Versão | Data | Alteração |
| --- | --- | --- |
| 1.0 | 2026-10-27 | Criação inicial, seguindo o template, com base na Lista 1 e nos CSVs |
