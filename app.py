import streamlit as st
import json
import os
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="The Grays: Caliga Hall", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #d4af37; }
    div[data-testid="stMetricValue"] { color: #d4af37; }
    .char-box { border: 2px solid #d4af37; padding: 10px; border-radius: 10px; background: #1a1a1a; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER: CROP PORTRAITS FROM SHEET ---
def get_portrait(sheet_path, coords):
    img = Image.open(sheet_path)
    # Left, Upper, Right, Lower
    return img.crop((coords[0], coords[1], coords[2], coords[3]))

# --- LOAD DATA ---
with open('config.json') as f:
    config = json.load(f)

if 'loyalty' not in st.session_state:
    st.session_state.loyalty = {c['name']: 0 for c in config['characters']}
    st.session_state.funds = 1000
    st.session_state.heat = 10

# --- HEADER ---
st.title(f"🏛️ {config['gang_name']} Syndicate")
st.caption(f"{config['location']} | {config['year']}")

# --- STATUS BAR ---
stat1, stat2, stat3 = st.columns(3)
stat1.metric("Family Funds", f"${st.session_state.funds}")
stat2.write(f"Heat Level: {st.session_state.heat}%")
stat2.progress(st.session_state.heat / 100)
stat3.info("Objective: Maintain the Distillery")

st.divider()

# --- THE FAMILY GRID ---
st.header("The Grays Family")
cols = st.columns(6)

for i, char in enumerate(config['characters']):
    with cols[i]:
        # Extract portrait from your uploaded sheet
        try:
            portrait = get_portrait("assets/spritesheet.png", char['coords'])
            st.image(portrait, use_container_width=True)
        except:
            st.error("Sheet missing")
        
        st.subheader(char['name'])
        st.caption(char['role'])
        
        # Loyalty Hearts
        hearts = st.session_state.loyalty[char['name']] // 20
        st.write("❤️" * (hearts + 1))
        
        if st.button(f"Talk to {char['name']}", key=f"btn_{i}"):
            st.session_state.loyalty[char['name']] = min(100, st.session_state.loyalty[char['name']] + 5)
            st.toast(f"{char['name']} appreciated the conversation.")

st.divider()

# --- ACTIVITIES ---
col_left, col_right = st.columns(2)

with col_left:
    st.header("🌙 Moonshine Distillery")
    if st.button("Start 1912 Private Batch"):
        st.session_state.funds += 250
        st.session_state.heat += 15
        st.success("Batch sold in Saint Denis! +$250 (Heat Increased)")

with col_right:
    st.header("📜 Active Quests")
    st.write("- **Nik:** Clear the squatters near the creek.")
    st.write("- **Myles:** Deliver the payoff to the Rhodes Sheriff.")
    if st.button("Complete Family Errands"):
        st.session_state.heat = max(0, st.session_state.heat - 20)
        st.balloons()
