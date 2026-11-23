"""
Domínio 2: Jogo dos 8 Números (8-Puzzle)
Grade 3x3 com peças 1-8 e célula vazia (0).

Estado representado como tupla de 9 elementos (leitura linha a linha).
Exemplo: (1,2,3,4,5,6,7,8,0) = estado objetivo.
"""

import random

OBJETIVO = (1, 2, 3, 4, 5, 6, 7, 8, 0)

MOVIMENTOS = {
    0: [1, 3],
    1: [0, 2, 4],
    2: [1, 5],
    3: [0, 4, 6],
    4: [1, 3, 5, 7],
    5: [2, 4, 8],
    6: [3, 7],
    7: [4, 6, 8],
    8: [5, 7],
}


def sucessores_puzzle(estado):
    """Gera os estados sucessores movendo a célula vazia. Retorna (novo_estado, custo=1)."""
    pos_vazio = estado.index(0)
    resultado = []
    for destino in MOVIMENTOS[pos_vazio]:
        novo = list(estado)
        novo[pos_vazio], novo[destino] = novo[destino], novo[pos_vazio]
        resultado.append((tuple(novo), 1))
    return resultado


def h1_pecas_fora(estado):
    """h1: Quantidade de peças fora do lugar (Misplaced Tiles). Não conta o 0."""
    return sum(1 for i in range(9) if estado[i] != 0 and estado[i] != OBJETIVO[i])


def h2_manhattan(estado):
    """h2: Soma das distâncias de Manhattan de cada peça até sua posição objetivo."""
    distancia = 0
    for i in range(9):
        if estado[i] != 0:
            valor = estado[i]
            pos_objetivo = OBJETIVO.index(valor)
            linha_atual, col_atual = divmod(i, 3)
            linha_obj, col_obj = divmod(pos_objetivo, 3)
            distancia += abs(linha_atual - linha_obj) + abs(col_atual - col_obj)
    return distancia


def estado_para_str(estado):
    """Representação visual do tabuleiro 3x3."""
    linhas = []
    for i in range(0, 9, 3):
        linhas.append(" ".join(str(x) if x != 0 else "_" for x in estado[i:i+3]))
    return "\n".join(linhas)


def eh_soluvel(estado):
    """Verifica se o estado é solucionável (número par de inversões)."""
    lista = [x for x in estado if x != 0]
    inversoes = 0
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] > lista[j]:
                inversoes += 1
    return inversoes % 2 == 0


def gerar_estado_a_profundidade(d):
    """
    Gera um estado inicial fazendo exatamente d movimentos aleatórios
    a partir do estado objetivo, garantindo profundidade de solução aproximada d.
    """
    estado = list(OBJETIVO)
    anterior = -1
    for _ in range(d):
        pos_vazio = estado.index(0)
        vizinhos = [v for v in MOVIMENTOS[pos_vazio] if v != anterior]
        destino = random.choice(vizinhos)
        anterior = pos_vazio
        estado[pos_vazio], estado[destino] = estado[destino], estado[pos_vazio]
    return tuple(estado)


# Estados iniciais pre-definidos para reprodutibilidade
# Profundidade otima confirmada via A* com h2 (Manhattan)
ESTADOS_INICIAIS = {
    5:  (2, 0, 3, 1, 5, 6, 4, 7, 8),  # solucao otima = 5 movimentos
    10: (0, 1, 2, 4, 5, 8, 7, 6, 3),  # solucao otima = 10 movimentos
    15: (3, 4, 2, 0, 1, 6, 5, 7, 8),  # solucao otima = 15 movimentos
}
