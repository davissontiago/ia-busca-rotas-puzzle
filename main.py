# -*- coding: utf-8 -*-
"""
Script principal: executa todos os algoritmos nos dois dominios
e exibe os resultados comparativos.

IFPI - Licenciatura em Computacao
Disciplina: Inteligencia Artificial
Assunto: Resolucao de problemas por busca
"""

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from algoritmos_busca import bfs, dfs, busca_gulosa, busca_a_estrela
from dominio_cidades import (
    sucessores_cidades, heuristica_parnaiba, ORIGEM, DESTINO
)
from dominio_puzzle import (
    sucessores_puzzle, h1_pecas_fora, h2_manhattan,
    OBJETIVO, ESTADOS_INICIAIS, estado_para_str, eh_soluvel
)


def separador(titulo):
    print(f"\n{'='*70}")
    print(f"  {titulo}")
    print(f"{'='*70}")


def linha_tabela(cols, larguras):
    return "| " + " | ".join(str(c).ljust(w) for c, w in zip(cols, larguras)) + " |"


# ==========================================================================
#  DOMINIO 1: ROTEAMENTO RODOVIARIO NO PIAUI
# ==========================================================================

def executar_cidades():
    separador("DOMINIO 1: ROTEAMENTO RODOVIARIO NO PIAUI")
    print(f"Origem: {ORIGEM}  -->  Destino: {DESTINO}\n")

    resultados = {}

    # BFS
    print("-" * 50)
    print("[BFS] Busca em Largura")
    r = bfs(ORIGEM, DESTINO, sucessores_cidades)
    print(r)
    resultados["BFS"] = r

    # DFS
    print("\n" + "-" * 50)
    print("[DFS] Busca em Profundidade")
    r = dfs(ORIGEM, DESTINO, sucessores_cidades)
    print(r)
    resultados["DFS"] = r

    # Gulosa
    print("\n" + "-" * 50)
    print("[GULOSA] Busca Gulosa")
    r = busca_gulosa(ORIGEM, DESTINO, sucessores_cidades, heuristica_parnaiba)
    print(r)
    resultados["Gulosa"] = r

    # A*
    print("\n" + "-" * 50)
    print("[A*] Busca A*")
    r = busca_a_estrela(ORIGEM, DESTINO, sucessores_cidades, heuristica_parnaiba)
    print(r)
    resultados["A*"] = r

    # Tabela comparativa
    separador("TABELA COMPARATIVA - CIDADES DO PIAUI")
    larguras = [10, 55, 12, 15, 12]
    cabecalho = ["Algoritmo", "Rota", "Custo (km)", "Nos Expandidos", "Tempo (s)"]
    print(linha_tabela(cabecalho, larguras))
    print("|" + "|".join("-" * (w + 2) for w in larguras) + "|")

    for nome, r in resultados.items():
        rota = " -> ".join(r.caminho) if r.encontrou else "Nao encontrada"
        custo = str(r.custo) if r.encontrou else "-"
        print(linha_tabela([nome, rota[:55], custo, r.nos_expandidos, f"{r.tempo:.6f}"], larguras))


# ==========================================================================
#  DOMINIO 2: JOGO DOS 8 NUMEROS (8-PUZZLE)
# ==========================================================================

def executar_puzzle():
    separador("DOMINIO 2: JOGO DOS 8 NUMEROS (8-PUZZLE)")
    print(f"Estado objetivo:\n{estado_para_str(OBJETIVO)}\n")

    todos_resultados = []

    for d, estado_inicial in sorted(ESTADOS_INICIAIS.items()):
        separador(f"8-PUZZLE - Profundidade aproximada d ~ {d}")
        print(f"Estado inicial:\n{estado_para_str(estado_inicial)}")
        print(f"Solucionavel: {eh_soluvel(estado_inicial)}\n")

        resultados_d = {}

        # BFS
        print("-" * 50)
        print("[BFS] Busca em Largura")
        r = bfs(estado_inicial, OBJETIVO, sucessores_puzzle)
        print(f"Movimentos: {r.custo}, Nos expandidos: {r.nos_expandidos}, Tempo: {r.tempo:.6f}s")
        resultados_d["BFS"] = r

        # DFS (com limite para evitar explosao)
        print("\n" + "-" * 50)
        print("[DFS] Busca em Profundidade")
        limite_dfs = max(30, d * 3)
        r = dfs(estado_inicial, OBJETIVO, sucessores_puzzle, limite=limite_dfs)
        if r.encontrou:
            print(f"Movimentos: {r.custo}, Nos expandidos: {r.nos_expandidos}, Tempo: {r.tempo:.6f}s")
        else:
            print(f"Nao encontrou solucao (limite={limite_dfs}), Nos expandidos: {r.nos_expandidos}, Tempo: {r.tempo:.6f}s")
        resultados_d["DFS"] = r

        # Gulosa com h1
        print("\n" + "-" * 50)
        print("[GULOSA h1] Busca Gulosa (pecas fora do lugar)")
        r = busca_gulosa(estado_inicial, OBJETIVO, sucessores_puzzle, h1_pecas_fora)
        print(f"Movimentos: {r.custo}, Nos expandidos: {r.nos_expandidos}, Tempo: {r.tempo:.6f}s")
        resultados_d["Gulosa h1"] = r

        # Gulosa com h2
        print("\n" + "-" * 50)
        print("[GULOSA h2] Busca Gulosa (Manhattan)")
        r = busca_gulosa(estado_inicial, OBJETIVO, sucessores_puzzle, h2_manhattan)
        print(f"Movimentos: {r.custo}, Nos expandidos: {r.nos_expandidos}, Tempo: {r.tempo:.6f}s")
        resultados_d["Gulosa h2"] = r

        # A* com h1
        print("\n" + "-" * 50)
        print("[A* h1] Busca A* (pecas fora do lugar)")
        r = busca_a_estrela(estado_inicial, OBJETIVO, sucessores_puzzle, h1_pecas_fora)
        print(f"Movimentos: {r.custo}, Nos expandidos: {r.nos_expandidos}, Tempo: {r.tempo:.6f}s")
        resultados_d["A* h1"] = r

        # A* com h2
        print("\n" + "-" * 50)
        print("[A* h2] Busca A* (Manhattan)")
        r = busca_a_estrela(estado_inicial, OBJETIVO, sucessores_puzzle, h2_manhattan)
        print(f"Movimentos: {r.custo}, Nos expandidos: {r.nos_expandidos}, Tempo: {r.tempo:.6f}s")
        resultados_d["A* h2"] = r

        todos_resultados.append((d, resultados_d))

    # Tabela comparativa geral do 8-Puzzle
    separador("TABELA COMPARATIVA - 8-PUZZLE")
    larguras = [12, 5, 12, 15, 12]
    cabecalho = ["Algoritmo", "d", "Movimentos", "Nos Expandidos", "Tempo (s)"]
    print(linha_tabela(cabecalho, larguras))
    print("|" + "|".join("-" * (w + 2) for w in larguras) + "|")

    for d, resultados_d in todos_resultados:
        for nome, r in resultados_d.items():
            movs = str(r.custo) if r.encontrou else "N/A"
            nos = str(r.nos_expandidos)
            tempo = f"{r.tempo:.6f}"
            print(linha_tabela([nome, d, movs, nos, tempo], larguras))
        print("|" + "|".join("-" * (w + 2) for w in larguras) + "|")

    # Comparacao A* h1 vs h2
    separador("COMPARACAO A* : h1 (pecas fora) vs h2 (Manhattan)")
    larguras_comp = [5, 15, 15, 15, 15]
    cabecalho_comp = ["d", "Nos A* h1", "Nos A* h2", "Tempo A* h1", "Tempo A* h2"]
    print(linha_tabela(cabecalho_comp, larguras_comp))
    print("|" + "|".join("-" * (w + 2) for w in larguras_comp) + "|")

    for d, resultados_d in todos_resultados:
        r1 = resultados_d["A* h1"]
        r2 = resultados_d["A* h2"]
        print(linha_tabela([
            d,
            r1.nos_expandidos,
            r2.nos_expandidos,
            f"{r1.tempo:.6f}",
            f"{r2.tempo:.6f}"
        ], larguras_comp))


# ==========================================================================
#  EXECUCAO PRINCIPAL
# ==========================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  RESOLUCAO DE PROBLEMAS POR BUSCA - INTELIGENCIA ARTIFICIAL")
    print("  IFPI - Campus Teresina Zona Sul")
    print("=" * 70)

    executar_cidades()
    executar_puzzle()

    separador("ANALISE FINAL")
    print("""
COMPLETUDE:
- BFS: Completa (encontra solucao se existir, para grafos finitos).
- DFS: Completa com controle de visitados em grafos finitos (pode nao
  terminar em espacos infinitos sem limite de profundidade).
- Gulosa: Incompleta (pode entrar em ciclos sem controle de visitados;
  com visitados, completa em espacos finitos).
- A*: Completa (com heuristica admissivel e espaco finito).

OTIMALIDADE:
- BFS: Otima quando todos os custos de aresta sao iguais (8-Puzzle).
  No problema de cidades (custos variaveis), NAO garante otimalidade.
- DFS: NAO e otima - pode encontrar caminhos subotimos.
- Gulosa: NAO e otima - ignora o custo acumulado g(n).
- A*: OTIMA quando a heuristica h(n) e admissivel (nunca superestima).
  As distancias em linha reta sao admissiveis para cidades, e ambas
  h1 e h2 sao admissiveis para o 8-Puzzle.

COMPARACAO h1 vs h2 NO A*:
- h2 (Manhattan) domina h1 (pecas fora do lugar): h2(n) >= h1(n) para
  todo estado n. Isso significa que h2 e mais informativa.
- Como consequencia, A* com h2 expande significativamente MENOS nos
  que A* com h1, mantendo a mesma solucao otima.
- A diferenca se torna mais pronunciada em estados com maior
  profundidade de solucao.
""")
