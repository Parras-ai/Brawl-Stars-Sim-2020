import streamlit as st
import random
import time

# ==========================================
# 1. LÓGICA DEL JUEGO (Todo integrado aquí)
# ==========================================

BRAWLERS = {
    "Shelly": {"hp": 3600, "atk": 1500, "img": "https://static.wikia.nocookie.net/brawlstars/images/6/60/Shelly_Portrait.png"},
    "Nita": {"hp": 4000, "atk": 800, "img": "https://static.wikia.nocookie.net/brawlstars/images/3/30/Nita_Portrait.png"},
    "Colt": {"hp": 2800, "atk": 2000, "img": "https://static.wikia.nocookie.net/brawlstars/images/c/c1/Colt_Portrait.png"},
    "Leon": {"hp": 3200, "atk": 1400, "img": "https://static.wikia.nocookie.net/brawlstars/images/5/5e/Leon_Portrait.png"},
    "Mortis": {"hp": 3800, "atk": 900, "img": "https://static.wikia.nocookie.net/brawlstars/images/3/33/Mortis_Portrait.png"},
    "Crow": {"hp": 2400, "atk": 1000, "img": "https://static.wikia.nocookie.net/brawlstars/images/0/01/Crow_Portrait.png"}
}

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


# ==========================================
# 2. INTERFAZ VISUAL (Streamlit)
# ==========================================

# Configuración de pantalla
st.set_page_config(page_title="Brawl Simulator All-in-One", layout="wide")

# --- FONDO Y ESTILOS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
    }
    .stat-box {
        font-size: 24px;
        font-weight: bold;
        text-shadow: 2px 2px #000;
        background-color: rgba(0,0,0,0.3);
        padding: 10px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN SIN ERRORES ---
if 'coins' not in st.session_state: st.session_state.coins = 500
if 'gems' not in st.session_state: st.session_state.gems = 50
if 'my_brawlers' not in st.session_state: st.session_state.my_brawlers = {"Shelly": 0}
if 'phase' not in st.session_state: st.session_state.phase = 'idle'
if 'items' not in st.session_state: st.session_state.items = 0
if 'reward' not in st.session_state: st.session_state.reward = False

# --- CABECERA DE RECURSOS ---
st.title("🏆 Brawl Stars Sim 2020")
res1, res2, res3 = st.columns(3)
res1.markdown(f"<div class='stat-box'>💰 Monedas: {st.session_state.coins}</div>", unsafe_allow_html=True)
res2.markdown(f"<div class='stat-box'>💎 Gemas: {st.session_state.gems}</div>", unsafe_allow_html=True)
res3.markdown(f"<div class='stat-box'>🏆 Copas Totales: {sum(st.session_state.my_brawlers.values())}</div>", unsafe_allow_html=True)

st.divider()

# --- TODO EN UNA PANTALLA (Pestañas) ---
tab_batalla, tab_tienda, tab_coleccion = st.tabs(["⚔️ BATALLA", "🛒 TIENDA", "👤 COLECCIÓN"])

# --- PESTAÑA: BATALLA ---
with tab_batalla:
    st.subheader("Simulador de Partida")
    col_b, col_info = st.columns([1, 2])
    
    with col_b:
        seleccion = st.selectbox("Elige tu Brawler", list(st.session_state.my_brawlers.keys()))
        st.image(BRAWLERS[seleccion]['img'], width=150)
    
    with col_info:
        st.write(f"**{seleccion}** - Copas actuales: {st.session_state.my_brawlers[seleccion]}")
        if st.button("¡JUGAR PARTIDA! 🥊"):
            with st.spinner("En la arena..."):
                time.sleep(1)
            victoria = random.random() < 0.55
            puntos = calcular_resultado_copas(st.session_state.my_brawlers[seleccion], victoria)
            st.session_state.my_brawlers[seleccion] = max(0, st.session_state.my_brawlers[seleccion] + puntos)
            
            if victoria:
                ganancia = random.randint(20, 50)
                st.session_state.coins += ganancia
                st.success(f"¡Victoria! +{puntos} copas y +{ganancia} monedas.")
                st.balloons()
            else:
                st.error(f"Derrota... {puntos} copas.")
            
            time.sleep(1.5) # Pausa para que veas el resultado
            st.rerun()

# --- PESTAÑA: TIENDA ---
with tab_tienda:
    st.subheader("Cajas Disponibles")
    t1, t2 = st.columns(2)
    
    with t1:
        st.image("https://static.wikia.nocookie.net/brawlstars/images/0/07/Big_Box.png", width=100)
        if st.button("Caja Brawl (100 Monedas)"):
            if st.session_state.coins >= 100:
                st.session_state.coins -= 100
                st.session_state.reward = check_luck("Brawl")
                st.session_state.items = 3 if st.session_state.reward else 2
                st.session_state.phase = 'opening'
                st.rerun()
            else: 
                st.error("No tienes suficientes monedas")

    with t2:
        st.image("https://static.wikia.nocookie.net/brawlstars/images/e/e0/Mega_Box.png", width=120)
        if st.button("MEGACAJA (80 Gemas)"):
            if st.session_state.gems >= 80:
                st.session_state.gems -= 80
                st.session_state.reward = check_luck("Mega")
                st.session_state.items = 6 if st.session_state.reward else 5
                st.session_state.phase = 'opening'
                st.rerun()
            else: 
                st.error("No tienes suficientes gemas")

    # Lógica de apertura visual
    if st.session_state.phase == 'opening':
        st.write("---")
        st.write(f"### 📦 Items restantes: {st.session_state.items}")
        if st.button("PULSAR PANTALLA 🔓"):
            if st.session_state.items > 1:
                st.session_state.items -= 1
                st.session_state.coins += random.randint(10, 30)
                st.rerun()
            else:
                if st.session_state.reward:
                    # Buscar brawlers que aún no tengas
                    posibles = [b for b in BRAWLERS.keys() if b not in st.session_state.my_brawlers]
                    if posibles:
                        nuevo = random.choice(posibles)
                        st.session_state.my_brawlers[nuevo] = 0
                        st.balloons()
                        st.success(f"¡BRUTAL! Te ha tocado {nuevo.upper()}")
                    else:
                        st.info("¡Te salió un Brawler pero ya los tienes todos! (+200 monedas)")
                        st.session_state.coins += 200
                else:
                    st.warning("Solo monedas esta vez...")
                
                st.session_state.phase = 'idle'
                time.sleep(2)
                st.rerun()

# --- PESTAÑA: COLECCIÓN ---
with tab_coleccion:
    st.subheader("Tu Álbum de Brawlers")
    cols_c = st.columns(3)
    for i, (b_name, b_copas) in enumerate(st.session_state.my_brawlers.items()):
        with cols_c[i % 3]:
            st.image(BRAWLERS[b_name]['img'], width=100)
            st.markdown(f"**{b_name}**")
            st.markdown(f"🏆 {b_copas} | Rango {int(b_copas/100)}")
