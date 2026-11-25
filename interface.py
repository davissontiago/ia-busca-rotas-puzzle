# -*- coding: utf-8 -*-
"""
Interface grafica para os algoritmos de busca.
Dois dominios: Cidades do Piaui e 8-Puzzle.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading

from algoritmos_busca import bfs, dfs, busca_gulosa, busca_a_estrela
from dominio_cidades import (
    sucessores_cidades, heuristica_parnaiba, ORIGEM, DESTINO,
    ESTRADAS, HEURISTICA_LINHA_RETA
)
from dominio_puzzle import (
    sucessores_puzzle, h1_pecas_fora, h2_manhattan,
    OBJETIVO, ESTADOS_INICIAIS, eh_soluvel
)

# Coordenadas aproximadas das cidades para desenho no canvas (x, y)
COORDENADAS_CIDADES = {
    "São Raimundo Nonato": (120, 520),
    "Canto do Buriti": (200, 450),
    "Simplício Mendes": (250, 500),
    "Floriano": (230, 370),
    "Oeiras": (330, 420),
    "Amarante": (250, 290),
    "Picos": (410, 380),
    "Jaicós": (340, 480),
    "Pio IX": (500, 400),
    "Fronteiras": (540, 360),
    "Valença do Piauí": (380, 300),
    "Teresina": (220, 190),
    "Altos": (270, 165),
    "José de Freitas": (300, 140),
    "Campo Maior": (350, 170),
    "Piripiri": (380, 100),
    "Pedro II": (440, 80),
    "Piracuruca": (490, 50),
    "Batalha": (340, 55),
    "Esperantina": (300, 30),
    "Luzilândia": (350, 15),
    "Parnaíba": (460, 10),
}

COR_FUNDO = "#1e1e2e"
COR_PAINEL = "#2a2a3c"
COR_BORDA = "#3a3a5c"
COR_TEXTO = "#cdd6f4"
COR_TITULO = "#89b4fa"
COR_ACENTO = "#f38ba8"
COR_VERDE = "#a6e3a1"
COR_AMARELO = "#f9e2af"
COR_AZUL = "#89b4fa"
COR_ROXO = "#cba6f7"
COR_LARANJA = "#fab387"
COR_ARESTA = "#585b70"
COR_CIDADE = "#45475a"
COR_ROTA = "#f38ba8"
COR_CELULA = "#313244"
COR_CELULA_CERTA = "#a6e3a1"
COR_CELULA_ERRADA = "#f38ba8"
COR_VAZIO = "#45475a"

CORES_ALGO = {
    "BFS": COR_AZUL,
    "DFS": COR_ROXO,
    "Gulosa": COR_LARANJA,
    "Gulosa h1": COR_LARANJA,
    "Gulosa h2": COR_AMARELO,
    "A*": COR_VERDE,
    "A* h1": COR_VERDE,
    "A* h2": COR_ACENTO,
}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Algoritmos de Busca - IA (IFPI)")
        self.geometry("1100x720")
        self.configure(bg=COR_FUNDO)
        self.minsize(900, 600)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background=COR_FUNDO, borderwidth=0)
        style.configure("TNotebook.Tab", background=COR_PAINEL, foreground=COR_TEXTO,
                         padding=[16, 6], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab",
                   background=[("selected", COR_BORDA)],
                   foreground=[("selected", COR_TITULO)])
        style.configure("TFrame", background=COR_FUNDO)
        style.configure("TLabel", background=COR_FUNDO, foreground=COR_TEXTO, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 13, "bold"), foreground=COR_TITULO)
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.aba_cidades = AbaCidades(notebook)
        self.aba_puzzle = AbaPuzzle(notebook)

        notebook.add(self.aba_cidades, text="  Cidades do Piauí  ")
        notebook.add(self.aba_puzzle, text="  8-Puzzle  ")


class AbaCidades(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.resultados = {}
        self.rota_atual = []

        # Layout: esquerda = canvas, direita = controles + resultados
        paned = ttk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=4, pady=4)

        # Canvas do mapa
        frame_mapa = ttk.Frame(paned)
        paned.add(frame_mapa, weight=3)

        ttk.Label(frame_mapa, text="Mapa Rodoviário do Piauí", style="Title.TLabel").pack(pady=(6, 2))

        self.canvas = tk.Canvas(frame_mapa, bg=COR_FUNDO, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=4, pady=4)
        self.canvas.bind("<Configure>", lambda e: self.desenhar_mapa())

        # Painel direito
        frame_dir = ttk.Frame(paned)
        paned.add(frame_dir, weight=2)

        ttk.Label(frame_dir, text="Controles", style="Title.TLabel").pack(pady=(6, 4))

        info = ttk.Label(frame_dir, text=f"Origem: {ORIGEM}\nDestino: {DESTINO}",
                         wraplength=350, justify="center")
        info.pack(pady=4)

        frame_btns = ttk.Frame(frame_dir)
        frame_btns.pack(pady=6)

        for i, (nome, cor) in enumerate([("BFS", COR_AZUL), ("DFS", COR_ROXO),
                                          ("Gulosa", COR_LARANJA), ("A*", COR_VERDE)]):
            btn = tk.Button(frame_btns, text=nome, bg=cor, fg="#11111b",
                            font=("Segoe UI", 10, "bold"), width=10, cursor="hand2",
                            activebackground=cor,
                            command=lambda n=nome: self.executar(n))
            btn.grid(row=i // 2, column=i % 2, padx=4, pady=3)

        btn_todos = tk.Button(frame_btns, text="Executar Todos", bg=COR_TITULO, fg="#11111b",
                              font=("Segoe UI", 10, "bold"), width=22, cursor="hand2",
                              activebackground=COR_TITULO,
                              command=self.executar_todos)
        btn_todos.grid(row=2, column=0, columnspan=2, padx=4, pady=6)

        ttk.Label(frame_dir, text="Resultados", style="Title.TLabel").pack(pady=(10, 4))

        # Tabela de resultados
        cols = ("algo", "custo", "nos", "tempo")
        self.tree = ttk.Treeview(frame_dir, columns=cols, show="headings", height=5)
        self.tree.heading("algo", text="Algoritmo")
        self.tree.heading("custo", text="Custo (km)")
        self.tree.heading("nos", text="Nós Exp.")
        self.tree.heading("tempo", text="Tempo (s)")
        self.tree.column("algo", width=80, anchor="center")
        self.tree.column("custo", width=80, anchor="center")
        self.tree.column("nos", width=80, anchor="center")
        self.tree.column("tempo", width=90, anchor="center")

        style = ttk.Style()
        style.configure("Treeview", background=COR_PAINEL, foreground=COR_TEXTO,
                         fieldbackground=COR_PAINEL, font=("Consolas", 10), rowheight=26)
        style.configure("Treeview.Heading", background=COR_BORDA, foreground=COR_TITULO,
                         font=("Segoe UI", 9, "bold"))

        self.tree.pack(fill="x", padx=8, pady=4)

        # Rota detalhada
        self.lbl_rota = tk.Text(frame_dir, bg=COR_PAINEL, fg=COR_TEXTO, font=("Consolas", 9),
                                height=6, wrap="word", relief="flat", padx=8, pady=6)
        self.lbl_rota.pack(fill="x", padx=8, pady=4)
        self.lbl_rota.insert("1.0", "Clique em um algoritmo para ver a rota.")
        self.lbl_rota.config(state="disabled")

        self.tree.bind("<<TreeviewSelect>>", self.ao_selecionar)

    def desenhar_mapa(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10 or h < 10:
            return

        sx = w / 620
        sy = h / 560

        # Desenhar arestas
        desenhadas = set()
        for cidade, vizinhos in ESTRADAS.items():
            if cidade not in COORDENADAS_CIDADES:
                continue
            x1, y1 = COORDENADAS_CIDADES[cidade]
            for vizinho, dist in vizinhos:
                if vizinho not in COORDENADAS_CIDADES:
                    continue
                par = tuple(sorted([cidade, vizinho]))
                if par in desenhadas:
                    continue
                desenhadas.add(par)
                x2, y2 = COORDENADAS_CIDADES[vizinho]

                eh_rota = False
                for i in range(len(self.rota_atual) - 1):
                    if par == tuple(sorted([self.rota_atual[i], self.rota_atual[i+1]])):
                        eh_rota = True
                        break

                cor = COR_ROTA if eh_rota else COR_ARESTA
                larg = 3 if eh_rota else 1
                self.canvas.create_line(x1*sx, y1*sy, x2*sx, y2*sy,
                                        fill=cor, width=larg)

                mx, my = (x1+x2)/2*sx, (y1+y2)/2*sy
                self.canvas.create_text(mx, my, text=str(dist),
                                        fill="#7f849c", font=("Consolas", 7))

        # Desenhar cidades
        for cidade, (x, y) in COORDENADAS_CIDADES.items():
            px, py = x * sx, y * sy
            r = 6

            if cidade in self.rota_atual:
                cor = COR_ROTA
                r = 8
            elif cidade == ORIGEM:
                cor = COR_VERDE
            elif cidade == DESTINO:
                cor = COR_AZUL
            else:
                cor = COR_CIDADE

            self.canvas.create_oval(px-r, py-r, px+r, py+r, fill=cor, outline=cor)

            nome_curto = cidade.replace("São Raimundo Nonato", "S.R.Nonato") \
                               .replace("Simplício Mendes", "S.Mendes") \
                               .replace("Valença do Piauí", "Valença") \
                               .replace("José de Freitas", "J.Freitas") \
                               .replace("Campo Maior", "C.Maior")
            self.canvas.create_text(px, py - r - 8, text=nome_curto,
                                    fill=COR_TEXTO, font=("Segoe UI", 7))

    def executar(self, nome):
        if nome == "BFS":
            r = bfs(ORIGEM, DESTINO, sucessores_cidades)
        elif nome == "DFS":
            r = dfs(ORIGEM, DESTINO, sucessores_cidades)
        elif nome == "Gulosa":
            r = busca_gulosa(ORIGEM, DESTINO, sucessores_cidades, heuristica_parnaiba)
        elif nome == "A*":
            r = busca_a_estrela(ORIGEM, DESTINO, sucessores_cidades, heuristica_parnaiba)
        else:
            return

        self.resultados[nome] = r
        self.atualizar_tabela()
        self.mostrar_rota(nome, r)

    def executar_todos(self):
        for nome in ["BFS", "DFS", "Gulosa", "A*"]:
            self.executar(nome)

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for nome, r in self.resultados.items():
            custo = r.custo if r.encontrou else "N/A"
            self.tree.insert("", "end", values=(nome, custo, r.nos_expandidos, f"{r.tempo:.6f}"))

    def mostrar_rota(self, nome, r):
        self.rota_atual = r.caminho if r.encontrou else []
        self.desenhar_mapa()

        self.lbl_rota.config(state="normal")
        self.lbl_rota.delete("1.0", "end")
        if r.encontrou:
            self.lbl_rota.insert("1.0",
                f"[{nome}] Custo: {r.custo} km | Nós: {r.nos_expandidos}\n\n"
                f"Rota: {' → '.join(r.caminho)}")
        else:
            self.lbl_rota.insert("1.0", f"[{nome}] Solução não encontrada.")
        self.lbl_rota.config(state="disabled")

    def ao_selecionar(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        nome = vals[0]
        if nome in self.resultados:
            self.mostrar_rota(nome, self.resultados[nome])


class AbaPuzzle(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.resultados = {}
        self.estado_atual = None
        self.caminho_solucao = []
        self.passo_atual = 0
        self.animando = False
        self.d_selecionado = 5

        # Layout
        paned = ttk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=4, pady=4)

        # Esquerda: tabuleiro
        frame_esq = ttk.Frame(paned)
        paned.add(frame_esq, weight=2)

        ttk.Label(frame_esq, text="8-Puzzle", style="Title.TLabel").pack(pady=(6, 2))

        # Seletor de profundidade
        frame_d = ttk.Frame(frame_esq)
        frame_d.pack(pady=6)
        ttk.Label(frame_d, text="Profundidade:").pack(side="left", padx=4)

        self.var_d = tk.IntVar(value=5)
        for d in [5, 10, 15]:
            rb = tk.Radiobutton(frame_d, text=f"d={d}", variable=self.var_d, value=d,
                                bg=COR_FUNDO, fg=COR_TEXTO, selectcolor=COR_PAINEL,
                                activebackground=COR_FUNDO, activeforeground=COR_TITULO,
                                font=("Segoe UI", 10), command=self.ao_mudar_d)
            rb.pack(side="left", padx=6)

        self.canvas = tk.Canvas(frame_esq, bg=COR_FUNDO, highlightthickness=0,
                                width=300, height=300)
        self.canvas.pack(pady=10)

        # Controles de animacao
        frame_anim = ttk.Frame(frame_esq)
        frame_anim.pack(pady=4)

        self.btn_play = tk.Button(frame_anim, text="▶ Animar Solução", bg=COR_VERDE, fg="#11111b",
                                   font=("Segoe UI", 10, "bold"), cursor="hand2",
                                   command=self.animar_solucao, state="disabled")
        self.btn_play.pack(side="left", padx=4)

        self.btn_reset = tk.Button(frame_anim, text="↺ Reset", bg=COR_AMARELO, fg="#11111b",
                                    font=("Segoe UI", 10, "bold"), cursor="hand2",
                                    command=self.resetar)
        self.btn_reset.pack(side="left", padx=4)

        self.lbl_passo = ttk.Label(frame_esq, text="")
        self.lbl_passo.pack(pady=2)

        # Direita: controles + resultados
        frame_dir = ttk.Frame(paned)
        paned.add(frame_dir, weight=3)

        ttk.Label(frame_dir, text="Algoritmos", style="Title.TLabel").pack(pady=(6, 4))

        frame_btns = ttk.Frame(frame_dir)
        frame_btns.pack(pady=4)

        algos = [("BFS", COR_AZUL), ("DFS", COR_ROXO),
                 ("Gulosa h1", COR_LARANJA), ("Gulosa h2", COR_AMARELO),
                 ("A* h1", COR_VERDE), ("A* h2", COR_ACENTO)]

        for i, (nome, cor) in enumerate(algos):
            btn = tk.Button(frame_btns, text=nome, bg=cor, fg="#11111b",
                            font=("Segoe UI", 9, "bold"), width=10, cursor="hand2",
                            activebackground=cor,
                            command=lambda n=nome: self.executar(n))
            btn.grid(row=i // 2, column=i % 2, padx=3, pady=2)

        btn_todos = tk.Button(frame_btns, text="Executar Todos", bg=COR_TITULO, fg="#11111b",
                              font=("Segoe UI", 10, "bold"), width=22, cursor="hand2",
                              activebackground=COR_TITULO,
                              command=self.executar_todos)
        btn_todos.grid(row=3, column=0, columnspan=2, padx=4, pady=6)

        ttk.Label(frame_dir, text="Resultados", style="Title.TLabel").pack(pady=(8, 4))

        cols = ("algo", "movs", "nos", "tempo")
        self.tree = ttk.Treeview(frame_dir, columns=cols, show="headings", height=7)
        self.tree.heading("algo", text="Algoritmo")
        self.tree.heading("movs", text="Movimentos")
        self.tree.heading("nos", text="Nós Exp.")
        self.tree.heading("tempo", text="Tempo (s)")
        self.tree.column("algo", width=90, anchor="center")
        self.tree.column("movs", width=85, anchor="center")
        self.tree.column("nos", width=85, anchor="center")
        self.tree.column("tempo", width=90, anchor="center")
        self.tree.pack(fill="x", padx=8, pady=4)

        self.tree.bind("<<TreeviewSelect>>", self.ao_selecionar_resultado)

        # Info da solucao selecionada
        self.lbl_info = tk.Text(frame_dir, bg=COR_PAINEL, fg=COR_TEXTO, font=("Consolas", 9),
                                height=5, wrap="word", relief="flat", padx=8, pady=6)
        self.lbl_info.pack(fill="x", padx=8, pady=4)
        self.lbl_info.insert("1.0", "Selecione uma profundidade e execute os algoritmos.")
        self.lbl_info.config(state="disabled")

        self.ao_mudar_d()

    def ao_mudar_d(self):
        self.d_selecionado = self.var_d.get()
        self.estado_atual = ESTADOS_INICIAIS[self.d_selecionado]
        self.resultados = {}
        self.caminho_solucao = []
        self.passo_atual = 0
        self.btn_play.config(state="disabled")
        self.atualizar_tabela()
        self.desenhar_tabuleiro(self.estado_atual)
        self.lbl_passo.config(text=f"Estado inicial (d={self.d_selecionado})")

    def desenhar_tabuleiro(self, estado):
        self.canvas.delete("all")
        tam = 85
        margem = 20
        for i in range(9):
            linha, col = divmod(i, 3)
            x = margem + col * tam
            y = margem + linha * tam
            valor = estado[i]

            if valor == 0:
                cor = COR_VAZIO
                cor_txt = "#7f849c"
                txt = ""
            elif valor == OBJETIVO[i]:
                cor = COR_CELULA_CERTA
                cor_txt = "#11111b"
                txt = str(valor)
            else:
                cor = COR_CELULA_ERRADA
                cor_txt = "#11111b"
                txt = str(valor)

            r = 8
            self.canvas.create_rectangle(x+r, y, x+tam-r, y+tam, fill=cor, outline="")
            self.canvas.create_rectangle(x, y+r, x+tam, y+tam-r, fill=cor, outline="")
            self.canvas.create_oval(x, y, x+2*r, y+2*r, fill=cor, outline="")
            self.canvas.create_oval(x+tam-2*r, y, x+tam, y+2*r, fill=cor, outline="")
            self.canvas.create_oval(x, y+tam-2*r, x+2*r, y+tam, fill=cor, outline="")
            self.canvas.create_oval(x+tam-2*r, y+tam-2*r, x+tam, y+tam, fill=cor, outline="")

            if txt:
                self.canvas.create_text(x + tam/2, y + tam/2, text=txt,
                                        fill=cor_txt, font=("Segoe UI", 28, "bold"))

    def executar(self, nome):
        estado = ESTADOS_INICIAIS[self.d_selecionado]

        if nome == "BFS":
            r = bfs(estado, OBJETIVO, sucessores_puzzle)
        elif nome == "DFS":
            r = dfs(estado, OBJETIVO, sucessores_puzzle, limite=max(30, self.d_selecionado * 3))
        elif nome == "Gulosa h1":
            r = busca_gulosa(estado, OBJETIVO, sucessores_puzzle, h1_pecas_fora)
        elif nome == "Gulosa h2":
            r = busca_gulosa(estado, OBJETIVO, sucessores_puzzle, h2_manhattan)
        elif nome == "A* h1":
            r = busca_a_estrela(estado, OBJETIVO, sucessores_puzzle, h1_pecas_fora)
        elif nome == "A* h2":
            r = busca_a_estrela(estado, OBJETIVO, sucessores_puzzle, h2_manhattan)
        else:
            return

        self.resultados[nome] = r
        self.atualizar_tabela()
        self.mostrar_info(nome, r)

    def executar_todos(self):
        for nome in ["BFS", "DFS", "Gulosa h1", "Gulosa h2", "A* h1", "A* h2"]:
            self.executar(nome)

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for nome, r in self.resultados.items():
            movs = r.custo if r.encontrou else "N/A"
            self.tree.insert("", "end", values=(nome, movs, r.nos_expandidos, f"{r.tempo:.6f}"))

    def mostrar_info(self, nome, r):
        self.lbl_info.config(state="normal")
        self.lbl_info.delete("1.0", "end")
        if r.encontrou:
            otimo = "SIM" if nome.startswith("A*") or (nome == "BFS") else "?"
            self.lbl_info.insert("1.0",
                f"[{nome}] d={self.d_selecionado}\n"
                f"Movimentos: {r.custo} | Nós expandidos: {r.nos_expandidos}\n"
                f"Tempo: {r.tempo:.6f}s\n"
                f"Solução ótima: {otimo}\n"
                f"Clique '▶ Animar' para ver o passo a passo.")
            self.caminho_solucao = r.caminho
            self.passo_atual = 0
            self.btn_play.config(state="normal")
        else:
            self.lbl_info.insert("1.0", f"[{nome}] Solução não encontrada (d={self.d_selecionado})")
            self.btn_play.config(state="disabled")
        self.lbl_info.config(state="disabled")

    def ao_selecionar_resultado(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        nome = vals[0]
        if nome in self.resultados:
            self.mostrar_info(nome, self.resultados[nome])

    def animar_solucao(self):
        if not self.caminho_solucao or self.animando:
            return
        self.animando = True
        self.passo_atual = 0
        self._proximo_passo()

    def _proximo_passo(self):
        if self.passo_atual >= len(self.caminho_solucao):
            self.animando = False
            self.lbl_passo.config(text="Solução completa!")
            return

        estado = self.caminho_solucao[self.passo_atual]
        self.desenhar_tabuleiro(estado)

        total = len(self.caminho_solucao) - 1
        if self.passo_atual == 0:
            self.lbl_passo.config(text=f"Estado inicial")
        else:
            self.lbl_passo.config(text=f"Passo {self.passo_atual}/{total}")

        self.passo_atual += 1
        delay = 400 if total <= 10 else (200 if total <= 20 else 100)
        self.after(delay, self._proximo_passo)

    def resetar(self):
        self.animando = False
        self.passo_atual = 0
        self.estado_atual = ESTADOS_INICIAIS[self.d_selecionado]
        self.desenhar_tabuleiro(self.estado_atual)
        self.lbl_passo.config(text=f"Estado inicial (d={self.d_selecionado})")


if __name__ == "__main__":
    app = App()
    app.mainloop()
