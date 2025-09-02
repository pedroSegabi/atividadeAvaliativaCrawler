#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tarefa 2 – 6 Graus de Separação
--------------------------------
- Constrói um grafo a partir das páginas de pessoas coletadas.
- Usa BFS para encontrar menor caminho entre duas pessoas.
"""

import sys
import collections
import difflib
import argparse
from utils import sanitize_title, carregar_grafo

def bfs_caminho(grafo, origem, destino):
    if origem not in grafo or destino not in grafo:
        return None

    fila = collections.deque([(origem, [origem])])
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
    parser = argparse.ArgumentParser(description="Encontra grau de separação entre duas pessoas nos HTMLs coletados.")
    parser.add_argument('pessoa1', help='Nome da pessoa origem (entre aspas se necessário)')
    parser.add_argument('pessoa2', help='Nome da pessoa destino (entre aspas se necessário)')
    parser.add_argument('--undirected', action='store_true', help='Tratar o grafo como não-direcionado (arestas bidirecionais).\n(Nota: o enunciado pede arestas dirigidas; use esta flag apenas para análise alternativa)')
    args = parser.parse_args()

    pessoa1 = sanitize_title(args.pessoa1)
    pessoa2 = sanitize_title(args.pessoa2)

    print("🔄 Construindo grafo a partir dos HTMLs coletados...")
    grafo, _ = carregar_grafo()
    print(f"Grafo carregado com {len(grafo)} pessoas.")
    # Verifica existência das pessoas no grafo e sugere nomes parecidos se necessário
    faltando = [p for p in (pessoa1, pessoa2) if p not in grafo]
    if faltando:
        for f in faltando:
            print(f"❌ Nome não encontrado no conjunto de HTMLs: \"{f}\"")
            candidatos = difflib.get_close_matches(f, grafo.keys(), n=5, cutoff=0.6)
            if candidatos:
                print("  Sugestões próximas:")
                for c in candidatos:
                    print(f"   - {c.title()}")
            else:
                print("  (Sem sugestões próximas)")
        sys.exit(1)

    # Por padrão usamos grafo dirigido — isto corresponde ao enunciado da atividade.
    if args.undirected:
        # construir versão não-direcionada do grafo
        undir = {u: set(vs) for u, vs in grafo.items()}
        for u, vs in grafo.items():
            for v in vs:
                undir.setdefault(v, set()).add(u)
        caminho = bfs_caminho(undir, pessoa1, pessoa2)
        modo = 'não-direcionado'
    else:
        caminho = bfs_caminho(grafo, pessoa1, pessoa2)
        modo = 'direcionado'

    if caminho:
        print(f"✅ Grau de separação ({modo}) entre \"{args.pessoa1}\" e \"{args.pessoa2}\": {len(caminho)-1}")
        print(" → ".join([c.title() for c in caminho]))
    else:
        print(f"❌ Não foi encontrado caminho ({modo}) entre \"{args.pessoa1}\" e \"{args.pessoa2}\".")

if __name__ == "__main__":
    main()
