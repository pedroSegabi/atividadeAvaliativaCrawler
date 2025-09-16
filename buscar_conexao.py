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
    undir = {u: set(vs) for u, vs in grafo.items()}
    for u, vs in grafo.items():
        for v in vs:
            undir.setdefault(v, set()).add(u)
    grafo = undir
    nomes = sorted(grafo.keys())
    total = len(nomes)

    def bfs_from_source(g, src):
        from collections import deque
        q = deque([src])
        parent = {src: None}
        while q:
            u = q.popleft()
            for v in g.get(u, ()):  # g[u] normalmente
                if v not in parent:
                    parent[v] = u
                    q.append(v)
        return parent

    if '--longest' in sys.argv:
        print('Calculando par com maior menor-caminho ("--longest")... isso pode demorar alguns segundos')
        norm = lambda s: ''.join(ch for ch in s if ch.isalnum()).lower()
        best = (-1, None, None, None)
        for i, a in enumerate(nomes):
            parent = bfs_from_source(grafo, a)
            for b in nomes:
                if a == b:
                    continue
                if b not in parent:
                    continue
                path = []
                cur = b
                while cur is not None:
                    path.append(cur)
                    cur = parent.get(cur)
                path = list(reversed(path))
                grau = len(path) - 1
                if grau == 1 and norm(path[0]) == norm(path[1]):
                    continue
                if grau > best[0]:
                    best = (grau, a, b, path)
        if best[0] >= 0:
            grau, a, b, path = best
            print('Encontrado par de maior distancia:')
            print(f'Origem: {a.title()}')
            print(f'Destino: {b.title()}')
            print(f'Grau: {grau}')
            print(' -> '.join([c.title() for c in path]))
        else:
            print('Nenhum par conectado encontrado.')
        return

    if len(sys.argv) >= 3:
        nome1 = sanitize_title(sys.argv[1])
        nome2 = sanitize_title(sys.argv[2])
        print(f"Buscando distância entre '{sys.argv[1]}' e '{sys.argv[2]}' em um grafo NÃO-DIRECIONADO...")
        caminho = bfs_caminho(grafo, nome1, nome2)
        if caminho:
            grau = len(caminho) - 1
            print(f"✅ Grau entre '{sys.argv[1]}' e '{sys.argv[2]}': {grau}")
            print(" -> ".join([c.title() for c in caminho]))
        else:
            print(f"❌ Não foi encontrado caminho entre '{sys.argv[1]}' e '{sys.argv[2]}'.")
        return

    min_degree = 2
    if len(sys.argv) == 2:
        try:
            min_degree = int(sys.argv[1])
        except ValueError:
            pass

    print(f"Procurando primeira conexao com grau >= {min_degree} em um grafo NÃO-DIRECIONADO com {total} pessoas...")
    norm = lambda s: ''.join(ch for ch in s if ch.isalnum()).lower()
    for i, a in enumerate(nomes):
        for b in nomes:
            if a == b:
                continue
            caminho = bfs_caminho(grafo, a, b)
            if not caminho:
                continue
            grau = len(caminho) - 1
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
