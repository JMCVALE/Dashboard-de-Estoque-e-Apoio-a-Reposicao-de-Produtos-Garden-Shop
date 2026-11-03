"""Script utilitário para gerar o arquivo index.html usando Stlite (WebAssembly).

Empacota app.py, src/data_engine.py e todos os CSVs para permitir que o Dashboard
seja executado 100% no navegador e publicado no GitHub Pages sem servidor Python.
"""

import json
from pathlib import Path


def generate_index_html():
    files_dict = {}

    # Adicionar código-fonte
    files_dict["app.py"] = Path("app.py").read_text(encoding="utf-8")
    files_dict["src/__init__.py"] = Path("src/__init__.py").read_text(encoding="utf-8")
    files_dict["src/data_engine.py"] = Path("src/data_engine.py").read_text(encoding="utf-8")

    # Adicionar bases CSV tanto em "Garden Shop - bases/" quanto na raiz para garantia
    base_dir = Path("Garden Shop - bases")
    for csv_file in base_dir.glob("*.csv"):
        content = csv_file.read_text(encoding="utf-8")
        files_dict[f"Garden Shop - bases/{csv_file.name}"] = content
        files_dict[csv_file.name] = content

    files_json = json.dumps(files_dict, ensure_ascii=False)

    html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <title>Garden Shop — Dashboard de Estoque e Reposição</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.73.0/build/stlite.css" />
    <style>
      body {{
        margin: 0;
        padding: 0;
        background-color: #f9fafb;
      }}
      #root {{
        height: 100vh;
      }}
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.73.0/build/stlite.js"></script>
    <script>
      stlite.mount({{
        requirements: ["pandas", "altair"],
        entrypoint: "app.py",
        files: {files_json}
      }}, document.getElementById("root"));
    </script>
  </body>
</html>
"""
    Path("index.html").write_text(html_template, encoding="utf-8")
    print(f"index.html criado com sucesso ({len(html_template)} bytes).")


if __name__ == "__main__":
    generate_index_html()
