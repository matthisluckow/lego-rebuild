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

# --- SESSION STATE (HUSKER DINE MØNTER OG XP) ---
if 'coins' not in st.session_state:
    st.session_state['coins'] = 12 # Start mønter
if 'xp' not in st.session_state:
    st.session_state['xp'] = 450   # Start XP
if 'level' not in st.session_state:
    st.session_state['level'] = 4  # Start Level

# --- FUNKTION: BEREGN LEVEL ---
def check_levelup():
    # Hvis man har mere end 600 XP, stiger man i level
    if st.session_state['xp'] >= 600:
        st.session_state['level'] += 1
        st.session_state['xp'] = st.session_state['xp'] - 600 # Nulstil (eller fortsæt)
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
    
    # Status bar (Dynamisk XP)
    current_xp = st.session_state['xp']
    st.caption(f"Din Bygge-status (Level {st.session_state['level']}):")
    # Vi sikrer at progress bar ikke crasher ved at holde værdien mellem 0.0 og 1.0
    progress_val = min(max(current_xp / 600, 0.0), 1.0)
    st.progress(progress_val, text=f"{current_xp} / 600 XP til næste level")
    
    # Mønter og XP (Henter fra session_state nu)
    c1, c2 = st.columns(2)
    c1.metric("⭐ XP", f"{current_xp}", "Level op")
    c2.metric("💰 Mønter", f"{st.session_state['coins']}", "Shop")
    
    st.write("---")
    st.write("**Dine Badges:**")
    
    b1, b2 = st.columns(2)
    b1.success("🚀 Rum-ekspert")
    b2.info("♻️ Genbrugs-helt")
    
    st.write("")
    if st.button("Luk Profil"):
        st.rerun()

# --- FUNKTION: VISNING AF MANUAL + UPLOAD AF FÆRDIGT BYGGERI ---
@st.dialog("Byggevejledning: X-Wing Fighter")
def vis_byggevejledning():
    manual_path = BASE_DIR / "x-wing-manual.pdf"
    
    # --- FANEBLADE: MANUAL VS. FÆRDIG ---
    tab1, tab2 = st.tabs(["📖 Vejledning", "📸 Færdig?"])
    
    with tab1:
        if manual_path.exists():
            with open(manual_path, "rb") as f:
                pdf_data = f.read()
            
            st.download_button(
                label="📱 Åbn manual i fuld skærm",
                data=pdf_data,
                file_name="x-wing-manual.pdf",
                mime="application/pdf",
                use_container_width=True,
                icon="📥"
            )
            st.divider()
            st.write("**Forhåndsvisning:**")
            pdf_viewer(str(manual_path))
        else:
            st.error("Kunne ikke finde manualen.")

    with tab2:
        st.header("Vis os dit mesterværk!")
        st.info("Upload et billede af din færdige model for at få din belønning.")
        
        # Upload af det færdige resultat
        finished_img = st.file_uploader("Upload billede af din X-Wing", type=['jpg', 'png'], key="finished_upload")
        
        if finished_img:
            st.image(finished_img, caption="Dit flotte byggeri!", width=200)
            st.balloons() # FEST!
            
            # Opdater mønter og XP (kun visuelt i denne session)
            # Vi bruger en lille "hack" så man ikke får point hver gang siden genindlæses
            if 'reward_claimed' not in st.session_state: 
                st.session_state['coins'] += 50
                st.session_state['xp'] += 100
                st.session_state['reward_claimed'] = True
                check_levelup() # Tjek om vi steg i level
            
            st.success("🎉 TILLYKKE! Du har optjent:")
            
            # Vis belønningen flot i to kolonner
            r1, r2 = st.columns(2)
            r1.metric("Mønter", "+50", "💰")
            r2.metric("XP", "+100", "⭐")
            
            st.write(f"Din nye saldo: **{st.session_state['coins']} Mønter**")
            
            if st.button("Gå til Shop for at bruge dem"):
                st.toast("Åbner shoppen... (Demo)", icon="🛒")

# --- HOVEDSKÆRM: HERO SECTION ---
st.markdown(
    f"""
    <div style="display:flex; align-items:center; gap:12px;">
      <img src="{LEGO_LOGO_URL}" width="72"/>
      <h1 style="margin:0; padding:0;">LEGO ReBuild</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Giv dine gamle klodser nyt liv!")

# --- INFO BOKS OM MØNTER (GAMIFICATION INTRO) ---
with st.container(border=True):
    c_icon, c_text = st.columns([1, 5])
    c_icon.markdown("# 🏆")
    c_text.markdown("""
    **Bliv en Master Builder!**
    1. Scan din bunke (+10 XP & Mønter)
    2. Byg og upload billede (+100 XP & +50 Mønter)
    """)

# --- PROFIL KNAP ---
if st.button("👤 Åbn Min Profil", type="primary"):
    vis_profil()

# --- TRIN 1: AI SCANNEREN ---
st.write("---")
st.header("📸 1. Scan din bunke")

st.info("Tag et billede af dine løse klodser på gulvet.")

uploaded_file = st.file_uploader("Upload billede", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Din bunke", use_container_width=True)
    
    with st.status("🤖 AI analyserer klodser...", expanded=True) as status:
        st.write("Identificerer former og farver...")
        time.sleep(1.5)
        st.write("Matcher med LEGO databasen...")
        time.sleep(1.5)
        status.update(label="Scanning Færdig! ✅", state="complete", expanded=False)
        
    # GAMIFICATION FEEDBACK
    st.toast("Du fik 10 XP og 10 Mønter!", icon="⭐")

    st.success("Vi fandt **432 klodser** i din bunke! Her er hvad du kan bygge:")

    # --- TRIN 2: BYGGEFORSLAG ---
    st.write("---")
    st.header("🚀 2. Vælg dit eventyr")

    col1, col2 = st.columns(2)

    with col1:
        img_path = BASE_DIR / "x-wing.png"
        if img_path.exists():
            st.image(str(img_path), caption="Rumskib", use_container_width=True)
        else:
            st.info("Mangler billede: x-wing.png")
            
        st.write("**X-Wing Fighter (Mini)**")
        st.progress(100, text="Du har 100% af klodserne")
        
        # Tydeliggør belønningen
        st.caption("🏆 +100 XP | +50 Mønter")
        if st.button("BYG NU (Gratis)", key="btn1"):
            vis_byggevejledning()

    with col2:
        img_path_castle = BASE_DIR / "lego-castle-kongens-borg-lego-70404.webp"
        if img_path_castle.exists():
            st.image(str(img_path_castle), caption="Middelalderslot", use_container_width=True)
        else:
            st.info("Mangler billede: lego-castle...")
            
        st.write("**Ridderborg tårn**")
        st.progress(85, text="Du har 85% af klodserne")
        st.warning("Mangler: 12 klodser")
        
        st.write("**Pris for manglende dele:** 24 DKK")
        st.caption("🏆 +150 XP | +100 Mønter")
        if st.button("Køb manglende + BYG", key="btn2"):
            st.toast('Klodser tilføjet til kurv!', icon='🛒')
            st.write("📦 Levering: 2-3 dage")
            
    st.write("---")
    st.write("👀 *Dine venner byggede dette i dag:*")
    st.caption("Elias (9 år) byggede en dinosaur af sine gamle City-sæt.")
    st.image(str(BASE_DIR / "lego-dinosaur.png"), caption="Dinosaur af Elias", use_container_width=True)
else:
    st.write("👆 Start med at uploade et billede for at se magien.")
