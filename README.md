# Relatorio Tecnico: Resolucao de Problemas por Busca

**IFPI - Campus Teresina Zona Sul**
**Licenciatura em Computacao**
**Disciplina: Inteligencia Artificial**

---

## 1. Introducao

Este relatorio apresenta a implementacao e analise experimental de quatro algoritmos
de busca em Inteligencia Artificial: Busca em Largura (BFS), Busca em Profundidade (DFS),
Busca Gulosa e Busca A*. Os algoritmos foram aplicados em dois dominios distintos:
roteamento rodoviario no estado do Piaui e o jogo classico dos 8 numeros (8-Puzzle).

## 2. Metodologia

### 2.1 Arquitetura Unificada

Todos os algoritmos foram implementados em Python sobre uma arquitetura unificada que
separa a logica de busca da modelagem dos dominios. Cada algoritmo recebe como parametros:
- Estado inicial e estado objetivo
- Funcao geradora de sucessores (retorna lista de pares (estado, custo))
- Funcao heuristica (para buscas informadas)

Os algoritmos de busca cega utilizam:
- **BFS**: Fila FIFO (collections.deque) como fronteira
- **DFS**: Pilha LIFO (lista Python) como fronteira, com controle de visitados em grafo

Os algoritmos de busca informada utilizam:
- **Gulosa**: Fila de prioridade (heapq) ordenada por f(n) = h(n)
- **A***: Fila de prioridade (heapq) ordenada por f(n) = g(n) + h(n)

### 2.2 Metricas Avaliadas
- **Custo do caminho**: distancia total (km) para cidades, ou numero de movimentos para o 8-Puzzle
- **Nos expandidos**: quantidade de estados retirados da fronteira e processados
- **Tempo de execucao**: tempo de parede em segundos (medido com time.time())
- **Completude**: se o algoritmo sempre encontra solucao quando ela existe
- **Otimalidade**: se o caminho encontrado e o de menor custo

---

## 3. Dominio 1: Roteamento Rodoviario no Piaui

**Origem**: Sao Raimundo Nonato | **Destino**: Parnaiba

O grafo modelado contempla 22 cidades do Piaui com distancias rodoviarias (km).
A heuristica utilizada para a Busca Gulosa e A* e a distancia geografica em linha reta
de cada cidade ate Parnaiba. Esta heuristica e **admissivel**, pois a distancia em linha
reta nunca superestima a distancia rodoviaria real.

### 3.1 Resultados - Rota, Custo, Nos Expandidos e Tempo

| Algoritmo | Rota | Custo (km) | Nos Exp. | Tempo (s) |
|-----------|------|------------|----------|-----------|
| BFS | S.R.Nonato -> Simpl.Mendes -> Oeiras -> Picos -> Valenca -> C.Maior -> Piripiri -> Parnaiba | 875 | 16 | 0.000024 |
| DFS | S.R.Nonato -> C.Buriti -> Floriano -> Amarante -> Teresina -> C.Maior -> Piripiri -> Parnaiba | 880 | 9 | 0.000018 |
| Gulosa | S.R.Nonato -> Simpl.Mendes -> Oeiras -> Picos -> Valenca -> C.Maior -> Piripiri -> Parnaiba | 875 | 8 | 0.000024 |
| A* | S.R.Nonato -> Simpl.Mendes -> Oeiras -> Picos -> Valenca -> C.Maior -> Piripiri -> Parnaiba | 875 | 17 | 0.000030 |

### 3.2 Analise do Dominio de Cidades

- **BFS**: Encontrou a rota via Simplicios Mendes com custo 875 km, expandindo 16 nos.
  Como a BFS explora por camadas (numero de arestas), ela nao garante otimalidade em
  grafos com custos variaveis. Neste caso particular, coincidiu com a rota otima.

- **DFS**: Encontrou uma rota diferente (via Canto do Buriti e Floriano) com custo 880 km,
  5 km a mais que o otimo. Expandiu apenas 9 nos, pois segue profundamente um unico ramo
  antes de retroceder. A DFS NAO garante otimalidade.

- **Busca Gulosa**: Encontrou a rota de 875 km expandindo apenas 8 nos (o menor entre
  todos os algoritmos). A heuristica em linha reta guiou eficientemente a busca neste caso,
  embora a otimalidade NAO seja garantida em geral pela Busca Gulosa.

- **A***: Encontrou a rota otima de 875 km com 17 nos expandidos. E o unico algoritmo
  que **garante otimalidade** quando a heuristica e admissivel (como e o caso da distancia
  em linha reta). Expandiu mais nos que a Gulosa porque precisa verificar se nao ha caminho
  mais barato via outros ramos.

---

## 4. Dominio 2: 8-Puzzle

**Estado objetivo**: 1 2 3 / 4 5 6 / 7 8 _

Estados iniciais com profundidade otima confirmada via A* com h2 (Manhattan):
- **d=5**: `2 _ 3 / 1 5 6 / 4 7 8` (solucao otima = 5 movimentos)
- **d=10**: `_ 1 2 / 4 5 8 / 7 6 3` (solucao otima = 10 movimentos)
- **d=15**: `3 4 2 / _ 1 6 / 5 7 8` (solucao otima = 15 movimentos)

Todos os estados foram verificados como solucionaveis (numero par de inversoes).

### 4.1 Tabela Comparativa Geral (Movimentos, Nos Expandidos e Tempo)

| Algoritmo | d | Movimentos | Nos Expandidos | Tempo (s) |
|-----------|---|------------|----------------|-----------|
| BFS | 5 | 5 | 23 | 0.000046 |
| DFS | 5 | N/A* | 15.136 | 0.016159 |
| Gulosa h1 | 5 | 5 | 6 | 0.000034 |
| Gulosa h2 | 5 | 5 | 6 | 0.000035 |
| A* h1 | 5 | 5 | 6 | 0.000022 |
| A* h2 | 5 | 5 | 6 | 0.000028 |
| **---** | **---** | **---** | **---** | **---** |
| BFS | 10 | 10 | 323 | 0.000456 |
| DFS | 10 | 22 | 6.077 | 0.007720 |
| Gulosa h1 | 10 | 32 | 209 | 0.000841 |
| Gulosa h2 | 10 | 34 | 96 | 0.000537 |
| A* h1 | 10 | 10 | 40 | 0.000149 |
| A* h2 | 10 | 10 | 17 | 0.000087 |
| **---** | **---** | **---** | **---** | **---** |
| BFS | 15 | 15 | 3.625 | 0.005807 |
| DFS | 15 | 29 | 129.817 | 0.193271 |
| Gulosa h1 | 15 | 39 | 561 | 0.002348 |
| Gulosa h2 | 15 | 25 | 293 | 0.001406 |
| A* h1 | 15 | 15 | 407 | 0.001391 |
| A* h2 | 15 | 15 | 110 | 0.000526 |

*N/A: DFS com limite de 30 niveis nao encontrou solucao para d=5 neste caso, pois explorou
ramos incorretos antes de esgotar o limite.*

### 4.2 Comparacao A*: h1 (Pecas Fora do Lugar) vs h2 (Distancia de Manhattan)

| d | Nos A* h1 | Nos A* h2 | Tempo A* h1 (s) | Tempo A* h2 (s) | Reducao de Nos |
|---|-----------|-----------|-----------------|-----------------|----------------|
| 5 | 6 | 6 | 0.000022 | 0.000028 | 0% |
| 10 | 40 | 17 | 0.000149 | 0.000087 | 57,5% |
| 15 | 407 | 110 | 0.001391 | 0.000526 | 73,0% |

### 4.3 Analise Detalhada

**Completude:**

| Algoritmo | Completa? | Observacao |
|-----------|-----------|------------|
| BFS | Sim | Encontra solucao se existir, para grafos finitos |
| DFS | Condicional | Completa com visitados em grafos finitos; pode nao terminar sem limite em espacos infinitos |
| Gulosa | Condicional | Com controle de visitados, completa em espacos finitos; sem visitados, pode ciclar |
| A* | Sim | Com heuristica admissivel e espaco finito |

**Otimalidade:**

| Algoritmo | Otima? | Evidencia Experimental |
|-----------|--------|----------------------|
| BFS | Sim (custos uniformes) | Encontrou solucoes otimas no 8-Puzzle (5, 10, 15 mov.). No problema de cidades com custos variaveis, nao ha garantia formal, mas coincidiu com o otimo neste caso. |
| DFS | Nao | Encontrou 22 mov. (otimo=10) e 29 mov. (otimo=15). Nao encontrou solucao para d=5 dentro do limite. |
| Gulosa | Nao | Encontrou 32 mov. em d=10 (otimo=10) e 39 mov. em d=15 (otimo=15). Ignora g(n). |
| A* | Sim | Encontrou solucao otima em TODOS os casos (5, 10, 15 mov.) com ambas as heuristicas. |

**Analise h1 vs h2:**

A heuristica h2 (distancia de Manhattan) **domina** h1 (pecas fora do lugar), ou seja,
h2(n) >= h1(n) para todo estado n, e ambas sao admissiveis. Isso a torna mais informativa.

Resultados experimentais confirmam:
- Para d=5 (problema simples), ambas expandem o mesmo numero de nos (6).
- Para d=10, A* com h2 expandiu 17 nos vs 40 com h1 — reducao de **57,5%**.
- Para d=15, A* com h2 expandiu 110 nos vs 407 com h1 — reducao de **73,0%**.
- Os tempos de execucao acompanham proporcionalmente: 0.000526s (h2) vs 0.001391s (h1) em d=15.

A vantagem de h2 cresce com a profundidade da solucao, confirmando a teoria de que
heuristicas mais informativas reduzem exponencialmente o espaco de busca explorado pelo A*.

---

## 5. Conclusao

Os resultados experimentais confirmam as propriedades teoricas dos algoritmos de busca:

1. **BFS** e completa e otima para custos uniformes (8-Puzzle), mas o numero de nos
   expandidos cresce exponencialmente com a profundidade (23 -> 323 -> 3.625 para d=5,10,15).

2. **DFS** pode ser eficiente em memoria mas encontra solucoes subotimas (22 e 29 movimentos
   vs otimos de 10 e 15) e pode falhar com limite de profundidade inadequado.

3. **Busca Gulosa** e rapida (poucos nos expandidos: 96-561 em d=15) mas sacrifica
   otimalidade, encontrando caminhos ate 2-3x mais longos que o otimo.

4. **A*** combina completude e otimalidade com eficiencia. Com h2 (Manhattan), alcanca
   o melhor equilibrio entre qualidade da solucao e custo computacional.

5. A escolha da heuristica impacta diretamente o desempenho do A*: **h2 domina h1** e
   reduz os nos expandidos em ate 73%, demonstrando que heuristicas mais informativas
   (porem admissiveis) sao sempre preferidas.

---

## Anexo: Estrutura do Codigo

| Arquivo | Descricao |
|---------|-----------|
| `algoritmos_busca.py` | Implementacao dos 4 algoritmos (BFS, DFS, Gulosa, A*) |
| `dominio_cidades.py` | Grafo rodoviario do Piaui (22 cidades) + heuristica em linha reta |
| `dominio_puzzle.py` | 8-Puzzle: sucessores, h1, h2 e estados iniciais |
| `main.py` | Script principal que executa todos os testes e gera tabelas |
| `resultado_execucao.txt` | Saida completa da execucao |
