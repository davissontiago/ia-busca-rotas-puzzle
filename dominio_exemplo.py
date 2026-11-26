# -*- coding: utf-8 -*-
"""
Cenario didatico projetado para evidenciar as diferencas entre os algoritmos.

- Gulosa: enganada pelo "Atalho" (h baixo, custo alto via Serra)
- A*: encontra o caminho otimo pela Rodovia
- DFS: pode se perder em caminhos profundos sem saida (Trilha->Caverna->Ruina)
- BFS: explora nivel por nivel, expande muitos nos mas nao se perde

Grafo:
                      Floresta (beco sem saida)
                     /
  Inicio -- Atalho -- Serra -- Destino       (custo: 2+15+2 = 19, armadilha)
    |
    +-- Rodovia -- Planicie -- Ponte -- Destino  (custo: 5+3+2+1 = 11, otimo)
    |         \
    |          Desvio -- Destino              (custo: 5+4+12 = 21)
    |
    +-- Trilha -- Caverna -- Ruina            (beco sem saida, armadilha DFS)
                      \
                       Mina -- Poco           (beco sem saida profundo)
"""

ESTRADAS_EXEMPLO = {
    "Inicio":    [("Atalho", 2), ("Rodovia", 5), ("Trilha", 3)],
    "Atalho":    [("Inicio", 2), ("Serra", 15), ("Floresta", 6)],
    "Serra":     [("Atalho", 15), ("Destino", 2)],
    "Floresta":  [("Atalho", 6)],
    "Rodovia":   [("Inicio", 5), ("Planicie", 3), ("Desvio", 4)],
    "Planicie":  [("Rodovia", 3), ("Ponte", 2)],
    "Ponte":     [("Planicie", 2), ("Destino", 1)],
    "Desvio":    [("Rodovia", 4), ("Destino", 12)],
    "Trilha":    [("Inicio", 3), ("Caverna", 4)],
    "Caverna":   [("Trilha", 4), ("Ruina", 5), ("Mina", 3)],
    "Ruina":     [("Caverna", 5)],
    "Mina":      [("Caverna", 3), ("Poco", 2)],
    "Poco":      [("Mina", 2)],
    "Destino":   [("Serra", 2), ("Ponte", 1), ("Desvio", 12)],
}

HEURISTICA_EXEMPLO = {
    "Inicio":    10,
    "Atalho":     3,
    "Serra":      2,
    "Floresta":   8,
    "Rodovia":    9,
    "Planicie":   6,
    "Ponte":      1,
    "Desvio":     8,
    "Trilha":     7,
    "Caverna":    9,
    "Ruina":     12,
    "Mina":      11,
    "Poco":      13,
    "Destino":    0,
}

ORIGEM_EX = "Inicio"
DESTINO_EX = "Destino"


def sucessores_exemplo(estado):
    return ESTRADAS_EXEMPLO.get(estado, [])


def heuristica_exemplo(estado):
    return HEURISTICA_EXEMPLO.get(estado, 0)
