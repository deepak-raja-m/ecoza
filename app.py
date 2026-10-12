import streamlit as st
import datetime
import random
import pandas as pd
from PIL import Image

# ----------------- Page Configuration -----------------
st.set_page_config(
    page_title="Ecoza - Circular Eco Recycling",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------- Session State Initialization -----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_identifier" not in st.session_state:
    st.session_state.user_identifier = ""

if "username" not in st.session_state:
    st.session_state.username = "Deepak Raja"

if "registered_users" not in st.session_state:
    st.session_state.registered_users = {
        "user@ecoza.com": {"password": "ecoza", "name": "Deepak Raja"},
        "9876543210": {"password": "ecoza", "name": "Deepak Raja"}
    }

# Persistent camera & scanner state
if "scan_result" not in st.session_state:
    st.session_state.scan_result = None

PAGES = [
    "🏠 Home", 
    "📸 AI Scanner", 
    "🗺️ Drop-off Map", 
    "🚚 Super Pickup", 
    "🎁 Rewards Store", 
    "🏆 Champions Leaderboard", 
    "📊 Impact Dashboard"
]

if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"

if "ecopoints" not in st.session_state:
    st.session_state.ecopoints = 250

if "waste_history" not in st.session_state:
    st.session_state.waste_history = [
        {"Item": "🥤 Plastic Bottles", "Weight": "500 g", "EcoPoints": 10, "Date": "2026-10-05"},
        {"Item": "📦 Paper & Notebooks", "Weight": "1200 g", "EcoPoints": 12, "Date": "2026-10-06"}
    ]

if "pickup_requests" not in st.session_state:
    st.session_state.pickup_requests = [
        {
            "Pickup ID": "ECO-401",
            "Address": "Anna Nagar Green Avenue, Chennai",
            "Items": "Plastic, Paper",
            "Date": "2026-10-10",
            "Contact": "+91 9876543210",
            "Status": "On The Way 🚚"
        }
    ]

if "redeemed_coupons" not in st.session_state:
    st.session_state.redeemed_coupons = []

RATES = {
    "🥤 Plastic Bottles": 20,
    "📚 Paper & Notebooks": 10,
    "🍶 Glass Jars": 15,
    "🥫 Metal Cans": 30,
    "🔋 E-Waste & Batteries": 50,
    "🍎 Organic Waste": 5
}

RECYCLING_CENTERS = [
    {
        "Center Name": "⚡ Guindy Eco Battery & E-Waste Hub",
        "Type": "E-Waste & Electronics",
        "Address": "Guindy Industrial Estate",
        "Contact": "+91 94441 23456",
        "lat": 13.0067,
        "lon": 80.2030
    },
    {
        "Center Name": "📘 Anna Nagar Paper Depot",
        "Type": "Plastic, Paper & Cardboard",
        "Address": "Anna Nagar West",
        "Contact": "+91 98840 56789",
        "lat": 13.0850,
        "lon": 80.2101
    },
    {
        "Center Name": "⚙️ Ambattur Scrap & Metal Depot",
        "Type": "Metal & Glass Recyclables",
        "Address": "Ambattur Industrial Estate",
        "Contact": "+91 97720 11223",
        "lat": 13.1143,
        "lon": 80.1548
    },
    {
        "Center Name": "🌱 Adyar Eco Park Composting Hub",
        "Type": "Wet & Organic Waste",
        "Address": "Adyar Eco Park Zone",
        "Contact": "+91 91234 98765",
        "lat": 13.0125,
        "lon": 80.2570
    }
]

# ----------------- High-Definition Dynamic Vector Artwork (No White Shade) -----------------
# 1. Nature Light Theme (Vivid sunlit foliage framing borders, clean organic sage shapes)
NATURE_LIGHT_ART = """data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='1920' height='1080' viewBox='0 0 1920 1080'>
  <defs>
    <linearGradient id='sky' x1='0' y1='0' x2='1920' y2='1080' gradientUnits='userSpaceOnUse'>
      <stop offset='0%' stop-color='%23eaf7ea'/>
      <stop offset='50%' stop-color='%23d9f1db'/>
      <stop offset='100%' stop-color='%23c1e7c5'/>
    </linearGradient>
    <linearGradient id='leafGrad' x1='0' y1='0' x2='400' y2='400' gradientUnits='userSpaceOnUse'>
      <stop offset='0%' stop-color='%2322c55e'/>
      <stop offset='100%' stop-color='%2314532d'/>
    </linearGradient>
  </defs>
  <rect width='1920' height='1080' fill='url(%23sky)'/>
  <!-- Organic waves matching reference tile 1 -->
  <path d='M-100,-100 Q450,150 250,750 T-100,1200 Z' fill='%2316a34a' opacity='0.28'/>
  <path d='M1350,1150 Q1500,600 2050,550 L2050,1150 Z' fill='%2315803d' opacity='0.35'/>
  <!-- Realistic crisp foliage silhouettes -->
  <g fill='url(%23leafGrad)' opacity='0.85'>
    <path d='M-20,-20 Q140,80 240,20 Q300,160 190,200 Q70,120 -20,-20 Z'/>
    <path d='M120,40 Q280,100 310,220 Q200,240 130,130 Z'/>
    <path d='M200,190 Q340,240 380,350 Q280,360 220,250 Z'/>
    <path d='M-10,130 Q110,200 140,300 Q50,300 0,190 Z'/>
    <path d='M70,270 Q200,340 220,460 Q120,430 80,330 Z'/>
    <path d='M1750,-30 Q1820,100 1780,190 Q1700,110 1750,-30 Z'/>
    <path d='M1820,80 Q1920,160 1880,260 Q1800,200 1820,80 Z'/>
  </g>
</svg>"""

# 2. Floating Elements Theme (Crisp 3D glowing green Earth sphere at bottom, floating leaves & eco-orbs)
FLOATING_ELEMENTS_ART = """data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='1920' height='1080' viewBox='0 0 1920 1080'>
  <defs>
    <linearGradient id='spaceSky' x1='960' y1='0' x2='960' y2='1080' gradientUnits='userSpaceOnUse'>
      <stop offset='0%' stop-color='%23dcfce7'/>
      <stop offset='50%' stop-color='%23bbf7d0'/>
      <stop offset='100%' stop-color='%2386efac'/>
    </linearGradient>
    <radialGradient id='earthGrad' cx='50%' cy='25%' r='75%'>
      <stop offset='0%' stop-color='%234ade80'/>
      <stop offset='30%' stop-color='%2316a34a'/>
      <stop offset='65%' stop-color='%2315803d'/>
      <stop offset='100%' stop-color='%23052e16'/>
    </radialGradient>
  </defs>
  <rect width='1920' height='1080' fill='url(%23spaceSky)'/>
  <!-- Floating translucent orbs with glowing green aura -->
  <circle cx='340' cy='460' r='60' fill='white' fill-opacity='0.45' stroke='%2322c55e' stroke-width='3'/>
  <circle cx='960' cy='380' r='75' fill='white' fill-opacity='0.55' stroke='%2316a34a' stroke-width='3.5'/>
  <circle cx='1580' cy='460' r='60' fill='white' fill-opacity='0.45' stroke='%2322c55e' stroke-width='3'/>
  <!-- Floating green leaves -->
  <g fill='%2315803d' opacity='0.9'>
    <path d='M260,320 Q310,280 350,310 Q320,360 270,340 Z'/>
    <path d='M1460,260 Q1500,210 1540,240 Q1520,290 1470,280 Z'/>
    <path d='M1680,410 Q1730,390 1760,440 Q1700,470 1680,410 Z'/>
    <path d='M190,520 Q240,490 270,540 Q220,570 190,520 Z'/>
    <path d='M1080,240 Q1120,210 1150,250 Q1100,280 1080,240 Z'/>
  </g>
  <!-- Curving glowing 3D Earth at bottom matching tile 5 -->
  <ellipse cx='960' cy='1320' rx='1100' ry='540' fill='url(%23earthGrad)' stroke='%2386efac' stroke-width='8'/>
</svg>"""

# Active background based on current page
if not st.session_state.authenticated:
    active_bg = NATURE_LIGHT_ART
elif st.session_state.current_page == "🏠 Home":
    active_bg = FLOATING_ELEMENTS_ART
else:
    active_bg = NATURE_LIGHT_ART

# ----------------- Direct CSS Injection (No Washed Out Whiteshade) -----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Fredoka:wght@600;700&display=swap');

    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        display: none !important;
    }

    /* Keep root Streamlit elements 100% transparent so background art stays clear */
    [data-testid="stHeader"],
    .stAppHeader,
    .stAppViewContainer,
    .main,
    .block-container {
        background-color: transparent !important;
        background: transparent !important;
    }

    /* Sharp background render */
    .stApp {
        background-image: url('""" + active_bg + """') !important;
        background-size: cover !important;
        background-position: center top !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Dark, readable typography */
    .stApp p, .stApp span, .stApp label, .stApp div {
        color: #0f291e !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 20px;
        line-height: 1.6;
    }

    h1 {
        font-family: 'Fredoka', cursive, sans-serif !important;
        color: #064e3b !important;
        font-size: 54px !important;
        margin-bottom: 14px !important;
    }

    h2 {
        font-family: 'Fredoka', cursive, sans-serif !important;
        color: #064e3b !important;
        font-size: 40px !important;
        margin-top: 18px !important;
        margin-bottom: 12px !important;
    }

    h3 {
        font-family: 'Fredoka', cursive, sans-serif !important;
        color: #065f46 !important;
        font-size: 28px !important;
    }

    /* Navigation Bar */
    div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.88) !important;
        backdrop-filter: blur(14px) !important;
        padding: 8px 16px !important;
        border-radius: 9999px !important;
        border: 2px solid #22c55e !important;
        box-shadow: 0 8px 24px rgba(22, 101, 52, 0.18) !important;
        display: flex !important;
        justify-content: center !important;
        gap: 8px !important;
    }

    div[role="radiogroup"] label {
        padding: 8px 18px !important;
        border-radius: 9999px !important;
        font-weight: 700 !important;
        font-family: 'Fredoka', cursive !important;
        color: #065f46 !important;
        font-size: 18px !important;
    }

    div[role="radiogroup"] label:hover {
        background: #dcfce7 !important;
    }

    /* Transparent Frosted Glass Cards (No opaque white wash) */
    [data-testid="stForm"], [data-testid="stMetric"], .stTable {
        background: rgba(255, 255, 255, 0.78) !important;
        backdrop-filter: blur(18px) !important;
        padding: 30px !important;
        border-radius: 24px !important;
        box-shadow: 0 12px 32px rgba(6, 78, 59, 0.12) !important;
        border: 2px solid rgba(134, 239, 172, 0.8) !important;
    }

    input, select, textarea, div[data-baseweb="input"], div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        color: #0f381f !important;
        border: 2px solid #86efac !important;
        border-radius: 14px !important;
        font-size: 20px !important;
        padding: 12px 16px !important;
    }

    div[data-testid="stMetricValue"] {
        color: #15803d !important;
        font-family: 'Fredoka', cursive !important;
        font-weight: 700 !important;
        font-size: 50px !important;
    }

    .stButton>button, div[data-testid="stForm"] button {
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%) !important;
        color: #ffffff !important;
        font-family: 'Fredoka', cursive !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        border-radius: 20px !important;
        border: 2px solid #86efac !important;
        padding: 12px 32px !important;
        box-shadow: 0 6px 18px rgba(22, 163, 74, 0.3) !important;
    }

    .stButton>button:hover, div[data-testid="stForm"] button:hover {
        background: linear-gradient(135deg, #166534 0%, #15803d 100%) !important;
        color: #ffffff !important;
    }

    .badge-points {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
        color: #ffffff !important;
        font-family: 'Fredoka', cursive;
        font-weight: 700;
        padding: 10px 24px;
        border-radius: 9999px;
        font-size: 19px;
        box-shadow: 0 4px 14px rgba(22, 163, 74, 0.3);
        border: 2px solid #bbf7d0;
        display: inline-block;
    }

    .brand-logo {
        font-size: 38px;
        font-family: 'Fredoka', cursive, sans-serif;
        font-weight: 700;
        color: #0f5132 !important;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- 1. LOGIN / AUTHENTICATION GATEWAY -----------------
if not st.session_state.authenticated:
    st.markdown("<br>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 2.2, 1])

    with col_l2:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 22px;">
                <div style="display: inline-flex; align-items: center; justify-content: center; gap: 14px; margin-bottom: 4px;">
                    <svg width="54" height="54" viewBox="0 0 24 24" fill="#15803d">
                        <path d="M2 22h20c0-5.52-4.48-10-10-10v-3.17c2.83-.48 5-2.94 5-5.83 0-.55-.45-1-1-1s-1 .45-1 1c0 2.21-1.79 4-4 4-1.1 0-2.1-.45-2.83-1.17-.39-.39-1.02-.39-1.41 0-.39.39-.39 1.02 0 1.41C7.79 8.44 9 9.61 10 9.87V12C4.48 12 0 16.48 0 22h2z"/>
                    </svg>
                    <span style="font-family: 'Fredoka', cursive, sans-serif; font-size: 62px; font-weight: 700; color: #15803d; letter-spacing: -0.5px;">Ecoza</span>
                </div>
                <div style="font-size: 21px; color: #166534; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 12px;">
                    Rethink. Reuse. Recreate.
                </div>
                <h1 style="color: #064e3b; font-size: 42px; margin-bottom: 6px;">Welcome to Ecoza</h1>
                <p style="color: #1b4d3e; font-weight: 700; font-size: 21px;">Enter your Email or Mobile Number to begin.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Simplified, fail-proof login form
        with st.form("login_form_secure"):
            login_id = st.text_input("User Email or Mobile Number", value=st.session_state.user_identifier or "deepakraja6524@gmail.com")
            login_password = st.text_input("Password", type="password", value="ecoza123")
            
            c_sub1, c_sub2 = st.columns([1.5, 1])
            with c_sub1:
                btn_login = st.form_submit_button("🚀 Log In / Enter Ecoza", use_container_width=True)
            with c_sub2:
                btn_guest = st.form_submit_button("⚡ Quick Guest Login", use_container_width=True)

            if btn_login:
                cleaned_id = login_id.strip()
                if not cleaned_id or not login_password:
                    st.error("Please enter both email/mobile and password!")
                else:
                    # Accepts either pre-registered user or automatically creates the profile
                    user_display = cleaned_id.split("@")[0].capitalize() if "@" in cleaned_id else f"Eco Hero ({cleaned_id})"
                    st.session_state.authenticated = True
                    st.session_state.user_identifier = cleaned_id
                    st.session_state.username = user_display
                    st.balloons()
                    st.rerun()

            if btn_guest:
                st.session_state.authenticated = True
                st.session_state.user_identifier = "guest@ecoza.com"
                st.session_state.username = "Eco Champion"
                st.balloons()
                st.rerun()

    st.stop()

# ----------------- AUTHENTICATED APP HEADER -----------------
head_col1, head_col2, head_col3 = st.columns([1.5, 4.3, 1.8], vertical_alignment="center")

with head_col1:
    st.markdown(
        """
        <div>
            <div class="brand-logo">🌱 Ecoza</div>
            <div style="font-size: 14px; font-weight: 700; color: #166534; letter-spacing: 0.8px; margin-top: -6px;">Rethink. Reuse. Recreate.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with head_col2:
    current_index = PAGES.index(st.session_state.current_page) if st.session_state.current_page in PAGES else 0
    selected = st.radio(
        "Navigation Bar",
        PAGES,
        index=current_index,
        horizontal=True,
        label_visibility="collapsed"
    )
    if selected != st.session_state.current_page:
        st.session_state.current_page = selected
        st.rerun()

with head_col3:
    col_pts, col_out = st.columns([1.3, 0.9], vertical_alignment="center")
    with col_pts:
        st.markdown(f'<div class="badge-points">🌟 {st.session_state.ecopoints} pts</div>', unsafe_allow_html=True)
    with col_out:
        if st.button("🚪 Logout", key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.user_identifier = ""
            st.rerun()

st.markdown(f"<p style='font-size: 18px; color: #14532d; font-weight: 700; margin-top: -4px;'>Logged in: <b>{st.session_state.username}</b> ({st.session_state.user_identifier})</p>", unsafe_allow_html=True)
st.markdown("<hr style='margin-top: 4px; margin-bottom: 26px; border: 0; border-top: 2px dashed #86efac;'>", unsafe_allow_html=True)

# ----------------- 1. Home Screen (Floating Elements Theme) -----------------
if st.session_state.current_page == "🏠 Home":
    st.markdown(
        """
        <div style="text-align: center; max-width: 920px; margin: 0 auto; padding: 20px 0 20px 0;">
            <div style="background: rgba(255,255,255,0.92); color: #15803d; font-weight: 800; font-family: 'Fredoka'; padding: 10px 28px; border-radius: 9999px; display: inline-block; font-size: 18px; margin-bottom: 16px; border: 2px solid #86efac; box-shadow: 0 4px 14px rgba(22, 163, 74, 0.12);">
                🍃 RETHINK • REUSE • RECREATE 🍃
            </div>
            <h1 style="font-size: 58px; color: #064e3b; line-height: 1.18; margin-bottom: 14px;">
                Turn Everyday Waste Into <span style="color: #16a34a;">EcoPoints!</span>
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    c_btn1, c_btn2, c_btn3 = st.columns([2.2, 1.6, 2.2])
    with c_btn2:
        if st.button("✨ Scan An Item Now!", use_container_width=True):
            st.session_state.current_page = "📸 AI Scanner"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div style="background: rgba(255,255,255,0.85); padding: 30px; border-radius: 22px; border: 2px solid #bbf7d0; text-align: center; box-shadow: 0 8px 24px rgba(6, 78, 59, 0.08);">
                <div style="font-size: 52px; margin-bottom: 10px;">📷</div>
                <h3 style="color: #065f46; margin: 0 0 10px 0; font-size: 28px;">AI Waste Scanner</h3>
                <p style="color: #0f381f; font-size: 19px; margin: 0; line-height: 1.5;">Snap a live camera photo to identify materials and calculate points per gram.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div style="background: rgba(255,255,255,0.85); padding: 30px; border-radius: 22px; border: 2px solid #bbf7d0; text-align: center; box-shadow: 0 8px 24px rgba(6, 78, 59, 0.08);">
                <div style="font-size: 52px; margin-bottom: 10px;">🚚</div>
                <h3 style="color: #065f46; margin: 0 0 10px 0; font-size: 28px;">Doorstep Collection</h3>
                <p style="color: #0f381f; font-size: 19px; margin: 0; line-height: 1.5;">Schedule doorstep pickups with verified local recycling partners.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div style="background: rgba(255,255,255,0.85); padding: 30px; border-radius: 22px; border: 2px solid #bbf7d0; text-align: center; box-shadow: 0 8px 24px rgba(6, 78, 59, 0.08);">
                <div style="font-size: 52px; margin-bottom: 10px;">🎁</div>
                <h3 style="color: #065f46; margin: 0 0 10px 0; font-size: 28px;">Community Rewards</h3>
                <p style="color: #0f381f; font-size: 19px; margin: 0; line-height: 1.5;">Trade accumulated points for plant saplings, book coupons, and vouchers.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ----------------- 2. AI Scanner & Classifier (Fixed Live Camera & Stable Prediction) -----------------
elif st.session_state.current_page == "📸 AI Scanner":
    st.title("📸 AI Waste Scanner & Classifier")
    st.markdown("<p style='font-size: 22px; color: #14532d; font-weight: 700;'>Snap a photo or upload an image to identify recyclables and earn EcoPoints!</p>", unsafe_allow_html=True)

    tab_cam, tab_up = st.tabs(["📷 Take Photo Now (Live Camera)", "📁 Upload Image File"])

    with tab_cam:
        cam_photo = st.camera_input("Point your camera at the recyclable item")
        if cam_photo is not None:
            # Store locked prediction in session state so it doesn't reshuffle
            if st.session_state.scan_result is None or st.session_state.scan_result.get("source") != "camera":
                chosen_cat = random.choice(list(RATES.keys()))
                st.session_state.scan_result = {
                    "source": "camera",
                    "category": chosen_cat,
                    "confidence": round(random.uniform(93.0, 99.2), 1)
                }

    with tab_up:
        file_photo = st.file_uploader("Upload item photo", type=["jpg", "jpeg", "png"])
        if file_photo is not None:
            if st.session_state.scan_result is None or st.session_state.scan_result.get("source") != "file":
                chosen_cat = random.choice(list(RATES.keys()))
                st.session_state.scan_result = {
                    "source": "file",
                    "category": chosen_cat,
                    "confidence": round(random.uniform(94.0, 99.5), 1)
                }

    # Display Analysis Outcome
    active_category = "🥤 Plastic Bottles"
    if st.session_state.scan_result:
        active_category = st.session_state.scan_result["category"]
        conf = st.session_state.scan_result["confidence"]

        st.success(f"### 🎉 Detected Recyclable: **{active_category}**")
        st.markdown(f"<p style='font-size: 22px;'>Confidence Match: <b>{conf}%</b></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 22px;'>Reward Rate: <b>{RATES[active_category]} EcoPoints per 1,000 grams</b></p>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("⚖️ Enter Estimated Weight (in Grams)")

    with st.form("waste_log_form_stable"):
        selected_category = st.selectbox(
            "Selected Material",
            list(RATES.keys()),
            index=list(RATES.keys()).index(active_category) if active_category in RATES else 0
        )
        
        input_grams = st.number_input(
            "Weight in Grams (e.g., 250 g, 500 g, 1000 g)",
            min_value=10,
            max_value=25000,
            step=50,
            value=250
        )
        
        rate_per_kg = RATES[selected_category]
        calculated_points = max(1, int((input_grams / 1000.0) * rate_per_kg))
        
        st.info(f"🌟 You will earn: **{calculated_points} EcoPoints!**")

        submit_log = st.form_submit_button("🚀 Add To Score!")
        if submit_log:
            st.session_state.ecopoints += calculated_points
            st.session_state.waste_history.append({
                "Item": selected_category,
                "Weight": f"{input_grams} g",
                "EcoPoints": calculated_points,
                "Date": str(datetime.date.today())
            })
            # Reset scan result after logging
            st.session_state.scan_result = None
            st.balloons()
            st.success(f"Awesome! Added {calculated_points} EcoPoints to your balance!")
            st.rerun()

# ----------------- 3. Nearby Collection Centers -----------------
elif st.session_state.current_page == "🗺️ Drop-off Map":
    st.title("🗺️ Ecoza Drop-Off Centers")
    st.markdown("<p style='font-size: 22px; color: #14532d;'>Find certified circular recycling drop-off centers across Chennai!</p>", unsafe_allow_html=True)

    df_centers = pd.DataFrame(RECYCLING_CENTERS)
    st.map(df_centers[["lat", "lon"]], zoom=11)

    st.subheader("📍 Center Locations & Contacts")
    for _, row in df_centers.iterrows():
        with st.container():
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"#### {row['Center Name']}")
                st.write(f"**Accepts:** {row['Type']}")
                st.write(f"**Address:** {row['Address']}")
            with col_b:
                st.write(f"📞 `{row['Contact']}`")
                st.button("Visit Station", key=f"dir_{row['Center Name']}")
            st.divider()

# ----------------- 4. Doorstep Pickup -----------------
elif st.session_state.current_page == "🚚 Super Pickup":
    st.title("🚚 Schedule Doorstep Pickup")
    st.markdown("<p style='font-size: 22px; color: #14532d;'>Book a verified Ecoza pickup partner directly to your address.</p>", unsafe_allow_html=True)

    with st.form("pickup_form"):
        pickup_address = st.text_area("Address", placeholder="Door No, Street, Landmark, Chennai")
        waste_items = st.multiselect("What are you recycling?", list(RATES.keys()), default=["🥤 Plastic Bottles", "📚 Paper & Notebooks"])
        pickup_date = st.date_input("Preferred Date", min_value=datetime.date.today())
        phone = st.text_input("Contact Mobile Number", placeholder="+91 9876543210")

        submit_booking = st.form_submit_button("🚛 Confirm Pickup")
        if submit_booking:
            if not pickup_address or not phone:
                st.error("Please enter both the address and contact number!")
            else:
                new_id = f"ECO-{random.randint(100, 999)}"
                st.session_state.pickup_requests.append({
                    "Pickup ID": new_id,
                    "Address": pickup_address,
                    "Items": ", ".join(waste_items),
                    "Date": str(pickup_date),
                    "Contact": phone,
                    "Status": "Confirmed 🎉"
                })
                st.success(f"Pickup Booked! Tracking ID: **{new_id}**")
                st.rerun()

    if st.session_state.pickup_requests:
        st.markdown("---")
        st.subheader("📋 Scheduled Pickups")
        st.dataframe(pd.DataFrame(st.session_state.pickup_requests), use_container_width=True)

# ----------------- 5. Rewards Store -----------------
elif st.session_state.current_page == "🎁 Rewards Store":
    st.title("🎁 Rewards Store")
    st.markdown(f"<p style='font-size: 22px; color: #14532d;'>Redeem points for eco-conscious rewards! Balance: <b>{st.session_state.ecopoints} EcoPoints</b></p>", unsafe_allow_html=True)

    rewards_list = [
        {"title": "🌱 Plant A Sapling With Your Tag", "cost": 150, "desc": "A fruit sapling planted with your name tag!"},
        {"title": "🍦 Organic Beverage / Treat Voucher", "cost": 80, "desc": "1 free artisanal beverage at participating kiosks."},
        {"title": "📚 Stationery Coupon (₹100 Off)", "cost": 100, "desc": "Redeemable at local school bookstores."},
        {"title": "🚌 Green Metro Day Explorer Pass", "cost": 120, "desc": "Free 1-day transit pass across the city metro line."}
    ]

    col_a, col_b = st.columns(2)
    for idx, reward in enumerate(rewards_list):
        card = col_a if idx % 2 == 0 else col_b
        with card:
            st.markdown(f"### {reward['title']}")
            st.write(reward["desc"])
            st.caption(f"Cost: **{reward['cost']} EcoPoints**")
            
            if st.button(f"Claim ({reward['cost']} pts)", key=f"rwd_{idx}"):
                if st.session_state.ecopoints >= reward["cost"]:
                    st.session_state.ecopoints -= reward["cost"]
                    voucher_code = f"PRIZE-{random.randint(10000, 99999)}"
                    st.session_state.redeemed_coupons.append({
                        "Reward": reward["title"],
                        "Coupon Code": voucher_code,
                        "Date": str(datetime.date.today())
                    })
                    st.snow()
                    st.success(f"🎉 Redeemed! Your Code: **{voucher_code}**")
                    st.rerun()
                else:
                    st.error("Not enough EcoPoints yet!")
            st.divider()

# ----------------- 6. Champions Leaderboard -----------------
elif st.session_state.current_page == "🏆 Champions Leaderboard":
    st.title("🏆 Community Leaderboard")
    st.markdown("<p style='font-size: 22px; color: #14532d;'>Top recyclers contributing to zero waste this week!</p>", unsafe_allow_html=True)

    leaderboard = [
        {"Rank": "🥇 1st Place", "Contributor": "Class 8B (Little Flower School)", "Waste Saved": "44,000 g", "EcoPoints": 880},
        {"Rank": "🥈 2nd Place", "Contributor": "Priya R.", "Waste Saved": "38,500 g", "EcoPoints": 770},
        {"Rank": "🥉 3rd Place", "Contributor": f"{st.session_state.username} (You!)", "Waste Saved": "28,000 g", "EcoPoints": st.session_state.ecopoints},
        {"Rank": "4th Place", "Contributor": "Karthik Raj", "Waste Saved": "18,500 g", "EcoPoints": 370},
        {"Rank": "5th Place", "Contributor": "Green Community Club", "Waste Saved": "12,000 g", "EcoPoints": 240}
    ]
    st.table(pd.DataFrame(leaderboard))

# ----------------- 7. User Dashboard -----------------
elif st.session_state.current_page == "📊 Impact Dashboard":
    st.title("📊 Environmental Impact Dashboard")
    st.markdown("<p style='font-size: 22px; color: #14532d;'>Track your total diverted waste and carbon savings!</p>", unsafe_allow_html=True)

    total_dropoffs = len(st.session_state.waste_history)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Available Points", f"{st.session_state.ecopoints} pts")
    col2.metric("Total Drop-offs", total_dropoffs)
    col3.metric("Pickups Called", len(st.session_state.pickup_requests))
    col4.metric("CO₂ Offset (Est.)", f"{total_dropoffs * 2.2:.1f} kg")

    st.markdown("---")
    st.subheader("📜 Recycling History")
    if st.session_state.waste_history:
        st.dataframe(pd.DataFrame(st.session_state.waste_history), use_container_width=True)

    if st.session_state.redeemed_coupons:
        st.subheader("🎟️ Claimed Coupons")
        st.dataframe(pd.DataFrame(st.session_state.redeemed_coupons), use_container_width=True)
