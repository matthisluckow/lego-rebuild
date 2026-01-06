import streamlit as st
import time
from pathlib import Path
from streamlit_pdf_viewer import pdf_viewer

# --- 1. OPSÆTNING ---
BASE_DIR = Path(__file__).resolve().parent
LEGO_LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/2/24/LEGO_logo.svg"

st.set_page_config(
    page_title="LEGO ReBuild", 
    page_icon="🟥", 
    layout="centered",
    initial_sidebar_state="expanded" # Vi åbner sidebaren så man ser menuen
)

# --- 2. SESSION STATE (DATA) ---
if 'coins' not in st.session_state:
    st.session_state['coins'] = 60 # Start med lidt flere mønter så vi kan teste shoppen
if 'xp' not in st.session_state:
    st.session_state['xp'] = 450
if 'level' not in st.session_state:
    st.session_state['level'] = 4
if 'reward_claimed' not in st.session_state:
    st.session_state['reward_claimed'] = False
if 'scan_reward_given' not in st.session_state:
    st.session_state['scan_reward_given'] = False
if 'likes_elias' not in st.session_state:
    st.session_state['likes_elias'] = 12
if 'likes_sofia' not in st.session_state:
    st.session_state['likes_sofia'] = 28
# NYT: Inventory til købte ting
if 'inventory' not in st.session_state:
    st.session_state['inventory'] = []

# --- 3. CSS (DESIGN) ---
st.markdown(
    """
    <style>
    /* Sticky Header til XP/Mønter */
    .sticky-header {
        position: fixed; top: 0; left: 0; width: 100%; height: 60px;
        background-color: rgba(255, 255, 255, 0.98);
        border-bottom: 3px solid #E3000B;
        z-index: 9999;
        display: flex; justify-content: center; align-items: center;
    }
    .header-content {
        display: flex; justify-content: space-between; align-items: center;
        width: 100%; max-width: 700px; padding: 0 20px;
    }
    .stat-pill {
        background-color: #f0f2f6; color: #31333F; padding: 5px 12px;
        border-radius: 15px; font-weight: bold; border: 1px solid #ddd;
    }
    /* Skub indhold ned */
    .main .block-container { padding-top: 80px !important; }
    header[data-testid="stHeader"] { display: none; }
    </style>
    """, unsafe_allow_html=True
)

# --- 4. FUNKTIONER ---

# Header (HUD)
def show_hud():
    st.markdown(
        f"""
        <div class="sticky-header">
            <div class="header-content">
                <div style="font-weight:800; font-size:18px; color:#E3000B;">Level {st.session_state['level']}</div>
                <div style="display:flex; gap:8px;">
                    <div class="stat-pill">⭐ {st.session_state['xp']} XP</div>
                    <div class="stat-pill">💰 {st.session_state['coins']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

def check_levelup():
    if st.session_state['xp'] >= 600:
        st.session_state['level'] += 1
        st.session_state['xp'] -= 600
        st.toast(f"🎉 LEVEL UP! Du er nu Level {st.session_state['level']}!", icon="🆙")

def add_like(person_key):
    st.session_state[person_key] += 1
    st.toast("Du sendte et like! ❤️", icon="😍")

@st.dialog("Byggevejledning: X-Wing Fighter")
def vis_byggevejledning():
    manual_path = BASE_DIR / "x-wing-manual.pdf"
    tab1, tab2 = st.tabs(["📖 Vejledning", "📸 Færdig?"])
    
    with tab1:
        if manual_path.exists():
            with open(manual_path, "rb") as f:
                pdf_data = f.read()
            st.download_button("📱 Åbn manual i fuld skærm", pdf_data, "manual.pdf", "application/pdf", use_container_width=True, icon="📥")
            st.divider()
            pdf_viewer(str(manual_path))
        else:
            st.error("Kunne ikke finde manualen.")

    with tab2:
        st.header("Vis os dit mesterværk!")
        finished_img = st.file_uploader("Upload billede", type=['jpg', 'png'], key="finished_upload")
        if finished_img:
            st.image(finished_img, width=200)
            if not st.session_state['reward_claimed']:
                st.balloons()
                st.session_state['coins'] += 50
                st.session_state['xp'] += 100
                st.session_state['reward_claimed'] = True
                check_levelup()
                st.rerun() # Opdater HUD
            else:
                st.info("Belønning allerede modtaget.")

# --- 5. NAVIGATION (SIDEBAR MENU) ---
show_hud() # Vis altid headeren

with st.sidebar:
    st.image(LEGO_LOGO_URL, width=100)
    st.title("Menu")
    
    # Her vælger vi hvilken side der skal vises
    page = st.radio("Gå til:", ["🏠 Hjem", "🛒 Shop & Kurv", "👤 Min Profil"])
    
    st.write("---")
    st.caption(f"Logget ind som: **Marcus (8 år)**")

# --- 6. SIDE LOGIK ---

# ==========================================
# SIDE 1: HJEM (Din originale app)
# ==========================================
if page == "🏠 Hjem":
    # Hero Section
    st.markdown(f"""<div style="display:flex; align-items:center; gap:12px;">
      <img src="{LEGO_LOGO_URL}" width="60"/>
      <h1 style="margin:0;">LEGO ReBuild</h1>
    </div>""", unsafe_allow_html=True)
    
    st.subheader("Giv dine gamle klodser nyt liv!")

    # Info Boks
    with st.container(border=True):
        c1, c2 = st.columns([1, 6])
        c1.markdown("# 🏆")
        c2.markdown("**Bliv en Master Builder!**\n1. 📸 Scan din bunke (+10 XP & Mønter)\n2. 🧱 Byg og upload (+100 XP & +50 Mønter)")

    # Scanner
    st.write("---")
    st.header("📸 1. Scan din bunke")
    uploaded_file = st.file_uploader("Upload billede", type=['jpg', 'png', 'jpeg'])

    if uploaded_file:
        st.image(uploaded_file, width=300)
        if not st.session_state['scan_reward_given']:
            with st.status("🤖 AI analyserer..."):
                time.sleep(1.5)
            st.session_state['coins'] += 10
            st.session_state['xp'] += 10
            st.session_state['scan_reward_given'] = True
            check_levelup()
            st.rerun()

        st.success("Vi fandt **432 klodser**! Her er byggeorslag:")
        
        # Byggeforslag
        st.write("---")
        st.header("🚀 2. Vælg dit eventyr")
        col1, col2 = st.columns(2)
        
        with col1:
            img_path = BASE_DIR / "x-wing.png"
            if img_path.exists(): st.image(str(img_path), use_container_width=True)
            st.write("**X-Wing Fighter**")
            st.caption("🏆 +100 XP | +50 Mønter")
            if st.button("BYG NU", key="btn1"):
                vis_byggevejledning()

        with col2:
            img_path_castle = BASE_DIR / "lego-castle-kongens-borg-lego-70404.webp"
            if img_path_castle.exists(): st.image(str(img_path_castle), use_container_width=True)
            st.write("**Ridderborg**")
            st.warning("Mangler: 12 klodser")
            if st.button("Køb manglende (24 kr)", key="btn2"):
                st.toast('Lagt i kurv!', icon='🛒')

        # Social
        st.write("---")
        st.subheader("🌟 Vennernes Galleri")
        sc1, sc2 = st.columns(2)
        with sc1:
            with st.container(border=True):
                st.write("**👦 Elias (9 år)**")
                img_dino = BASE_DIR / "lego-dinosaur.png"
                if img_dino.exists(): st.image(str(img_dino))
                st.button(f"❤️ {st.session_state['likes_elias']}", key="l1", on_click=add_like, args=('likes_elias',))
        with sc2:
            with st.container(border=True):
                st.write("**👧 Sofia (7 år)**")
                img_dragon = BASE_DIR / "den_grønne_drage.jpg"
                if img_dragon.exists(): st.image(str(img_dragon))
                st.button(f"❤️ {st.session_state['likes_sofia']}", key="l2", on_click=add_like, args=('likes_sofia',))

    else:
        st.info("👆 Start med at uploade et billede.")

# ==========================================
# SIDE 2: SHOP (NY SIDE!)
# ==========================================
elif page == "🛒 Shop & Kurv":
    st.header("🛒 LEGO Shoppen")
    st.write(f"Du har: **{st.session_state['coins']} Mønter** til at shoppe for.")
    
    st.divider()
    
    # Viser produkter i et grid
    col_p1, col_p2 = st.columns(2)
    
    # PRODUKT 1
    with col_p1:
        with st.container(border=True):
            st.markdown("# ⚜️") # Placeholder ikon
            st.write("**Guld-klods (Digital)**")
            st.caption("En sjælden badge til din profil.")
            st.write("**Pris: 50 Mønter**")
            
            if "Guld-klods" in st.session_state['inventory']:
                st.success("✅ Købt")
            else:
                if st.button("Køb nu", key="shop1"):
                    if st.session_state['coins'] >= 50:
                        st.session_state['coins'] -= 50
                        st.session_state['inventory'].append("Guld-klods")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Ikke nok mønter!")

    # PRODUKT 2
    with col_p2:
        with st.container(border=True):
            st.markdown("# 📜") # Placeholder ikon
            st.write("**Hemmelig Byggevejledning**")
            st.caption("Lås op for en unik robot-opskrift.")
            st.write("**Pris: 100 Mønter**")
            
            if "Robot-opskrift" in st.session_state['inventory']:
                st.success("✅ Købt")
            else:
                if st.button("Køb nu", key="shop2"):
                    if st.session_state['coins'] >= 100:
                        st.session_state['coins'] -= 100
                        st.session_state['inventory'].append("Robot-opskrift")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Ikke nok mønter!")

    st.write("---")
    st.subheader("🎒 Din Rygsæk (Inventory)")
    if len(st.session_state['inventory']) > 0:
        for item in st.session_state['inventory']:
            st.info(f"🔹 {item}")
    else:
        st.caption("Du har ikke købt noget endnu.")

# ==========================================
# SIDE 3: PROFIL (Flyttet til egen side)
# ==========================================
elif page == "👤 Min Profil":
    st.header("Min Bygmester Profil")
    
    col_prof1, col_prof2 = st.columns([1, 3])
    with col_prof1:
        st.image(LEGO_LOGO_URL, width=80)
    with col_prof2:
        st.subheader("Marcus (8 år)")
        st.write(f"**Level {st.session_state['level']} Master Builder**")
    
    st.write("---")
    st.write("### Statistik")
    m1, m2, m3 = st.columns(3)
    m1.metric("XP", st.session_state['xp'])
    m2.metric("Mønter", st.session_state['coins'])
    m3.metric("Likes givet", 5) # Bare et eksempel
    
    st.write("### Badges & Inventory")
    if "Guld-klods" in st.session_state['inventory']:
        st.markdown("### ⚜️ Guld-klods Ejer")
    
    st.success("🚀 Rum-ekspert")
    st.info("♻️ Genbrugs-helt")
