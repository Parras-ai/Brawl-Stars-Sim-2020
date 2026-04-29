import streamlit as st
import random
import time
import requests

# ==========================================
# 1. CONEXIÓN A TU NUBE DE GOOGLE (FIREBASE) ☁️
# ==========================================
FIREBASE_URL = "https://brawlsim-b5ed8-default-rtdb.europe-west1.firebasedatabase.app"

def load_user_data(username):
    """Descarga el perfil del jugador desde tu Firebase"""
    url = f"{FIREBASE_URL}/jugadores/{username}.json"
    try:
        res = requests.get(url)
        if res.status_code == 200 and res.json() is not None:
            return res.json()
    except: pass
    return None

def save_player_data():
    """Sube el progreso del jugador a tu Firebase"""
    url = f"{FIREBASE_URL}/jugadores/{st.session_state.player_name}.json"
    data = {
        "coins": st.session_state.coins,
        "gems": st.session_state.gems,
        "my_brawlers": st.session_state.my_brawlers
    }
    try:
        requests.put(url, json=data)
    except: pass

# ==========================================
# 2. DATOS DE LOS BRAWLERS
# ==========================================
BRAWLERS = {
    "Shelly": {"img": "https://cdn.brawlify.com/brawler/Shelly.png"},
    "Nita": {"img": "https://cdn.brawlify.com/brawler/Nita.png"},
    "Colt": {"img": "https://cdn.brawlify.com/brawler/Colt.png"},
    "Leon": {"img": "https://cdn.brawlify.com/brawler/Leon.png"},
    "Mortis": {"img": "https://cdn.brawlify.com/brawler/Mortis.png"},
    "Crow": {"img": "https://cdn.brawlify.com/brawler/Crow.png"}
}

# ==========================================
# 3. DISEÑO Y ESTILOS (LILITA FONT)
# ==========================================
st.set_page_config(page_title="Brawl Sim Global", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lilita+One&display=swap');
    html, body, [class*="st-at"], .stButton>button { 
        font-family: 'Lilita One', cursive !important; 
        text-transform: uppercase; 
    }
    .stApp { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; }
    .stat-card { background-color: rgba(0,0,0,0.6); padding: 15px; border-radius: 15px; border: 3px solid white; text-align: center; font-size: 24px; }
    .stButton>button { background-color: #f1c40f; color: black; border: 4px solid black; font-size: 22px; width: 100%; box-shadow: 0 5px #9e7e00; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. PANTALLA DE LOGIN
# ==========================================
if 'player_name' not in st.session_state:
    st.markdown("<h1 style='text-align:center; font-size: 70px;'>🌍 BRAWL SIM GLOBAL</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>ESTADO DEL SERVIDOR: EN LÍNEA ✅</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        name = st.text_input("", placeholder="NOMBRE DE USUARIO...", max_chars=12)
        if st.button("¡ENTRAR AL SERVIDOR! 🚀"):
            if name.strip():
                clean_name = name.strip().upper()
                st.session_state.player_name = clean_name
                
                with st.spinner("Sincronizando con la nube..."):
                    user_data = load_user_data(clean_name)
                    
                if user_data:
                    st.session_state.coins = user_data["coins"]
                    st.session_state.gems = user_data["gems"]
                    st.session_state.my_brawlers = user_data["my_brawlers"]
                    st.success(f"¡BIENVENIDO DE NUEVO, {clean_name}!")
                else:
                    st.session_state.coins = 200
                    st.session_state.gems = 20
                    st.session_state.my_brawlers = {"Shelly": 0}
                    save_player_data()
                    st.info("¡NUEVA CUENTA REGISTRADA!")
                
                time.sleep(1)
                st.session_state.phase = 'idle'
                st.rerun()
            else:
                st.error("¡ESCRIBE UN NOMBRE!")
    st.stop()

# ==========================================
# 5. EL JUEGO (DASHBOARD)
# ==========================================
st.sidebar.title(f"👤 {st.session_state.player_name}")
menu = st.sidebar.radio("MENÚ", ["INICIO", "TIENDA", "BATALLA"])
if st.sidebar.button("CERRAR SESIÓN 🚪"):
    save_player_data()
    del st.session_state['player_name']
    st.rerun()

c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='stat-card'>💰 {st.session_state.coins}</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='stat-card'>💎 {st.session_state.gems}</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='stat-card'>🏆 {sum(st.session_state.my_brawlers.values())}</div>", unsafe_allow_html=True)

st.divider()

if menu == "INICIO":
    st.header("TUS BRAWLERS")
    cols = st.columns(3)
    for i, (name, trophies) in enumerate(st.session_state.my_brawlers.items()):
        with cols[i % 3]:
            st.image(BRAWLERS[name]['img'], width=130)
            st.subheader(name)
            st.write(f"🏆 {trophies}")

elif menu == "TIENDA":
    st.header("CAJAS")
    t1, t2 = st.columns(2)
    with t1:
        st.markdown("<h1 style='text-align:center;'>🟦</h1>", unsafe_allow_html=True)
        if st.button("CAJA BRAWL (100 💰)"):
            if st.session_state.coins >= 100:
                st.session_state.coins -= 100
                st.session_state.reward = random.random() < 0.10
                st.session_state.items = 3 if st.session_state.reward else 2
                st.session_state.phase = 'opening'
                save_player_data()
                st.rerun()
    with t2:
        st.markdown("<h1 style='text-align:center;'>🧰</h1>", unsafe_allow_html=True)
        if st.button("MEGACAJA (80 💎)"):
            if st.session_state.gems >= 80:
                st.session_state.gems -= 80
                st.session_state.reward = random.random() < 0.30
                st.session_state.items = 6 if st.session_state.reward else 5
                st.session_state.phase = 'opening'
                save_player_data()
                st.rerun()

    if st.session_state.phase == 'opening':
        st.write("---")
        st.markdown(f"<h1 style='text-align:center; font-size:100px;'>{st.session_state.items}</h1>", unsafe_allow_html=True)
        if st.button("PULSAR PANTALLA 🔓"):
            if st.session_state.items > 1:
                st.session_state.items -= 1
                st.session_state.coins += random.randint(10, 40)
                st.rerun()
            else:
                if st.session_state.reward:
                    unlockable = [b for b in BRAWLERS.keys() if b not in st.session_state.my_brawlers]
                    if unlockable:
                        new_b = random.choice(unlockable)
                        st.session_state.my_brawlers[new_b] = 0
                        st.balloons(); st.success(f"¡NUEVO BRAWLER: {new_b}!")
                    else: st.info("BRAWLER REPETIDO: +200 💰"); st.session_state.coins += 200
                st.session_state.phase = 'idle'
                save_player_data()
                time.sleep(2); st.rerun()

elif menu == "BATALLA":
    st.header("COMBATE")
    sel = st.selectbox("ELEGIR BRAWLER:", list(st.session_state.my_brawlers.keys()))
    st.image(BRAWLERS[sel]['img'], width=180)
    if st.button("¡BUSCAR PARTIDA! 🥊"):
        with st.spinner("JUGANDO..."): time.sleep(1)
        win = random.random() < 0.55
        if win:
            st.session_state.my_brawlers[sel] += 8
            st.session_state.coins += random.randint(25, 55)
            st.success("¡VICTORIA! +8 🏆"); st.balloons()
        else:
            st.session_state.my_brawlers[sel] = max(0, st.session_state.my_brawlers[sel] - 4)
            st.error("DERROTA -4 🏆")
        save_player_data()
        time.sleep(1.5); st.rerun()
