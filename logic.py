import random

# Base de datos de Brawlers con stats de 2020
BRAWLERS = {
    "Shelly": {"hp": 3600, "atk": 1500, "img": "https://static.wikia.nocookie.net/brawlstars/images/6/60/Shelly_Portrait.png"},
    "Nita": {"hp": 4000, "atk": 800, "img": "https://static.wikia.nocookie.net/brawlstars/images/3/30/Nita_Portrait.png"},
    "Colt": {"hp": 2800, "atk": 2000, "img": "https://static.wikia.nocookie.net/brawlstars/images/5/52/El_Primo_Portrait.png"},
    "Leon": {"hp": 3200, "atk": 1400, "img": "https://static.wikia.nocookie.net/brawlstars/images/5/5e/Leon_Portrait.png"},
    "Mortis": {"hp": 3800, "atk": 900, "img": "https://static.wikia.nocookie.net/brawlstars/images/3/33/Mortis_Portrait.png"}
}

def check_luck(box_type):
    probs = {"Mega": 0.25, "Grande": 0.12, "Brawl": 0.05}
    return random.random() < probs.get(box_type, 0.05)

def calcular_resultado_copas(copas_actuales, victoria):
    """Sistema de trofeos equitativo"""
    if victoria:
        return 8 if copas_actuales < 700 else 5
    else:
        if copas_actuales < 100: return 0
        return -5 if copas_actuales < 700 else -8
