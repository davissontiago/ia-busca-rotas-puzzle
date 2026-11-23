"""
Implementação unificada dos algoritmos de busca:
BFS, DFS, Busca Gulosa e A*.
"""

from collections import deque
import heapq
import time


class ResultadoBusca:
    def __init__(self, caminho, custo, nos_expandidos, tempo, encontrou):
        self.caminho = caminho
        self.custo = custo
        self.nos_expandidos = nos_expandidos
        self.tempo = tempo
        self.encontrou = encontrou

    def __str__(self):
        if not self.encontrou:
            return "Solução não encontrada."
        return (
            f"Caminho: {' -> '.join(map(str, self.caminho))}\n"
            f"Custo: {self.custo}\n"
            f"Nos expandidos: {self.nos_expandidos}\n"
            f"Tempo: {self.tempo:.6f}s"
        )


def bfs(estado_inicial, objetivo, sucessores, custo_aresta=None):
    """Busca em Largura (Breadth-First Search) com fila FIFO."""
    inicio = time.time()
    nos_expandidos = 0

    if estado_inicial == objetivo:
        return ResultadoBusca([estado_inicial], 0, 0, time.time() - inicio, True)

    fronteira = deque()
    fronteira.append((estado_inicial, [estado_inicial], 0))
    visitados = {estado_inicial}

    while fronteira:
        estado, caminho, custo = fronteira.popleft()
        nos_expandidos += 1

        for vizinho, peso in sucessores(estado):
            if vizinho not in visitados:
                novo_custo = custo + (peso if custo_aresta is None else custo_aresta(estado, vizinho))
                novo_caminho = caminho + [vizinho]

                if vizinho == objetivo:
                    return ResultadoBusca(novo_caminho, novo_custo, nos_expandidos, time.time() - inicio, True)

                visitados.add(vizinho)
                fronteira.append((vizinho, novo_caminho, novo_custo))

    return ResultadoBusca([], 0, nos_expandidos, time.time() - inicio, False)


def dfs(estado_inicial, objetivo, sucessores, custo_aresta=None, limite=None):
    """Busca em Profundidade (Depth-First Search) com pilha LIFO e controle de visitados."""
    inicio = time.time()
    nos_expandidos = 0

    if estado_inicial == objetivo:
        return ResultadoBusca([estado_inicial], 0, 0, time.time() - inicio, True)

    fronteira = [(estado_inicial, [estado_inicial], 0)]
    visitados = {estado_inicial}

    while fronteira:
        estado, caminho, custo = fronteira.pop()
        nos_expandidos += 1

        if limite is not None and len(caminho) - 1 >= limite:
            continue

        for vizinho, peso in sucessores(estado):
            if vizinho not in visitados:
                novo_custo = custo + (peso if custo_aresta is None else custo_aresta(estado, vizinho))
                novo_caminho = caminho + [vizinho]

                if vizinho == objetivo:
                    return ResultadoBusca(novo_caminho, novo_custo, nos_expandidos, time.time() - inicio, True)

                visitados.add(vizinho)
                fronteira.append((vizinho, novo_caminho, novo_custo))

    return ResultadoBusca([], 0, nos_expandidos, time.time() - inicio, False)


def busca_gulosa(estado_inicial, objetivo, sucessores, heuristica):
    """Busca Gulosa (Greedy Best-First Search) com f(n) = h(n)."""
    inicio = time.time()
    nos_expandidos = 0
    contador = 0

    fronteira = []
    heapq.heappush(fronteira, (heuristica(estado_inicial), contador, estado_inicial, [estado_inicial], 0))
    contador += 1
    visitados = {estado_inicial}

    while fronteira:
        _, _, estado, caminho, custo = heapq.heappop(fronteira)
        nos_expandidos += 1

        if estado == objetivo:
            return ResultadoBusca(caminho, custo, nos_expandidos, time.time() - inicio, True)

        for vizinho, peso in sucessores(estado):
            if vizinho not in visitados:
                visitados.add(vizinho)
                novo_custo = custo + peso
                novo_caminho = caminho + [vizinho]
                h = heuristica(vizinho)
                heapq.heappush(fronteira, (h, contador, vizinho, novo_caminho, novo_custo))
                contador += 1

    return ResultadoBusca([], 0, nos_expandidos, time.time() - inicio, False)


def busca_a_estrela(estado_inicial, objetivo, sucessores, heuristica):
    """Busca A* com f(n) = g(n) + h(n)."""
    inicio = time.time()
    nos_expandidos = 0
    contador = 0

    g_custos = {estado_inicial: 0}
    fronteira = []
    heapq.heappush(fronteira, (heuristica(estado_inicial), contador, estado_inicial, [estado_inicial]))
    contador += 1

    while fronteira:
        f, _, estado, caminho = heapq.heappop(fronteira)
        nos_expandidos += 1
        g_atual = g_custos[estado]

        if estado == objetivo:
            return ResultadoBusca(caminho, g_atual, nos_expandidos, time.time() - inicio, True)

        for vizinho, peso in sucessores(estado):
            novo_g = g_atual + peso

            if vizinho not in g_custos or novo_g < g_custos[vizinho]:
                g_custos[vizinho] = novo_g
                h = heuristica(vizinho)
                f_novo = novo_g + h
                novo_caminho = caminho + [vizinho]
                heapq.heappush(fronteira, (f_novo, contador, vizinho, novo_caminho))
                contador += 1

    return ResultadoBusca([], 0, nos_expandidos, time.time() - inicio, False)
