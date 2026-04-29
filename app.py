import streamlit as st
import random
import time
import requests

# ==========================================
# 1. CONEXIÓN A FIREBASE ☁️
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
        try:
            requests.put(url, json=data)
        except: pass

# ==========================================
# 2. INICIALIZACIÓN SEGURA
# ==========================================
if 'phase' not in st.session_state: st.session_state.phase = 'idle'
if 'items' not in st.session_state: st.session_state.items = 0
if 'reward' not in st.session_state: st.session_state.reward = False
if 'last_match' not in st.session_state: st.session_state.last_match = None

# ==========================================
# 3. DATOS DE LOS BRAWLERS (EMOJIS SEGUROS)
# ==========================================
BRAWLERS = {
    "Shelly": {"emoji": "🔫"},
    "Nita": {"emoji": "🐻"},
    "Colt": {"emoji": "🤠"},
    "Leon": {"emoji": "🦎"},
    "Mortis": {"emoji": "🦇"},
    "Crow": {"emoji": "🐦"}
}

# ==========================================
# 4. DISEÑO Y ESTILOS
# ==========================================
st.set_page_config(page_title="Brawl Sim Global", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lilita+One&display=swap');
    
    html, body, p, h1, h2, h3, .stButton>button { 
        font-family: 'Lilita One', cursive !important; 
        text-transform: uppercase; 
    }
    .emoji-safe {
        font-family: "Apple Color Emoji", "Segoe UI Emoji", Arial, sans-serif !important;
        font-size: 80px;
        text-align: center;
        margin-bottom: -10px;
    }
    .emoji-giant {
        font-family: "Apple Color Emoji", "Segoe UI Emoji", Arial, sans-serif !important;
        font-size: 150px;
        text-align: center;
    }
    .stApp { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; }
    .stat-card { background-color: rgba(0,0,0,0.6); padding: 15px; border-radius: 15px; border: 3px solid white; text-align: center; font-size: 24px; }
    .stButton>button { background-color: #f1c40f; color: black; border: 4px solid black; font-size: 22px; width: 100%; box-shadow: 0 5px #9e7e00; }
    
    /* Colores para la pantalla de victoria/derrota */
    .win-text { color: #2ecc71; text-shadow: 0 0 20px #2ecc71; font-size: 80px; text-align: center; margin-top: -20px;}
    .lose-text { color: #e74c3c; text-shadow: 0 0 20px #e74c3c; font-size: 80px; text-align: center; margin-top: -20px;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 5. PANTALLA DE LOGIN
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
                else:
                    st.session_state.coins = 200
                    st.session_state.gems = 20
                    st.session_state.my_brawlers = {"Shelly": 0}
                    save_player_data()
                
                st.session_state.phase = 'idle'
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("¡ESCRIBE UN NOMBRE!")
    st.stop()

# ==========================================
# 6. PANTALLA EXCLUSIVA DE RESULTADO DE BATALLA
# ==========================================
# Si la fase es 'battle_result', ocultamos todo el menú normal y mostramos solo esto
if st.session_state.phase == 'battle_result':
    res = st.session_state.last_match
    
    st.markdown(f"<div class='emoji-giant'>{BRAWLERS[res['brawler']]['emoji']}</div>", unsafe_allow_html=True)
    
    if res['win']:
        st.markdown("<p class='win-text'>¡VICTORIA!</p>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>+{res['cups']} 🏆 | +{res['coins']} 💰</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<p class='lose-text'>SUERTE LA PRÓXIMA</p>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{res['cups']} 🏆</h2>", unsafe_allow_html=True)
    
    st.write("---")
    colA, colB, colC = st.columns([1,2,1])
    with colB:
        if st.button("VOLVER A JUGAR 🔄"):
            # Devolvemos a la fase normal en la pestaña de Batalla
            st.session_state.phase = 'idle' 
            st.rerun()
            
    st.stop() # Esto evita que se dibuje el menú de abajo mientras estamos en esta pantalla

# ==========================================
# 7. EL JUEGO NORMAL (MENÚ Y DASHBOARD)
# ==========================================
st.sidebar.title(f"👤 {st.session_state.player_name}")
# Guardamos en qué pestaña estamos para que al "Volver a jugar" te deje en Batalla
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "INICIO"

menu = st.sidebar.radio("MENÚ", ["INICIO", "TIENDA", "BATALLA"], index=["INICIO", "TIENDA", "BATALLA"].index(st.session_state.current_menu))
st.session_state.current_menu = menu

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
            st.markdown(f"<div class='emoji-safe'>{BRAWLERS[name]['emoji']}</div>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align:center;'>{name}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center;'>🏆 {trophies}</p>", unsafe_allow_html=True)

elif menu == "TIENDA":
    st.header("CAJAS")
    t1, t2 = st.columns(2)
    with t1:
        st.markdown("<div class='emoji-safe'>🟦</div>", unsafe_allow_html=True)
        if st.button("CAJA BRAWL (100 💰)"):
            if st.session_state.coins >= 100:
                st.session_state.coins -= 100
                st.session_state.reward = random.random() < 0.20
                st.session_state.items = 3 if st.session_state.reward else 2
                st.session_state.phase = 'opening'
                save_player_data()
                st.rerun()
    with t2:
        st.markdown("<div class='emoji-safe'>🧰</div>", unsafe_allow_html=True)
        if st.button("MEGACAJA (80 💎)"):
            if st.session_state.gems >= 80:
                st.session_state.gems -= 80
                st.session_state.reward = random.random() < 0.40
                st.session_state.items = 6 if st.session_state.reward else 5
                st.session_state.phase = 'opening'
                save_player_data()
                st.rerun()

    if st.session_state.phase == 'opening':
        st.write("---")
        items_actuales = int(st.session_state.get('items', 0))
        st.markdown(f"<div class='emoji-safe'>{items_actuales}</div>", unsafe_allow_html=True)
        
        if st.button("PULSAR PANTALLA 🔓"):
            if items_actuales > 1:
                st.session_state.items = items_actuales - 1
                st.session_state.coins += random.randint(10, 40)
                st.rerun()
            else:
                if st.session_state.reward:
                    unlockable = [b for b in BRAWLERS.keys() if b not in st.session_state.my_brawlers]
                    if unlockable:
                        new_b = random.choice(unlockable)
                        st.session_state.my_brawlers[new_b] = 0
                        st.success(f"¡NUEVO BRAWLER: {new_b}!")
                    else: 
                        st.info("BRAWLER REPETIDO: +200 💰"); st.session_state.coins += 200
                else:
                    st.warning("SOLO RECURSOS...")
                st.session_state.phase = 'idle'
                save_player_data()
                time.sleep(1.5); st.rerun()

elif menu == "BATALLA":
    st.header("COMBATE")
    sel = st.selectbox("ELEGIR BRAWLER:", list(st.session_state.my_brawlers.keys()))
    st.markdown(f"<div class='emoji-safe'>{BRAWLERS[sel]['emoji']}</div>", unsafe_allow_html=True)
    
    if st.button("¡BUSCAR PARTIDA! 🥊"):
        with st.spinner("Luchando en la arena..."): 
            time.sleep(1.5)
        
        win = random.random() < 0.55
        if win:
            cups_won = 8
            coins_won = random.randint(25, 55)
            st.session_state.my_brawlers[sel] += cups_won
            st.session_state.coins += coins_won
            # Guardamos los datos de la partida para mostrarlos en la nueva pantalla
            st.session_state.last_match = {"win": True, "brawler": sel, "cups": cups_won, "coins": coins_won}
        else:
            cups_lost = -4 if st.session_state.my_brawlers[sel] > 0 else 0
            st.session_state.my_brawlers[sel] = max(0, st.session_state.my_brawlers[sel] + cups_lost)
            st.session_state.last_match = {"win": False, "brawler": sel, "cups": cups_lost, "coins": 0}
        
        save_player_data()
        
        # Activamos la pantalla exclusiva de resultados
        st.session_state.phase = 'battle_result'
        st.rerun()
