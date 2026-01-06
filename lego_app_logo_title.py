import streamlit as st
import time
import random
from pathlib import Path
from streamlit_pdf_viewer import pdf_viewer

# --- OPSÆTNING AF STI ---
BASE_DIR = Path(__file__).resolve().parent

LEGO_LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/2/24/LEGO_logo.svg"

# --- KONFIGURATION AF APPENS VIBE ---
st.set_page_config(
    page_title="LEGO ReBuild", 
    page_icon="🟥", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- SESSION STATE ---
if 'coins' not in st.session_state:
    st.session_state['coins'] = 12
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

# --- CSS: STICKY HEADER & DESIGN ---
st.markdown(
    """
    <style>
    /* 1. STICKY HEADER (HUD) */
    .sticky-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 70px;
        background-color: rgba(255, 255, 255, 0.98);
        border-bottom: 3px solid #E3000B;
        z-index: 999990; /* Ligger under knappen, men over indholdet */
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    
    @media (prefers-color-scheme: dark) {
        .sticky-header {
            background-color: rgba(14, 17, 23, 0.98);
            border-bottom: 3px solid #E3000B;
        }
    }

    /* Container indeni headeren */
    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        max-width: 700px;
        /* Vi laver plads til knappen i venstre side */
        padding-left: 170px; 
        padding-right: 10px;
    }

    /* Stat bokse (XP og Mønter) */
    .stat-pill {
        background-color: #f0f2f6;
        color: #31333F;
        padding: 5px 12px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 15px;
        display: flex;
        align-items: center;
        gap: 6px;
        border: 1px solid #ddd;
    }
    @media (prefers-color-scheme: dark) {
        .stat-pill {
            background-color: #262730;
            color: white;
            border: 1px solid #444;
        }
    }

    /* 2. KNAP PLACERING (CSS HACK) */
    /* Dette finder den første knap (Profil knappen) og tvinger den op i hjørnet */
    div[data-testid="stButton"]:first-of-type {
        position: fixed !important;
        top: 15px !important;
        z-index: 999999 !important; /* SKAL være højere end headeren */
    }

    /* På PC skærm: Placer relativt til midten */
    @media (min-width: 800px) {
        div[data-testid="stButton"]:first-of-type {
            left: 50% !important;
            margin-left: -350px !important; /* Rykker den til venstre kant af containeren */
        }
    }
    
    /* På Mobil: Sæt den fast i venstre side */
    @media (max-width: 799px) {
        div[data-testid="stButton"]:first-of-type {
            left: 10px !important;
        }
        .header-content {
            padding-left: 140px !important; /* Juster plads på mobil */
        }
    }

    /* 3. Skub resten af indholdet ned så det ikke gemmer sig bag headeren */
    .main .block-container {
        padding-top: 90px !important;
    }
    
    /* Skjul standard header */
    header[data-testid="stHeader"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- VIGTIGT: FUNKTIONER DEFINERES FØRST (SÅ PYTHON KENDER DEM) ---

def opdater_header():
    """Tegner headeren (HTML)"""
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
        """, 
        unsafe_allow_html=True
    )

def check_levelup():
    if st.session_state['xp'] >= 600:
        st.session_state['level'] += 1
        st.session_state['xp'] -= 600
        st.toast(f"🎉 LEVEL UP! Du er nu Level {st.session_state['level']}!", icon="🆙")
        # Vi behøver ikke kalde opdater_header her, da Streamlit reruns automatisk ved state change

def add_like(person_key):
    st.session_state[person_key] += 1
    st.toast("Du sendte et like! ❤️", icon="😍")

@st.dialog("👤 Min Bygmester Profil")
def vis_profil():
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(LEGO_LOGO_URL, width=60)
    with col2:
        st.write("### Hej Marcus (8 år) 👋")
    
    st.write("---")
    current_xp = st.session_state['xp']
    st.caption(f"Din Bygge-status (Level {st.session_state['level']}):")
    progress_val = min(max(current_xp / 600, 0.0), 1.0)
    st.progress(progress_val, text=f"{current_xp} / 600 XP til næste level")
    
    st.write("---")
    st.write("**Dine Badges:**")
    b1, b2 = st.columns(2)
    b1.success("🚀 Rum-ekspert")
    b2.info("♻️ Genbrugs-helt")
    
    if st.button("Luk Profil"):
        st.rerun()

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
        st.info("Upload et billede af din færdige model for at få din belønning.")
        finished_img = st.file_uploader("Upload billede", type=['jpg', 'png'], key="finished_upload")
        
        if finished_img:
            st.image(finished_img, caption="Dit flotte byggeri!", width=200)
            if not st.session_state['reward_claimed']:
                st.balloons()
                st.session_state['coins'] += 50
                st.session_state['xp'] += 100
                st.session_state['reward_claimed'] = True
                check_levelup()
                st.success("🎉 TILLYKKE! Du har optjent 100 XP og 50 Mønter!")
            else:
                st.info("Du har allerede fået belønning for dette byggeri.")
            
            if st.button("Gå til Shop"):
                st.toast("Åbner shoppen...", icon="🛒")

# --- HER STARTER SIDENS LOGIK (EFTER FUNKTIONER ER DEFINERET) ---

# 1. Tegn Headeren
opdater_header()

# 2. Tegn Knappen (Dette er den FØRSTE knap i koden, så CSS'en rammer den)
# Nu virker det, fordi vis_profil er defineret ovenfor!
if st.button("👤 Min Profil", type="primary"):
    vis_profil()

# --- HERO SECTION ---
st.markdown(
    f"""<div style="display:flex; align-items:center; gap:12px;">
      <img src="{LEGO_LOGO_URL}" width="72"/>
      <h1 style="margin:0; padding:0;">LEGO ReBuild</h1>
    </div>""", unsafe_allow_html=True
)

st.subheader("Giv dine gamle klodser nyt liv!")

# --- INFO BOKS ---
with st.container(border=True):
    col_icon, col_content = st.columns([1, 6])
    with col_icon:
        st.markdown("# 🏆")
    with col_content:
        st.markdown("### Bliv en Master Builder!")
        st.markdown("""
        1. 📸 **Scan din bunke** (+10 XP & Mønter)  
        2. 🧱 **Byg og upload billede** (+100 XP & +50 Mønter)
        """)

# --- TRIN 1: SCANNER ---
st.write("---")
st.header("📸 1. Scan din bunke")
st.info("Tag et billede af dine løse klodser på gulvet.")

uploaded_file = st.file_uploader("Upload billede", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Din bunke", use_container_width=True)
    
    if not st.session_state['scan_reward_given']:
        with st.status("🤖 AI analyserer klodser...", expanded=True) as status:
            time.sleep(1.0)
            st.write("Matcher med LEGO databasen...")
            time.sleep(1.0)
            status.update(label="Scanning Færdig! ✅", state="complete", expanded=False)
        
        st.session_state['coins'] += 10
        st.session_state['xp'] += 10
        st.session_state['scan_reward_given'] = True
        check_levelup()
        st.toast("Du fik 10 XP og 10 Mønter!", icon="⭐")
        st.rerun() # Opdater headeren med det samme

    st.success("Vi fandt **432 klodser** i din bunke! Her er hvad du kan bygge:")

    # --- TRIN 2: BYGGEFORSLAG ---
    st.write("---")
    st.header("🚀 2. Vælg dit eventyr")

    col1, col2 = st.columns(2)

    with col1:
        img_path = BASE_DIR / "x-wing.png"
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
        st.write("**X-Wing Fighter (Mini)**")
        st.progress(100, text="100% af klodserne")
        st.caption("🏆 +100 XP | +50 Mønter")
        if st.button("BYG NU (Gratis)", key="btn1"):
            vis_byggevejledning()

    with col2:
        img_path_castle = BASE_DIR / "lego-castle-kongens-borg-lego-70404.webp"
        if img_path_castle.exists():
            st.image(str(img_path_castle), use_container_width=True)
        st.write("**Ridderborg tårn**")
        st.progress(85, text="85% af klodserne")
        st.warning("Mangler: 12 klodser")
        st.caption("🏆 +150 XP | +100 Mønter")
        if st.button("Køb manglende", key="btn2"):
            st.toast('Lagt i kurv!', icon='🛒')

    # --- TRIN 3: SOCIAL COMMUNITY ---
    st.write("---")
    st.subheader("🌟 Vennernes Galleri")
    st.write("Se hvad andre børn har bygget i dag med deres gamle klodser!")

    social_col1, social_col2 = st.columns(2)

    with social_col1:
        with st.container(border=True):
            av1, txt1 = st.columns([1, 4])
            av1.markdown("## 👦")
            txt1.markdown("**Elias (9 år)**")
            txt1.caption("2 timer siden")
            
            img_dino = BASE_DIR / "lego-dinosaur.png"
            if img_dino.exists():
                st.image(str(img_dino), use_container_width=True)
            
            st.write("🦖 *\"Se min farlige dino!\"*")
            
            st.button(
                f"❤️ {st.session_state['likes_elias']} Likes", 
                key="like_elias", 
                on_click=add_like, 
                args=('likes_elias',)
            )

    with social_col2:
        with st.container(border=True):
            av2, txt2 = st.columns([1, 4])
            av2.markdown("## 👧")
            txt2.markdown("**Sofia (7 år)**")
            txt2.caption("4 timer siden")
            
            img_dragon = BASE_DIR / "den_grønne_drage.jpg"
            if img_dragon.exists():
                st.image(str(img_dragon), use_container_width=True)
                
            st.write("🐉 *\"Dragen passer på slottet\"*")
            
            st.button(
                f"❤️ {st.session_state['likes_sofia']} Likes", 
                key="like_sofia", 
                on_click=add_like, 
                args=('likes_sofia',)
            )

else:
    st.session_state['scan_reward_given'] = False
    st.write("👆 Start med at uploade et billede for at se magien.")
