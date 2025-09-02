from utils import carregar_grafo, sanitize_title
from collections import deque


def bfs_caminho(grafo, origem, destino):
    if origem not in grafo or destino not in grafo:
        return None
    fila = deque([(origem, [origem])])
    visitados = set([origem])
    while fila:
        atual, caminho = fila.popleft()
        if atual == destino:
            return caminho
        for viz in grafo[atual]:
            if viz not in visitados:
                visitados.add(viz)
                fila.append((viz, caminho + [viz]))
    return None


def main():
    import sys
    grafo, _ = carregar_grafo()
    nomes = sorted(grafo.keys())
    total = len(nomes)
    # aceitar argumento opcional de linha de comando: min_degree
    min_degree = 2
    if len(sys.argv) > 1:
        try:
            min_degree = int(sys.argv[1])
        except ValueError:
            pass

    print(f"Procurando primeira conexao com grau >= {min_degree} em um grafo com {total} pessoas...")
    norm = lambda s: ''.join(ch for ch in s if ch.isalnum()).lower()
    for i, a in enumerate(nomes):
        for b in nomes:
            if a == b:
                continue
            caminho = bfs_caminho(grafo, a, b)
            if not caminho:
                continue
            grau = len(caminho) - 1
            # pular conexões triviais que são variantes do mesmo nome
            if grau == 1 and norm(caminho[0]) == norm(caminho[1]):
                continue
            if grau >= min_degree:
                print("Encontrado par conectado:")
                print(f"Origem: {a.title()}")
                print(f"Destino: {b.title()}")
                print(f"Grau: {grau}")
                print(" -> ".join([c.title() for c in caminho]))
                return
    print(f"Nenhuma conexao encontrada com grau >= {min_degree} entre pares do grafo.")

if __name__ == '__main__':
    main()
