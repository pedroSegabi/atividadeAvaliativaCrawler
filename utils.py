import os
import re
from bs4 import BeautifulSoup

DATA_DIR = "dados_html"

def sanitize_title(title: str) -> str:
    """Normaliza título (para comparação entre nomes de pessoas)."""
    # substituir underscores por espaços, colapsar espaços e lowercase
    title = title.replace("_", " ")
    return re.sub(r"\s+", " ", title.strip()).lower()

def salvar_pagina(titulo, html):
    """Salva HTML no diretório de dados."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    path = os.path.join(DATA_DIR, f"{titulo}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

def carregar_grafo():
    """Constrói grafo a partir das páginas salvas em dados_html/"""
    grafo = {}
    titulo_para_arquivo = {}

    # Mapeia arquivos -> nomes de pessoas
    for fname in os.listdir(DATA_DIR):
        if not fname.endswith(".html"):
            continue
        titulo = fname[:-5]
        titulo_normalizado = sanitize_title(titulo)
        titulo_para_arquivo[titulo_normalizado] = fname
        grafo[titulo_normalizado] = set()

    # Extrai links
    for pessoa, fname in titulo_para_arquivo.items():
        path = os.path.join(DATA_DIR, fname)
        with open(path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/wiki/"):
                destino = href.split("/wiki/")[1]
                destino = destino.replace("_", " ")
                # remover sufixos parentéticos para normalizar (ex: 'Nome (cantor)' -> 'Nome')
                destino_sem_paren = re.sub(r"\s*\(.*\)$", "", destino).strip()
                destino_normalizado = sanitize_title(destino_sem_paren)
                if destino_normalizado in grafo and destino_normalizado != pessoa:
                    grafo[pessoa].add(destino_normalizado)

    return grafo, titulo_para_arquivo
