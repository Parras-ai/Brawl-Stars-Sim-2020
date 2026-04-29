import streamlit as st
import random
import time
import requests

# ==========================================
# 1. CONFIGURACIÓN TU FIREBASE (CONECTADO ✅)
# ==========================================
FIREBASE_URL = "https://brawlsim-b5ed8-default-rtdb.europe-west1.firebasedatabase.app"

def load_user_data(username):
    url = f"{FIREBASE_URL}/jugadores/{username}.json"
    try:
        res = requests.get(url)
        if res.status_code == 200 and res.json() is not None:
            return res.json()
    except: pass
    return None

def save_player_data():
    if 'player_name' in st.session_state:
        url = f"{FIREBASE_URL}/jugadores/{st.session_state.player_name}.json"
        data = {
            "coins": st.session_state.coins,
            "gems": st.session_state.gems,
            "my_brawlers": st.session_state.my_brawlers
        }
        try: requests.put(url, json=data)
        except: pass

# ==========================================
# 2. DATOS CON LOS PINS DE TU IMAGEN
# ==========================================
BRAWLERS = {
    "Shelly": {"img": "https://cdn.brawlify.com/pins/Shelly.png"},
    "Nita": {"img": "https://cdn.brawlify.com/pins/Nita.png"},
    "Colt": {"img": "https://cdn.brawlify.com/pins/Colt.png"},
    "Leon": {"img": "https://cdn.brawlify.com/pins/Leon.png"},
    "Mortis": {"img": "https://cdn.brawlify.com/pins/Mortis.png"},
    "Crow": {"img": "https://cdn.brawlify.com/pins/Crow.png"},
    "Spike": {"img": "https://cdn.brawlify.com/pins/Spike.png"},
    "Poco": {"img": "https://cdn.brawlify.com/pins/Poco.png"},
    "El Primo": {"img": "https://cdn.brawlify.com/pins/El-Primo.png"}
}

MODOS = {
    "💎 ATRAPAGEMAS": {"type": "3vs3", "cups": 8, "mult": 1.0},
    "⚽ BALÓN BRAWL": {"type": "3vs3", "cups": 10, "mult": 1.2},
    "🌵 SUPERVIVENCIA": {"type": "showdown", "cups": 12, "mult": 1.5}
}

BOT_NAMES = ["LeonPro", "ShellyKiller", "NoobMaster69", "BrawlStar_Fan", "PocoLoco", "BullCharge", "SuperCell_Boss"]

if 'phase' not in st.session_state: st.session_state.phase = 'idle'
if 'selected_brawler' not in st.session_state: st.session_state.selected_brawler = "Shelly"

# ==========================================
# 3. ESTILO NEO-RETRO MEJORADO
# ==========================================
st.set_page_config(page_title="Brawl Sim Pins Edition", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lilita+One&display=swap');
    
    html, body, p, h1, h2, h3, .stButton>button { 
        font-family: 'Lilita One', cursive !important; 
        text-transform: uppercase; 
    }
    .stApp { background: #0a0a20; color: white; }
    
    /* HUD Superior */
    .hud-bar {
        display: flex;
        justify-content: space-around;
        background: rgba(0,0,0,0.8);
        padding: 15px;
        border-bottom: 3px solid #f1c40f;
        margin-bottom: 20px;
    }
    .hud-val { font-size: 22px; color: #f1c40f; }

    /* Botones de Navegación Gigantes */
    .nav-btn>button {
        height: 120px !important;
        font-size: 35px !important;
        border-radius: 25px !important;
        border: 5px solid black !important;
        box-shadow: 0 8px #000;
    }
    .btn-tienda>button { background: linear-gradient(180deg, #3498db, #2980b9) !important; color: white !important; }
    .btn-batalla>button { background: linear-gradient(180deg, #e74c3c, #c0392b) !important; color: white !important; }

    /* Cartas de Brawlers */
    .pin-card {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        border: 2px solid rgba(255,255,255,0.2);
        margin-bottom: 10px;
    }
    .pin-img { width: 90px; filter: drop-shadow(0 0 8px rgba(255,255,255,0.5)); }
    .vs-txt { font-size: 70px; color: #f1c40f; text-align: center; margin-top: 80px; text-shadow: 0 0 20px #f1c40f; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. LÓGICA DE PANTALLAS
# ==========================================

# --- LOGIN ---
if 'player_name' not in st.session_state:
    st.markdown("<h1 style='text-align:center; font-size: 80px;'>BRAWL PINS</h1>", unsafe_allow_html=True)
    name = st.text_input("TU NOMBRE:", placeholder="USUARIO...")
    if st.button("ENTRAR AL SERVIDOR"):
        if name.strip():
            st.session_state.player_name = name.strip().upper()
            data = load_user_data(st.session_state.player_name)
            if data: st.session_state.update(data)
            else:
                st.session_state.update({"coins": 500, "gems": 50, "my_brawlers": {"Shelly": 0}})
                save_player_data()
            st.rerun()
    st.stop()

# --- PANTALLA DE BATALLA (SELECCIÓN) ---
if st.session_state.phase == 'battle_select':
    st.markdown("<h1 style='text-align:center;'>MODOS DE JUEGO</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='pin-card'><h3>1. BRAWLER</h3></div>", unsafe_allow_html=True)
        b_sel = st.selectbox("", list(st.session_state.my_brawlers.keys()))
        st.session_state.selected_brawler = b_sel
        st.markdown(f"<div style='text-align:center;'><img src='{BRAWLERS[b_sel]['img']}' style='width:160px;'></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='pin-card'><h3>2. EVENTO</h3></div>", unsafe_allow_html=True)
        m_sel = st.selectbox("", list(MODOS.keys()))
        st.markdown(f"<div class='pin-card'><h2>{m_sel}</h2><p style='font-size:20px;'>RECOMPENSA: {MODOS[m_sel]['cups']}🏆</p></div>", unsafe_allow_html=True)
    
    st.write("---")
    if st.button("¡BUSCAR PARTIDA! 🥊", use_container_width=True):
        st.session_state.selected_modo = m_sel
        st.session_state.phase = 'matchmaking'
        st.rerun()
    if st.button("VOLVER AL INICIO"):
        st.session_state.phase = 'idle'
        st.rerun()
    st.stop()

# --- MATCHMAKING 3VS3 CON ICONOS ---
if st.session_state.phase == 'matchmaking':
    st.markdown(f"<h1 style='text-align:center;'>{st.session_state.selected_modo}</h1>", unsafe_allow_html=True)
    c1, cvs, c2 = st.columns([2,1,2])
    with c1:
        st.markdown(f"<div class='pin-card'><img src='{BRAWLERS[st.session_state.selected_brawler]['img']}' class='pin-img'><br><b style='font-size:20px;'>{st.session_state.player_name}</b></div>", unsafe_allow_html=True)
        for _ in range(2):
            bot_b = random.choice(list(BRAWLERS.keys()))
            st.markdown(f"<div class='pin-card'><img src='{BRAWLERS[bot_b]['img']}' class='pin-img'><br>{random.choice(BOT_NAMES)}</div>", unsafe_allow_html=True)
    with cvs: st.markdown("<p class='vs-txt'>VS</p>", unsafe_allow_html=True)
    with c2:
        for _ in range(3):
            bot_b = random.choice(list(BRAWLERS.keys()))
            st.markdown(f"<div class='pin-card'><img src='{BRAWLERS[bot_b]['img']}' class='pin-img'><br>{random.choice(BOT_NAMES)}</div>", unsafe_allow_html=True)
    
    time.sleep(2.5)
    if st.button("¡ENTRAR A LA ARENA!"):
        win = random.random() < 0.55
        m = MODOS[st.session_state.selected_modo]
        b = st.session_state.selected_brawler
        if win:
            st.session_state.my_brawlers[b] += m['cups']
            st.session_state.coins += int(45 * m['mult'])
            st.session_state.last_match = {"win":True, "cups":m['cups'], "coins":int(45*m['mult']), "brawler":b}
        else:
            lost = -4 if st.session_state.my_brawlers[b] > 10 else 0
            st.session_state.my_brawlers[b] += lost
            st.session_state.last_match = {"win":False, "cups":lost, "coins":0, "brawler":b}
        save_player_data()
        st.session_state.phase = 'result'
        st.rerun()
    st.stop()

# --- PANTALLA FINAL (RESULTADOS) ---
if st.session_state.phase == 'result':
    res = st.session_state.last_match
    st.markdown(f"<div style='text-align:center;'><img src='{BRAWLERS[res['brawler']]['img']}' style='width:220px;'></div>", unsafe_allow_html=True)
    if res['win']:
        st.markdown(f"<h1 style='text-align:center; color:#2ecc71; font-size:80px;'>VICTORIA</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>+{res['cups']} 🏆 | +{res['coins']} 💰</h2>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h1 style='text-align:center; color:#e74c3c; font-size:80px;'>DERROTA</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{res['cups']} 🏆</h2>", unsafe_allow_html=True)
    
    if st.button("VOLVER AL MENÚ PRINCIPAL", use_container_width=True):
        st.session_state.phase = 'idle'
        st.rerun()
    st.stop()

# --- TIENDA ---
if st.session_state.phase == 'tienda':
    st.header("🛒 TIENDA ESTELAR")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='pin-card'><h3>📦 CAJA BRAWL</h3><p>100 💰</p></div>", unsafe_allow_html=True)
        if st.button("ABRIR CAJA"):
            if st.session_state.coins >= 100:
                st.session_state.coins -= 100
                if random.random() < 0.20:
                    disponibles = [b for b in BRAWLERS.keys() if b not in st.session_state.my_brawlers]
                    if disponibles:
                        new = random.choice(disponibles)
                        st.session_state.my_brawlers[new] = 0
                        st.balloons(); st.success(f"¡NUEVO BRAWLER: {new}!")
                save_player_data(); st.rerun()
    if st.button("CERRAR TIENDA"):
        st.session_state.phase = 'idle'
        st.rerun()
    st.stop()

# ==========================================
# 5. MENÚ PRINCIPAL (HUD Y COLECCIÓN)
# ==========================================
st.markdown(f"""
    <div class='hud-bar'>
        <div class='hud-val'>👤 {st.session_state.player_name}</div>
        <div class='hud-val'>💰 {st.session_state.coins}</div>
        <div class='hud-val'>💎 {st.session_state.gems}</div>
        <div class='hud-val'>🏆 {sum(st.session_state.my_brawlers.values())}</div>
    </div>
""", unsafe_allow_html=True)

col_t, col_b = st.columns(2)
with col_t:
    st.markdown("<div class='nav-btn btn-tienda'>", unsafe_allow_html=True)
    if st.button("🛒 TIENDA", use_container_width=True):
        st.session_state.phase = 'tienda'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_b:
    st.markdown("<div class='nav-btn btn-batalla'>", unsafe_allow_html=True)
    if st.button("⚔️ BATALLA", use_container_width=True):
        st.session_state.phase = 'battle_select'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.subheader("👤 TU COLECCIÓN")
cols = st.columns(4)
for i, (name, cups) in enumerate(st.session_state.my_brawlers.items()):
    with cols[i % 4]:
        st.markdown(f"""
            <div class='pin-card'>
                <img src='{BRAWLERS[name]['img']}' class='pin-img'>
                <p><b>{name}</b><br>🏆 {cups}</p>
            </div>
        """, unsafe_allow_html=True)
