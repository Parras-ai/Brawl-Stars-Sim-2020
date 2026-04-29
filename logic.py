import random

# Stats equilibradas y fotos funcionales
BRAWLERS = {
    "Shelly": {"hp": 3600, "atk": 1500, "img": "https://static.wikia.nocookie.net/brawlstars/images/6/60/Shelly_Portrait.png"},
    "Nita": {"hp": 4000, "atk": 800, "img": "https://static.wikia.nocookie.net/brawlstars/images/3/30/Nita_Portrait.png"},
    "Colt": {"hp": 2800, "atk": 2000, "img": "https://static.wikia.nocookie.net/brawlstars/images/5/52/El_Primo_Portrait.png"},
    "Leon": {"hp": 3200, "atk": 1400, "img": "https://static.wikia.nocookie.net/brawlstars/images/5/5e/Leon_Portrait.png"},
    "Mortis": {"hp": 3800, "atk": 900, "img": "https://static.wikia.nocookie.net/brawlstars/images/3/33/Mortis_Portrait.png"},
    "Crow": {"hp": 2400, "atk": 1000, "img": "https://static.wikia.nocookie.net/brawlstars/images/0/01/Crow_Portrait.png"}
}

# Precios equilibrados
PRECIOS = {
    "Caja_Brawl": {"monedas": 100, "gemas": 0},
    "Megacaja": {"monedas": 1500, "gemas": 80}
}

def check_luck(box_type):
    prob = 0.25 if box_type == "Mega" else 0.05
    return random.random() < prob

def calcular_resultado_copas(copas, victoria):
    if victoria:
        return 8
    else:
        return -4 if copas > 100 else 0
