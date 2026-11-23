"""
Domínio 1: Roteamento Rodoviário no Piauí
Origem: São Raimundo Nonato → Destino: Parnaíba

Grafo com distâncias rodoviárias (km) entre cidades do Piauí
e heurísticas em linha reta até Parnaíba.
"""

# Distâncias rodoviárias entre cidades (km) - grafo bidirecional
ESTRADAS = {
    "São Raimundo Nonato": [("Simplício Mendes", 120), ("Canto do Buriti", 95)],
    "Canto do Buriti": [("São Raimundo Nonato", 95), ("Floriano", 160)],
    "Simplício Mendes": [("São Raimundo Nonato", 120), ("Oeiras", 110), ("Floriano", 170)],
    "Floriano": [("Canto do Buriti", 160), ("Simplício Mendes", 170), ("Oeiras", 130), ("Amarante", 90)],
    "Oeiras": [("Simplício Mendes", 110), ("Floriano", 130), ("Picos", 100)],
    "Amarante": [("Floriano", 90), ("Teresina", 180)],
    "Picos": [("Oeiras", 100), ("Jaicós", 75), ("Pio IX", 110), ("Valença do Piauí", 105)],
    "Jaicós": [("Picos", 75), ("Simplício Mendes", 80)],
    "Pio IX": [("Picos", 110), ("Fronteiras", 55)],
    "Fronteiras": [("Pio IX", 55), ("Picos", 140)],
    "Valença do Piauí": [("Picos", 105), ("Teresina", 240), ("Campo Maior", 170)],
    "Teresina": [("Amarante", 180), ("Valença do Piauí", 240), ("Campo Maior", 85), ("José de Freitas", 55), ("Altos", 40)],
    "Altos": [("Teresina", 40), ("José de Freitas", 35), ("Campo Maior", 65)],
    "José de Freitas": [("Teresina", 55), ("Altos", 35), ("Campo Maior", 50)],
    "Campo Maior": [("Teresina", 85), ("José de Freitas", 50), ("Valença do Piauí", 170), ("Piripiri", 80)],
    "Piripiri": [("Campo Maior", 80), ("Pedro II", 60), ("Batalha", 70), ("Parnaíba", 190)],
    "Pedro II": [("Piripiri", 60), ("Piracuruca", 100)],
    "Piracuruca": [("Pedro II", 100), ("Parnaíba", 100)],
    "Batalha": [("Piripiri", 70), ("Esperantina", 55)],
    "Esperantina": [("Batalha", 55), ("Luzilândia", 50)],
    "Luzilândia": [("Esperantina", 50), ("Parnaíba", 100)],
    "Parnaíba": [("Piripiri", 190), ("Piracuruca", 100), ("Luzilândia", 100)],
}

# Distâncias em linha reta (km) de cada cidade até Parnaíba (heurística admissível)
HEURISTICA_LINHA_RETA = {
    "São Raimundo Nonato": 590,
    "Canto do Buriti": 520,
    "Simplício Mendes": 480,
    "Floriano": 420,
    "Oeiras": 400,
    "Amarante": 350,
    "Picos": 370,
    "Jaicós": 430,
    "Pio IX": 400,
    "Fronteiras": 410,
    "Valença do Piauí": 310,
    "Teresina": 250,
    "Altos": 230,
    "José de Freitas": 220,
    "Campo Maior": 200,
    "Piripiri": 150,
    "Pedro II": 140,
    "Piracuruca": 85,
    "Batalha": 130,
    "Esperantina": 115,
    "Luzilândia": 90,
    "Parnaíba": 0,
}


def sucessores_cidades(cidade):
    """Retorna lista de (vizinho, distância_km) para uma cidade."""
    return ESTRADAS.get(cidade, [])


def heuristica_parnaiba(cidade):
    """Distância em linha reta até Parnaíba."""
    return HEURISTICA_LINHA_RETA.get(cidade, float('inf'))


ORIGEM = "São Raimundo Nonato"
DESTINO = "Parnaíba"
