import streamlit as st
import random
import time
from logic import BRAWLERS, calcular_resultado_copas, check_luck

st.set_page_config(page_title="Brawl Sim 2020", layout="centered")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .shake { animation: shake-anim 0.5s infinite; width: 200px; }
    @keyframes shake-anim { 0% {transform: rotate(0deg)} 25% {transform: rotate(5deg)} 75% {transform: rotate(-5deg)} 100% {transform: rotate(0deg)} }
    .glow { color: #00ffff; text-shadow: 0 0 20px #00ffff; font-size: 100px; text-align: center; animation: pulse 0.5s infinite; }
    @keyframes pulse { 0% {opacity: 0.6} 100% {opacity: 1} }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN ---
if 'total_trophies' not in st.session_state:
    st.session_state.update({'coins': 1000, 'my_brawlers': {"Shelly": 0}, 'phase': 'menu', 'items': 0, 'reward': False})

# --- NAVEGACIÓN ---
menu = st.sidebar.radio("Navegación", ["Menú", "Tienda", "Batalla"])

if menu == "Menú":
    st.title("🌵 Inicio")
    total = sum(st.session_state.my_brawlers.values())
    st.metric("🏆 Trofeos Totales", total)
    cols = st.columns(3)
    for i, (name, trophies) in enumerate(st.session_state.my_brawlers.items()):
        with cols[i % 3]:
            st.image(BRAWLERS[name]['img'], width=80)
            st.write(f"**{name}**\n🏆 {trophies}")

elif menu == "Tienda":
    st.title("📦 Cajas")
    if st.button("🔴 Abrir Megacaja"):
        st.session_state.reward = check_luck("Mega")
        st.session_state.items = 6 if st.session_state.reward else 5
        st.session_state.phase = 'opening'
    
    if st.session_state.phase == 'opening':
        st.markdown('<center><img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Y2Z2R6b3BqZ3Z4bmE1eHpxeHpxeHpxeHpxeHpxeHpxeHpxJnZXB0PXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1z/3o7TKMGpxx6r3G9G76/giphy.gif" class="shake"></center>', unsafe_allow_html=True)
        if st.session_state.items > 1:
            st.write(f"## {st.session_state.items}")
        else:
            st.markdown('<p class="glow">1</p>', unsafe_allow_html=True)
        
        if st.button("TAP 🔓"):
            if st.session_state.items > 1:
                st.session_state.items -= 1
            else:
                if st.session_state.reward:
                    nuevo = random.choice(list(BRAWLERS.keys()))
                    st.session_state.my_brawlers[nuevo] = st.session_state.my_brawlers.get(nuevo, 0)
                    st.balloons()
                    st.success(f"¡NUEVO!: {nuevo}")
                st.session_state.phase = 'menu'

elif menu == "Batalla":
    st.title("⚔️ Partida Rápida")
    brawler = st.selectbox("Selecciona Brawler", list(st.session_state.my_brawlers.keys()))
    if st.button("¡BUSCAR PARTIDA!"):
        with st.spinner("Buscando..."):
            time.sleep(1.5)
        victoria = random.random() < 0.5
        puntos = calcular_resultado_copas(st.session_state.my_brawlers[brawler], victoria)
        st.session_state.my_brawlers[brawler] = max(0, st.session_state.my_brawlers[brawler] + puntos)
        if victoria: st.success(f"¡Ganaste! +{puntos} 🏆"); st.balloons()
        else: st.error(f"Perdiste... {puntos} 🏆")
