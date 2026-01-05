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

# --- SESSION STATE (HUSKER DINE DATA) ---
if 'coins' not in st.session_state:
    st.session_state['coins'] = 12
if 'xp' not in st.session_state:
    st.session_state['xp'] = 450
if 'level' not in st.session_state:
    st.session_state['level'] = 4
if 'reward_claimed' not in st.session_state:
    st.session_state['reward_claimed'] = False
# NYT: Husker om vi har givet belønning for scanning
if 'scan_reward_given' not in st.session_state:
    st.session_state['scan_reward_given'] = False

# --- FUNKTION: BEREGN LEVEL ---
def check_levelup():
    if st.session_state['xp'] >= 600:
        st.session_state['level'] += 1
        st.session_state['xp'] -= 600
        st.toast(f"🎉 LEVEL UP! Du er nu Level {st.session_state['level']}!", icon="🆙")

# --- FUNKTION: PROFIL POP-UP ---
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
    
    c1, c2 = st.columns(2)
    c1.metric("⭐ XP", f"{current_xp}", "Level op")
    c2.metric("💰 Mønter", f"{st.session_state['coins']}", "Shop")
    
    st.write("---")
    st.write("**Dine Badges:**")
    b1, b2 = st.columns(2)
    b1.success("🚀 Rum-ekspert")
    b2.info("♻️ Genbrugs-helt")
    
    if st.button("Luk Profil"):
        st.rerun()

# --- FUNKTION: VISNING AF MANUAL + UPLOAD ---
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
            
            # Tjek om belønning allerede er givet for DETTE byggeri
            if not st.session_state['reward_claimed']:
                st.balloons()
                st.session_state['coins'] += 50
                st.session_state['xp'] += 100
                st.session_state['reward_claimed'] = True
                check_levelup()
                st.success("🎉 TILLYKKE! Du har optjent:")
            else:
                st.info("Du har allerede fået belønning for dette byggeri.")
            
            r1, r2 = st.columns(2)
            r1.metric("Mønter", "+50", "💰")
            r2.metric("XP", "+100", "⭐")
            
            if st.button("Gå til Shop"):
                st.toast("Åbner shoppen...", icon="🛒")

# --- HOVEDSKÆRM ---
st.markdown(
    f"""<div style="display:flex; align-items:center; gap:12px;">
      <img src="{LEGO_LOGO_URL}" width="72"/>
      <h1 style="margin:0; padding:0;">LEGO ReBuild</h1>
    </div>""", unsafe_allow_html=True
)

st.subheader("Giv dine gamle klodser nyt liv!")

# --- INFO BOKS (GAMIFICATION) ---
with st.container(border=True):
    c_icon, c_text = st.columns([1, 5])
    c_icon.markdown("# 🏆")
    c_text.markdown("""**Bliv en Master Builder!** 1. Scan din bunke (+10 XP & Mønter)  
    2. Byg og upload billede (+100 XP & +50 Mønter)""")

if st.button("👤 Åbn Min Profil", type="primary"):
    vis_profil()

# --- TRIN 1: SCANNER ---
st.write("---")
st.header("📸 1. Scan din bunke")
st.info("Tag et billede af dine løse klodser på gulvet.")

uploaded_file = st.file_uploader("Upload billede", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Din bunke", use_container_width=True)
    
    # RETTELSE: Vi kører kun analysen og belønningen ÉN gang
    if not st.session_state['scan_reward_given']:
        with st.status("🤖 AI analyserer klodser...", expanded=True) as status:
            time.sleep(1.0)
            st.write("Matcher med LEGO databasen...")
            time.sleep(1.0)
            status.update(label="Scanning Færdig! ✅", state="complete", expanded=False)
        
        # Giv belønning og gem status
        st.session_state['coins'] += 10
        st.session_state['xp'] += 10
        st.session_state['scan_reward_given'] = True # VIGTIGT: Nu er den markeret som "Givet"
        check_levelup()
        st.toast("Du fik 10 XP og 10 Mønter!", icon="⭐")

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
            if st.button("❤️ 12 Likes", key="like1"):
                st.toast("Du likede Elias' Dinosaur!", icon="❤️")

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
            if st.button("❤️ 28 Likes", key="like2"):
                st.toast("Du likede Sofias Drage!", icon="❤️")

else:
    # Hvis man fjerner billedet, nulstiller vi status, så man kan scanne igen
    st.session_state['scan_reward_given'] = False
    st.write("👆 Start med at uploade et billede for at se magien.")
