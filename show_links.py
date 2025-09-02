from utils import carregar_grafo, sanitize_title
from bs4 import BeautifulSoup
import os
import re

DATA_DIR = "dados_html"

# caminho conhecido (normalizado)
path = ["categoriapessoas vivas", "jason abalos", "1985"]

def find_anchor_block(soup, target_normalized):
    """Procura uma âncora cujo destino normalizado corresponda a target_normalized.
    Retorna o elemento âncora encontrado e um bloco pai relevante (p, li, div).
    """
    for a in soup.find_all('a', href=True):
        href = a['href']
        if not href.startswith('/wiki/'):
            continue
        destino = href.split('/wiki/')[1]
        destino = destino.replace('_', ' ')
        destino_sem_paren = re.sub(r"\s*\(.*\)$", "", destino).strip()
        destino_normalizado = sanitize_title(destino_sem_paren)
        if destino_normalizado == target_normalized:
            # tentar pegar um bloco pai útil
            parent = a.find_parent(['p', 'li', 'div'])
            return a, parent
    return None, None


def show_for_path(path):
    grafo, titulo_para_arquivo = carregar_grafo()
    for i in range(len(path)-1):
        src = path[i]
        dst = path[i+1]
        fname = titulo_para_arquivo.get(src)
        if not fname:
            print(f"Arquivo para '{src}' não encontrado.")
            continue
        path_file = os.path.join(DATA_DIR, fname)
        with open(path_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        a, block = find_anchor_block(soup, dst)
        display_title = fname[:-5]
        print('\n' + '='*80)
        print(f"Arquivo: {fname} (orig. título: {display_title})")
        if a:
            print(f"Link encontrado para: {dst.title()}")
            print("Anchor tag:")
            print(str(a))
            if block:
                text = block.get_text('\n', strip=True)
                print('\nTrecho do bloco pai (texto):')
                print(text[:600])
            else:
                print('\n(Bloco pai não encontrado)')
        else:
            print(f"Link para {dst} não encontrado dentro de {fname}.")

if __name__ == '__main__':
    show_for_path(path)
