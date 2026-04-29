import streamlit as st
import random
import time
from logic import BRAWLERS, PRECIOS, calcular_resultado_copas, check_luck

# Configuración de pantalla
st.set_page_config(page_title="Brawl Simulator All-in-One", layout="wide")

# --- FONDO Y ESTILOS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
    }
    .main-card {
        background-color: rgba(0, 0, 0, 0.4);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #f1c40f;
    }
    .stat-box {
        font-size: 24px;
        font-weight: bold;
        text-shadow: 2px 2px #000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN ---
if 'coins' not in st.session_state:
    st.session_state.update({
        'coins': 500, 'gems': 50, 'my_brawlers': {"Shelly": 0},
        'phase': 'idle', 'items': 0, 'reward': False
    })

# --- CABECERA DE RECURSOS ---
st.title("🏆 Brawl Stars Sim 2020")
res1, res2, res3 = st.columns(3)
res1.markdown(f"<p class='stat-box'>💰 Monedas: {st.session_state.coins}</p>", unsafe_allow_html=True)
res2.markdown(f"<p class='stat-box'>💎 Gemas: {st.session_state.gems}</p>", unsafe_allow_html=True)
res3.markdown(f"<p class='stat-box'>🏆 Copas: {sum(st.session_state.my_brawlers.values())}</p>", unsafe_allow_html=True)

st.divider()

# --- TODO EN UNA PANTALLA (Tabs) ---
tab_batalla, tab_tienda, tab_coleccion = st.tabs(["⚔️ BATALLA", "🛒 TIENDA", "👤 COLECCIÓN"])

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
            st.rerun()

with tab_tienda:
    st.subheader("Cajas Disponibles")
    t1, t2 = st.columns(2)
    
    with t1:
        st.image("https://static.wikia.nocookie.net/brawlstars/images/0/07/Big_Box.png", width=100)
        if st.button(f"Caja Brawl (100 Monedas)"):
            if st.session_state.coins >= 100:
                st.session_state.coins -= 100
                st.session_state.reward = check_luck("Brawl")
                st.session_state.items = 3 if st.session_state.reward else 2
                st.session_state.phase = 'opening'
                st.rerun()
            else: st.error("No tienes suficientes monedas")

    with t2:
        st.image("https://static.wikia.nocookie.net/brawlstars/images/e/e0/Mega_Box.png", width=120)
        if st.button(f"MEGACAJA (80 Gemas)"):
            if st.session_state.gems >= 80:
                st.session_state.gems -= 80
                st.session_state.reward = check_luck("Mega")
                st.session_state.items = 6 if st.session_state.reward else 5
                st.session_state.phase = 'opening'
                st.rerun()
            else: st.error("No tienes suficientes gemas")

    # Lógica de apertura dentro de la pestaña de tienda
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
                    nuevo = random.choice(list(BRAWLERS.keys()))
                    if nuevo not in st.session_state.my_brawlers:
                        st.session_state.my_brawlers[nuevo] = 0
                        st.balloons()
                        st.success(f"¡BRUTAL! Te ha tocado {nuevo.upper()}")
                    else:
                        st.info(f"Repetido: {nuevo} (+200 monedas)")
                        st.session_state.coins += 200
                else:
                    st.warning("Solo monedas esta vez...")
                st.session_state.phase = 'idle'
                time.sleep(2)
                st.rerun()

with tab_coleccion:
    st.subheader("Tu Álbum de Brawlers")
    cols_c = st.columns(3)
    for i, (b_name, b_copas) in enumerate(st.session_state.my_brawlers.items()):
        with cols_c[i % 3]:
            st.image(BRAWLERS[b_name]['img'], width=100)
            st.markdown(f"**{b_name}**")
            st.markdown(f"🏆 {b_copas} | Rango {int(b_copas/100)}")
