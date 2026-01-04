import streamlit as st
import time
import random
from pathlib import Path
from streamlit_pdf_viewer import pdf_viewer

# --- OPSÆTNING AF STI ---
BASE_DIR = Path(__file__).resolve().parent

LEGO_LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/2/24/LEGO_logo.svg"

# --- KONFIGURATION AF APPENS VIBE ---
# RETTELSE: Tilføjet initial_sidebar_state="collapsed" så man ser knappen med det samme!
st.set_page_config(
    page_title="LEGO ReBuild", 
    page_icon="🟥", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS HACK: TILPAS SIDEBAR KNAPPEN ---
st.markdown(
    """
    <style>
    /* 1. Selve knappen (når sidebaren er lukket) */
    [data-testid="stSidebarCollapsedControl"] {
        background-color: #E3000B !important; /* LEGO Rød */
        border: 2px solid white !important;
        border-radius: 8px !important;
        padding: 10px !important;
        
        /* Flexbox sikrer at pil og tekst står pænt på linje */
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        
        width: auto !important;
        height: auto !important;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.3) !important;
        
        /* Flyt knappen lidt ned/ind så den ikke sidder helt oppe i hjørnet */
        margin-top: 10px !important;
        margin-left: 10px !important;
    }

    /* 2. Teksten "Min Profil" */
    [data-testid="stSidebarCollapsedControl"]::after {
        content: "Min Profil" !important;
        font-weight: 800 !important; /* Extra bold */
        font-size: 16px !important;
        color: white !important;
        padding-right: 5px !important;
    }

    /* 3. Pil-ikonet */
    [data-testid="stSidebarCollapsedControl"] svg {
        fill: white !important;
        width: 20px !important;
        height: 20px !important;
    }

    /* 4. Hover effekt */
    [data-testid="stSidebarCollapsedControl"]:hover {
        background-color: #B30009 !important; /* Mørkere rød */
        transform: scale(1.05);
        transition: transform 0.2s;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- FUNKTION: VISNING AF MANUAL (MOBIL-VENLIG) ---
@st.dialog("Byggevejledning: X-Wing Fighter")
def vis_byggevejledning():
    """
    Viser en dialogboks med PDF.
    Inkluderer en download-knap for bedste mobil-oplevelse.
    """
    manual_path = BASE_DIR / "x-wing-manual.pdf"
    
    if manual_path.exists():
        # Læs filen ind til download-knappen
        with open(manual_path, "rb") as f:
            pdf_data = f.read()
            
        # 1. DOWNLOAD KNAP (VIGTIG FOR MOBIL)
        st.download_button(
            label="📱 Åbn manual i fuld skærm",
            data=pdf_data,
            file_name="x-wing-manual.pdf",
            mime="application/pdf",
            use_container_width=True, # Gør knappen bred
            icon="📥"
        )
        
        st.caption("Tip: Download filen for at kunne zoome helt ind på telefonen.")
        st.divider()

        # 2. FORHÅNDSVISNING (RESPONSIV)
        st.write("**Forhåndsvisning:**")
        # Vi udelader width/height, så den tilpasser sig pop-up vinduets bredde automatisk
        pdf_viewer(str(manual_path))
        
    else:
        st.error(f"Kunne ikke finde manualen: {manual_path.name}")
        st.info("Sørg for at 'x-wing-manual.pdf' ligger i samme mappe som denne python-fil.")

# --- SIDEBAR: NYT OG FORBEDRET DESIGN ---
with st.sidebar:
    st.image(LEGO_LOGO_URL, width=120)
    
    st.write("---") # En lille streg
    
    # 1. Tydelig overskrift som ønsket
    st.title("👤 Min Profil")
    
    # 2. "Kort-design" med ramme for at skabe blikfang
    with st.container(border=True):
        st.write("👋 **Hej Marcus (8 år)**")
        
        st.caption("Din Bygge-status:")
        st.progress(75, text="Level 4: Master Builder")
        
        col_xp, col_coin = st.columns(2)
        col_xp.metric("XP", "450", "+50")
        col_coin.metric("Mønter", "12", "Shop")
        
        st.write("**Dine Badges:**")
        st.markdown("🚀 *Rum-ekspert*")
        st.markdown("♻️ *Genbrugs-helt*")
        
    # 3. Tydelig knap (Primary gør den rød/udfyldt)
    if st.button("⚙️ Gå til Min Profil", type="primary", use_container_width=True):
        st.toast("Åbner profilindstillinger...", icon="👤")

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

# --- TRIN 1: AI SCANNEREN (The Tech) ---
st.write("---")
st.header("📸 1. Scan din bunke")
st.info("Tag et billede af dine løse klodser på gulvet.")

uploaded_file = st.file_uploader("Upload billede", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    # Viser det uploadede billede
    st.image(uploaded_file, caption="Din bunke", use_container_width=True)
    
    # Simulerer AI-analyse (Loading bar)
    with st.status("🤖 AI analyserer klodser...", expanded=True) as status:
        st.write("Identificerer former og farver...")
        time.sleep(1.5)
        st.write("Matcher med LEGO databasen...")
        time.sleep(1.5)
        st.write("Tjekker 'Pick-a-Brick' lagerstatus...")
        time.sleep(1.0)
        status.update(label="Scanning Færdig! ✅", state="complete", expanded=False)

    # Resultat af scanningen
    st.success("Vi fandt **432 klodser** i din bunke! Her er hvad du kan bygge:")

    # --- TRIN 2: BYGGEFORSLAG (The Solution) ---
    st.write("---")
    st.header("🚀 2. Vælg dit eventyr")

    col1, col2 = st.columns(2)

    # KOLONNE 1: X-WING
    with col1:
        # Tjekker om billedet findes, ellers viser placeholder tekst
        img_path = BASE_DIR / "x-wing.png"
        if img_path.exists():
            st.image(str(img_path), caption="Rumskib", use_container_width=True)
        else:
            st.info("Mangler billede: x-wing.png")
            
        st.write("**X-Wing Fighter (Mini)**")
        st.progress(100, text="Du har 100% af klodserne")
        
        # --- KNAPPEN DER ÅBNER MANUALEN ---
        if st.button("BYG NU (Gratis)", key="btn1"):
            vis_byggevejledning()

    # KOLONNE 2: BORGEN
    with col2:
        img_path_castle = BASE_DIR / "lego-castle-kongens-borg-lego-70404.webp"
        if img_path_castle.exists():
            st.image(str(img_path_castle), caption="Middelalderslot", use_container_width=True)
        else:
            st.info("Mangler billede: lego-castle...")
            
        st.write("**Ridderborg tårn**")
        st.progress(85, text="Du har 85% af klodserne")
        st.warning("Mangler: 12 klodser")
        
        # --- FORRETNINGSMODEL (Pick-a-Brick) ---
        st.write("**Pris for manglende dele:** 24 DKK")
        if st.button("Køb manglende + BYG", key="btn2"):
            st.toast('Klodser tilføjet til kurv!', icon='🛒')
            st.write("📦 Levering: 2-3 dage")

    # --- TRIN 3: SOCIAL PROOF / COMMUNITY ---
    st.write("---")
    st.write("👀 *Dine venner byggede dette i dag:*")
    st.caption("Elias (9 år) byggede en dinosaur af sine gamle City-sæt.")
    st.image(str(BASE_DIR / "lego-dinosaur.png"), caption="Dinosaur af Elias", use_container_width=True)
    st.caption("Sofia (7 år) skabte den grønne drage med sine klodser.")
    st.image(str(BASE_DIR / "den_grønne_drage.jpg"), caption="Drage af Sofia", use_container_width=True)
else:
    st.write("👆 Start med at uploade et billede for at se magien.")
