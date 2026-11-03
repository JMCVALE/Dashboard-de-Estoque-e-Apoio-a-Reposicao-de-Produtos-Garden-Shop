# AGENTS.md — Instruções para agentes de IA

> **Responsável pelo projeto:** Júlia Maria de Carvalho Vale  
> **Disciplina:** Inteligência Artificial Aplicada / Gestão de Dados e Decisão  
> **Projeto:** Dashboard de Estoque e Apoio à Reposição — Garden Shop

## 1. Objetivo

Este documento define as diretrizes, a abordagem de trabalho, a arquitetura do projeto e os comandos de verificação que qualquer agente de IA ou desenvolvedor deve seguir ao manter, implementar e testar o código deste repositório.

## 2. Hierarquia de referência

Antes de executar qualquer modificação no repositório:
1. Consulte este arquivo (`AGENTS.md`) para entender o processo de trabalho e comandos autorizados;
2. Consulte o `PRD.md` para compreender o problema de negócio, os objetivos e as necessidades dos usuários da Garden Shop;
3. Consulte a `SPEC.md` como fonte inequívoca da especificação técnica, fórmulas matemáticas e contratos de dados;
4. **Regra de ouro sobre templates:** A pasta `templates/` contém os modelos originais fornecidos pela disciplina e **nunca deve ser sobrescrita nem modificada**.

## 3. Abordagem de implementação: Combinação (SDD + TDD)

A abordagem adotada neste projeto combina **Spec-Driven Development (SDD)** com **Test-Driven Development (TDD)**:
* **SDD (Spec-Driven):** O `PRD.md` e a `SPEC.md` orientam todo o escopo e os critérios de aceitação. Nenhuma regra é codificada sem estar documentada na especificação técnica.
* **TDD (Test-Driven):** As regras contábeis e de classificação de estoque (descarte de pedidos cancelados, valor total de US$ 4.763,00, classificação de criticidade e cálculo de déficit) são traduzidas em testes unitários automatizados com `pytest` antes ou em conjunto com a implementação do código final, garantindo 100% de precisão nos cálculos.

## 4. Estrutura do projeto

```text
LISTA 2/
├── Garden Shop - bases/            # CSVs originais da disciplina (somente leitura)
│   ├── categories.csv
│   ├── customers.csv
│   ├── orders.csv
│   ├── order_items.csv
│   ├── products.csv
│   └── suppliers.csv
├── templates/                      # Templates originais (NÃO MODIFICAR)
├── src/                            # Código-fonte da aplicação
│   ├── __init__.py
│   └── data_engine.py              # Módulo de lógica de negócio e processamento de dados
├── tests/                          # Suíte de testes automatizados
│   ├── __init__.py
│   └── test_data_engine.py         # Testes unitários com pytest
├── app.py                          # Aplicação do Dashboard em Streamlit (execução local)
├── index.html                      # Versão web independente para GitHub Pages (Stlite)
├── requirements.txt                # Dependências Python
├── PRD.md                          # Documento de Requisitos do Produto
├── SPEC.md                         # Especificação Técnica de Software
└── AGENTS.md                       # Diretrizes para agentes de IA e desenvolvedores
```

## 5. Padrões específicos do projeto

- **Linguagem principal:** Python 3.10+
- **Bibliotecas essenciais:** `streamlit`, `pandas`, `pytest`
- **Ambiente web estático:** Stlite (distribuição WebAssembly para publicação direta no GitHub Pages sem necessidade de servidor Python dedicado)
- **Cuidados estritos com os dados:**
  - Preservar os arquivos CSV na pasta `Garden Shop - bases/` como somente leitura.
  - Nunca criar dados artificiais que conflitem com o dicionário de dados.
  - Sempre sanitizar valores nulos de fornecedores (como e-mails ausentes) e produtos sem vendas com valores padrão seguros (`"Não informado"`, `0`).

## 6. Comandos de referência

Os comandos abaixo devem ser executados no terminal PowerShell ou Bash na raiz do projeto:

| Finalidade | Comando | Status de verificação |
| :--- | :--- | :--- |
| Instalação de dependências | `pip install -r requirements.txt` | Verificado |
| Execução dos testes automatizados | `pytest tests/ -v` | Verificado |
| Execução local do dashboard Streamlit | `streamlit run app.py` | Verificado |
| Servidor local de teste do GitHub Pages | `python -m http.server 8000` | Verificado |

## 7. Critérios de qualidade e conclusão

Uma entrega ou alteração só é considerada válida quando:
1. Todos os testes em `tests/test_data_engine.py` passarem com sucesso (0 falhas);
2. O valor patrimonial do estoque reportado for exatamente **US$ 4.763,00**;
3. O volume de unidades vendidas em pedidos válidos for rigorosamente **86 unidades**;
4. Os 5 produtos que exigem reposição forem devidamente destacados com seus respectivos déficits;
5. O dashboard carregar sem exceções tanto no ambiente Streamlit local quanto no navegador via GitHub Pages.
