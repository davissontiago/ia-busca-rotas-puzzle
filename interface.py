# -*- coding: utf-8 -*-
"""
Interface web para os algoritmos de busca.
Abre no navegador com visualizacoes animadas.
"""

import json
import os
import webbrowser
import http.server
import socketserver

from algoritmos_busca import bfs, dfs, busca_gulosa, busca_a_estrela
from dominio_cidades import (
    sucessores_cidades, heuristica_parnaiba, ORIGEM, DESTINO,
    ESTRADAS, HEURISTICA_LINHA_RETA
)
from dominio_puzzle import (
    sucessores_puzzle, h1_pecas_fora, h2_manhattan,
    OBJETIVO, ESTADOS_INICIAIS
)
from dominio_exemplo import (
    sucessores_exemplo, heuristica_exemplo,
    ORIGEM_EX, DESTINO_EX, ESTRADAS_EXEMPLO, HEURISTICA_EXEMPLO
)


def gerar_dados_grafo():
    nos = {}
    for cidade, h in HEURISTICA_LINHA_RETA.items():
        nos[cidade] = {"h": h}

    arestas = []
    vistas = set()
    for cidade, vizinhos in ESTRADAS.items():
        for vizinho, dist in vizinhos:
            par = tuple(sorted([cidade, vizinho]))
            if par not in vistas:
                vistas.add(par)
                arestas.append({"de": cidade, "para": vizinho, "peso": dist})

    return {"nos": nos, "arestas": arestas, "origem": ORIGEM, "destino": DESTINO}


def gerar_dados_exemplo():
    nos = {}
    for cidade, h in HEURISTICA_EXEMPLO.items():
        nos[cidade] = {"h": h}

    arestas = []
    vistas = set()
    for cidade, vizinhos in ESTRADAS_EXEMPLO.items():
        for vizinho, dist in vizinhos:
            par = tuple(sorted([cidade, vizinho]))
            if par not in vistas:
                vistas.add(par)
                arestas.append({"de": cidade, "para": vizinho, "peso": dist})

    return {"nos": nos, "arestas": arestas, "origem": ORIGEM_EX, "destino": DESTINO_EX}


def executar_busca_exemplo(nome):
    if nome == "BFS":
        r = bfs(ORIGEM_EX, DESTINO_EX, sucessores_exemplo, gravar=True)
    elif nome == "DFS":
        r = dfs(ORIGEM_EX, DESTINO_EX, sucessores_exemplo, gravar=True)
    elif nome == "Gulosa":
        r = busca_gulosa(ORIGEM_EX, DESTINO_EX, sucessores_exemplo, heuristica_exemplo, gravar=True)
    elif nome == "A*":
        r = busca_a_estrela(ORIGEM_EX, DESTINO_EX, sucessores_exemplo, heuristica_exemplo, gravar=True)
    else:
        return None

    historico = []
    for p in r.historico:
        historico.append({
            "expandindo": p["expandindo"],
            "visitados": list(p["visitados"]),
            "fronteira": list(p["fronteira"]),
        })

    return {
        "nome": nome,
        "encontrou": r.encontrou,
        "caminho": r.caminho if r.encontrou else [],
        "custo": r.custo,
        "nos_expandidos": r.nos_expandidos,
        "tempo": round(r.tempo * 1000, 3),
        "historico": historico,
    }


def executar_busca_cidades(nome):
    if nome == "BFS":
        r = bfs(ORIGEM, DESTINO, sucessores_cidades, gravar=True)
    elif nome == "DFS":
        r = dfs(ORIGEM, DESTINO, sucessores_cidades, gravar=True)
    elif nome == "Gulosa":
        r = busca_gulosa(ORIGEM, DESTINO, sucessores_cidades, heuristica_parnaiba, gravar=True)
    elif nome == "A*":
        r = busca_a_estrela(ORIGEM, DESTINO, sucessores_cidades, heuristica_parnaiba, gravar=True)
    else:
        return None

    historico = []
    for p in r.historico:
        historico.append({
            "expandindo": p["expandindo"],
            "visitados": list(p["visitados"]),
            "fronteira": list(p["fronteira"]),
        })

    return {
        "nome": nome,
        "encontrou": r.encontrou,
        "caminho": r.caminho if r.encontrou else [],
        "custo": r.custo,
        "nos_expandidos": r.nos_expandidos,
        "tempo": round(r.tempo * 1000, 3),
        "historico": historico,
    }


def executar_busca_puzzle(nome, d):
    estado = ESTADOS_INICIAIS[d]

    if nome == "BFS":
        r = bfs(estado, OBJETIVO, sucessores_puzzle, gravar=True)
    elif nome == "DFS":
        r = dfs(estado, OBJETIVO, sucessores_puzzle, limite=max(30, d * 3), gravar=True)
    elif nome == "Gulosa h1":
        r = busca_gulosa(estado, OBJETIVO, sucessores_puzzle, h1_pecas_fora, gravar=True)
    elif nome == "Gulosa h2":
        r = busca_gulosa(estado, OBJETIVO, sucessores_puzzle, h2_manhattan, gravar=True)
    elif nome == "A* h1":
        r = busca_a_estrela(estado, OBJETIVO, sucessores_puzzle, h1_pecas_fora, gravar=True)
    elif nome == "A* h2":
        r = busca_a_estrela(estado, OBJETIVO, sucessores_puzzle, h2_manhattan, gravar=True)
    else:
        return None

    historico_resumido = []
    total = len(r.historico)
    step = max(1, total // 100) if total > 300 else (max(1, total // 60) if total > 80 else 1)

    for i in range(0, total, step):
        p = r.historico[i]
        est = p["expandindo"]
        historico_resumido.append({
            "expandindo": list(est) if isinstance(est, tuple) else est,
            "n_visitados": len(p["visitados"]),
            "n_fronteira": len(p["fronteira"]),
        })

    caminho = []
    if r.encontrou:
        for estado in r.caminho:
            caminho.append(list(estado))

    return {
        "nome": nome,
        "encontrou": r.encontrou,
        "caminho": caminho,
        "custo": r.custo,
        "nos_expandidos": r.nos_expandidos,
        "tempo": round(r.tempo * 1000, 3),
        "historico": historico_resumido,
    }


class APIHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        self._dir = directory
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        if self.path == "/api/dados":
            dados = {
                "grafo": gerar_dados_grafo(),
                "exemplo": gerar_dados_exemplo(),
                "puzzle": {
                    "objetivo": list(OBJETIVO),
                    "estados": {str(d): list(ESTADOS_INICIAIS[d]) for d in [5, 10, 15]},
                }
            }
            self._json(dados)
        elif self.path.startswith("/api/exemplo/"):
            nome = self.path.split("/api/exemplo/")[1].replace("%20", " ").replace("+", " ")
            res = executar_busca_exemplo(nome)
            self._json(res) if res else self._json({"erro": "invalido"}, 400)
        elif self.path.startswith("/api/cidades/"):
            nome = self.path.split("/api/cidades/")[1].replace("%20", " ").replace("+", " ")
            res = executar_busca_cidades(nome)
            self._json(res) if res else self._json({"erro": "invalido"}, 400)
        elif self.path.startswith("/api/puzzle-solve/"):
            nums = self.path.split("/api/puzzle-solve/")[1]
            estado = tuple(int(x) for x in nums.split(","))
            r = busca_a_estrela(estado, OBJETIVO, sucessores_puzzle, h2_manhattan)
            caminho = [list(e) for e in r.caminho] if r.encontrou else []
            self._json({
                "encontrou": r.encontrou,
                "caminho": caminho,
                "custo": r.custo,
                "nos_expandidos": r.nos_expandidos,
            })
        elif self.path.startswith("/api/puzzle/"):
            partes = self.path.split("/api/puzzle/")[1].split("/")
            nome = partes[0].replace("%20", " ").replace("+", " ")
            d = int(partes[1]) if len(partes) > 1 else 5
            res = executar_busca_puzzle(nome, d)
            self._json(res) if res else self._json({"erro": "invalido"}, 400)
        else:
            super().do_GET()

    def _json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass


def main():
    diretorio = os.path.dirname(os.path.abspath(__file__))
    porta = 8080
    handler = lambda *a, **k: APIHandler(*a, directory=diretorio, **k)

    with socketserver.TCPServer(("", porta), handler) as httpd:
        httpd.allow_reuse_address = True
        print(f"Servidor rodando em http://localhost:{porta}")
        print("Abrindo navegador...")
        print("Pressione Ctrl+C para encerrar.")
        webbrowser.open(f"http://localhost:{porta}/interface.html")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")


if __name__ == "__main__":
    main()
