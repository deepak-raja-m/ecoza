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
    st.session_state.username = "Green Hero"

if "registered_users" not in st.session_state:
    st.session_state.registered_users = {
        "user@ecoza.com": {"password": "ecoza", "name": "Deepak Raja"},
        "9876543210": {"password": "ecoza", "name": "Deepak Raja"}
    }

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

# ----------------- Pure CSS Backgrounds Matching The Image -----------------
if not st.session_state.authenticated:
    # 1. Nature Light Theme (Organic sunlit wave shapes & natural green layers)
    theme_bg_css = """
    .stApp {
        background: 
            radial-gradient(circle at 10% 10%, rgba(134, 239, 172, 0.45) 0%, transparent 45%),
            radial-gradient(circle at 90% 15%, rgba(187, 247, 208, 0.40) 0%, transparent 45%),
            radial-gradient(circle at 85% 85%, rgba(22, 101, 52, 0.25) 0%, transparent 50%),
            linear-gradient(135deg, #f7fee7 0%, #ecfdf5 45%, #d1fae5 100%) !important;
        background-attachment: fixed !important;
    }
    """
elif st.session_state.current_page == "🏠 Home":
    # 5. Floating Elements Theme (Radiant bottom Earth sphere glow + floating mint orbs)
    theme_bg_css = """
    .stApp {
        background: 
            radial-gradient(circle at 50% 105%, #15803d 0%, #166534 30%, #064e3b 55%, transparent 75%),
            radial-gradient(circle at 15% 75%, rgba(34, 197, 94, 0.35) 0%, transparent 35%),
            radial-gradient(circle at 85% 75%, rgba(74, 222, 128, 0.35) 0%, transparent 35%),
            radial-gradient(circle at 20% 30%, rgba(187, 247, 208, 0.5) 0%, transparent 40%),
            radial-gradient(circle at 80% 35%, rgba(187, 247, 208, 0.5) 0%, transparent 40%),
            linear-gradient(180deg, #ecfdf5 0%, #d1fae5 60%, #bbf7d0 100%) !important;
        background-attachment: fixed !important;
    }
    """
elif st.session_state.current_page == "📸 AI Scanner":
    theme_bg_css = """
    .stApp {
        background: 
            radial-gradient(circle at 20% 20%, rgba(20, 184, 166, 0.25) 0%, transparent 40%),
            radial-gradient(circle at 80% 80%, rgba(13, 148, 136, 0.25) 0%, transparent 45%),
            linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 50%, #99f6e4 100%) !important;
        background-attachment: fixed !important;
    }
    """
elif st.session_state.current_page == "🗺️ Drop-off Map":
    # 3. Forest Lake Mountain Atmosphere
    theme_bg_css = """
    .stApp {
        background: 
            radial-gradient(circle at 50% 10%, rgba(254, 240, 138, 0.4) 0%, transparent 45%),
            radial-gradient(circle at 85% 90%, rgba(15, 118, 110, 0.35) 0%, transparent 50%),
            linear-gradient(180deg, #ecfeff 0%, #cffafe 45%, #a5f3fc 85%, #0f766e 100%) !important;
        background-attachment: fixed !important;
    }
    """
elif st.session_state.current_page == "🚚 Super Pickup":
    # 2. Minimal Organic Theme (Soft neutral sand and sage tones)
    theme_bg_css = """
    .stApp {
        background: 
            radial-gradient(circle at 10% 20%, rgba(220, 252, 231, 0.6) 0%, transparent 45%),
            radial-gradient(circle at 90% 80%, rgba(245, 245, 244, 0.9) 0%, transparent 50%),
            linear-gradient(135deg, #fafaf9 0%, #f5f5f4 50%, #e7e5e4 100%) !important;
        background-attachment: fixed !important;
    }
    """
elif st.session_state.current_page == "🎁 Rewards Store":
    theme_bg_css = """
    .stApp {
        background: 
            radial-gradient(circle at 15% 15%, rgba(253, 224, 71, 0.5) 0%, transparent 40%),
            radial-gradient(circle at 85% 85%, rgba(245, 158, 11, 0.3) 0%, transparent 50%),
            linear-gradient(135deg, #fffbeb 0%, #fef3c7 50%, #fde68a 100%) !important;
        background-attachment: fixed !important;
    }
    """
elif st.session_state.current_page == "🏆 Champions Leaderboard":
    # 4. Recycled Paper Theme (Warm kraft cardboard palette)
    theme_bg_css = """
    .stApp {
        background: 
            radial-gradient(circle at 80% 20%, rgba(214, 180, 138, 0.35) 0%, transparent 45%),
            radial-gradient(circle at 15% 85%, rgba(180, 142, 98, 0.3) 0%, transparent 45%),
            linear-gradient(135deg, #fefae0 0%, #faedcd 50%, #e9edc9 100%) !important;
        background-attachment: fixed !important;
    }
    """
else:  # 📊 Impact Dashboard
    theme_bg_css = """
    .stApp {
        background: 
            radial-gradient(circle at 50% 15%, rgba(134, 239, 172, 0.45) 0%, transparent 45%),
            linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #bbf7d0 100%) !important;
        background-attachment: fixed !important;
    }
    """

# Inject Dynamic CSS safely
st.markdown("<style>" + theme_bg_css + "</style>", unsafe_allow_html=True)

# ----------------- Static Layout & Typography Styling -----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Fredoka:wght@600;700&display=swap');

    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        display: none !important;
    }

    /* Keep all Streamlit inner wrappers transparent so the background renders fully */
    [data-testid="stHeader"],
    .stAppHeader,
    .stAppViewContainer,
    .main,
    .block-container {
        background-color: transparent !important;
        background: transparent !important;
    }

    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .stApp p, .stApp span, .stApp label, .stApp div {
        color: #143522;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 20px;
        line-height: 1.6;
    }

    h1 {
        font-family: 'Fredoka', cursive, sans-serif !important;
        letter-spacing: 0.3px;
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

    h4 {
        font-family: 'Fredoka', cursive, sans-serif !important;
        color: #065f46 !important;
        font-size: 24px !important;
    }

    button[data-baseweb="tab"] {
        font-size: 22px !important;
        font-family: 'Fredoka', cursive !important;
        font-weight: 700 !important;
        padding: 10px 24px !important;
        background: transparent !important;
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

    .badge-points {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
        color: #ffffff !important;
        font-family: 'Fredoka', cursive;
        font-weight: 700;
        padding: 12px 26px;
        border-radius: 9999px;
        font-size: 20px;
        box-shadow: 0 4px 14px rgba(22, 163, 74, 0.3);
        border: 2px solid #bbf7d0;
        display: inline-block;
    }

    div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.94);
        backdrop-filter: blur(14px);
        padding: 10px 18px;
        border-radius: 9999px;
        border: 2px solid #bbf7d0;
        box-shadow: 0 4px 20px rgba(6, 78, 59, 0.1);
        display: flex;
        justify-content: center;
        gap: 10px;
    }

    div[role="radiogroup"] label {
        padding: 10px 20px !important;
        border-radius: 9999px !important;
        font-weight: 700 !important;
        font-family: 'Fredoka', cursive !important;
        color: #065f46 !important;
        font-size: 19px !important;
        transition: all 0.2s ease;
    }

    div[role="radiogroup"] label:hover {
        background: #dcfce7 !important;
    }

    [data-testid="stForm"], [data-testid="stMetric"], .stTable {
        background: rgba(255, 255, 255, 0.94) !important;
        backdrop-filter: blur(16px) !important;
        padding: 32px !important;
        border-radius: 26px !important;
        box-shadow: 0 10px 30px rgba(6, 78, 59, 0.09) !important;
        border: 2px solid #bbf7d0 !important;
    }

    input, select, textarea, div[data-baseweb="input"], div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        color: #0f381f !important;
        border-color: #86efac !important;
        border-radius: 14px !important;
        font-size: 20px !important;
        padding: 12px 16px !important;
    }

    input::placeholder {
        color: #94a3b8 !important;
        font-size: 19px !important;
    }

    div[data-testid="stMetricValue"] {
        color: #15803d !important;
        font-family: 'Fredoka', cursive !important;
        font-weight: 700 !important;
        font-size: 50px !important;
    }

    div[data-testid="stMetricLabel"] * {
        font-size: 22px !important;
        font-weight: 700 !important;
    }

    .stButton>button, div[data-testid="stForm"] button {
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%) !important;
        color: #ffffff !important;
        font-family: 'Fredoka', cursive !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        border-radius: 20px !important;
        border: 2px solid #86efac !important;
        padding: 14px 34px !important;
        box-shadow: 0 6px 18px rgba(22, 163, 74, 0.28) !important;
        transition: transform 0.15s ease;
    }

    .stButton>button:hover, div[data-testid="stForm"] button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, #166534 0%, #15803d 100%) !important;
        color: #ffffff !important;
    }

    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px dashed #16a34a !important;
        border-radius: 22px !important;
        padding: 34px !important;
    }

    [data-testid="stFileUploader"] * {
        background-color: transparent !important;
        font-size: 19px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- LOGIN GATEWAY (Nature Light Theme) -----------------
if not st.session_state.authenticated:
    st.markdown("<br>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 2.2, 1])

    with col_l2:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 24px;">
                <div style="display: inline-flex; align-items: center; justify-content: center; gap: 14px; margin-bottom: 4px;">
                    <svg width="54" height="54" viewBox="0 0 24 24" fill="#15803d">
                        <path d="M2 22h20c0-5.52-4.48-10-10-10v-3.17c2.83-.48 5-2.94 5-5.83 0-.55-.45-1-1-1s-1 .45-1 1c0 2.21-1.79 4-4 4-1.1 0-2.1-.45-2.83-1.17-.39-.39-1.02-.39-1.41 0-.39.39-.39 1.02 0 1.41C7.79 8.44 9 9.61 10 9.87V12C4.48 12 0 16.48 0 22h2z"/>
                    </svg>
                    <span style="font-family: 'Fredoka', cursive, sans-serif; font-size: 62px; font-weight: 700; color: #15803d; letter-spacing: -0.5px;">Ecoza</span>
                </div>
                <div style="font-size: 21px; color: #166534; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 12px;">
                    Rethink. Reuse. Recreate.
                </div>
                <h1 style="color: #064e3b; font-size: 40px; margin-bottom: 6px;">Welcome to Ecoza</h1>
                <p style="color: #365342; font-weight: 600; font-size: 22px;">Log in with your email or mobile number to continue.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        auth_tab1, auth_tab2 = st.tabs(["🔐 Log In", "📝 Create New Account"])

        with auth_tab1:
            with st.form("login_form"):
                login_id = st.text_input("User Email or Mobile Number", placeholder="name@example.com or 9876543210")
                login_password = st.text_input("Password", type="password", placeholder="••••••••")
                btn_login = st.form_submit_button("🚀 Enter Ecoza", use_container_width=True)

                if btn_login:
                    cleaned_id = login_id.strip()
                    if not cleaned_id or not login_password:
                        st.error("Please enter both your User Email/Mobile Number and password!")
                    elif cleaned_id in st.session_state.registered_users and st.session_state.registered_users[cleaned_id]["password"] == login_password:
                        st.session_state.authenticated = True
                        st.session_state.user_identifier = cleaned_id
                        st.session_state.username = st.session_state.registered_users[cleaned_id]["name"]
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Incorrect details! (Demo: user@ecoza.com / pass: ecoza)")

        with auth_tab2:
            with st.form("signup_form"):
                new_name = st.text_input("Full Name", placeholder="Deepak Raja")
                new_id = st.text_input("User Email or Mobile Number", placeholder="name@example.com or 9876543210")
                new_password = st.text_input("Create Password", type="password", placeholder="••••••••")
                btn_signup = st.form_submit_button("⭐ Sign Up & Join Ecoza", use_container_width=True)

                if btn_signup:
                    cleaned_new_id = new_id.strip()
                    if not new_name or not cleaned_new_id or not new_password:
                        st.error("Please fill in all details!")
                    elif cleaned_new_id in st.session_state.registered_users:
                        st.warning("This User Email or Mobile Number is already registered! Please log in.")
                    else:
                        st.session_state.registered_users[cleaned_new_id] = {
                            "password": new_password,
                            "name": new_name
                        }
                        st.session_state.authenticated = True
                        st.session_state.user_identifier = cleaned_new_id
                        st.session_state.username = new_name
                        st.balloons()
                        st.success("Account created successfully! Welcome.")
                        st.rerun()

    st.stop()

# ----------------- AUTHENTICATED APPLICATION -----------------

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

st.markdown(f"<p style='font-size: 18px; color: #365342; margin-top: -6px;'>Logged in: <b>{st.session_state.username}</b> ({st.session_state.user_identifier})</p>", unsafe_allow_html=True)
st.markdown("<hr style='margin-top: 4px; margin-bottom: 26px; border: 0; border-top: 2px dashed #bbf7d0;'>", unsafe_allow_html=True)

# ----------------- 1. Home / Hero Screen (Floating Elements Theme) -----------------
if st.session_state.current_page == "🏠 Home":
    st.markdown(
        """
        <div style="text-align: center; max-width: 920px; margin: 0 auto; padding: 20px 0 26px 0;">
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

    # Floating eco orbs container matching image tile 5
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; gap: 30px; margin-bottom: 24px;">
            <div style="background: rgba(255,255,255,0.85); border: 2px solid #86efac; border-radius: 50%; width: 68px; height: 68px; display: flex; align-items: center; justify-content: center; font-size: 30px; box-shadow: 0 6px 18px rgba(34, 197, 94, 0.25);">
                ♻️
            </div>
            <div style="background: rgba(255,255,255,0.85); border: 2px solid #86efac; border-radius: 50%; width: 78px; height: 78px; display: flex; align-items: center; justify-content: center; font-size: 36px; box-shadow: 0 8px 24px rgba(34, 197, 94, 0.35);">
                🌿
            </div>
            <div style="background: rgba(255,255,255,0.85); border: 2px solid #86efac; border-radius: 50%; width: 68px; height: 68px; display: flex; align-items: center; justify-content: center; font-size: 30px; box-shadow: 0 6px 18px rgba(34, 197, 94, 0.25);">
                💡
            </div>
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
            <div style="background: rgba(255,255,255,0.95); padding: 30px; border-radius: 22px; border: 2px solid #bbf7d0; text-align: center; box-shadow: 0 6px 18px rgba(6, 78, 59, 0.06);">
                <div style="font-size: 52px; margin-bottom: 10px;">📷</div>
                <h3 style="color: #065f46; margin: 0 0 10px 0; font-size: 28px;">AI Waste Scanner</h3>
                <p style="color: #365342; font-size: 19px; margin: 0; line-height: 1.5;">Upload or snap photos to identify materials and calculate points per 1,000 grams.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div style="background: rgba(255,255,255,0.95); padding: 30px; border-radius: 22px; border: 2px solid #bbf7d0; text-align: center; box-shadow: 0 6px 18px rgba(6, 78, 59, 0.06);">
                <div style="font-size: 52px; margin-bottom: 10px;">🚚</div>
                <h3 style="color: #065f46; margin: 0 0 10px 0; font-size: 28px;">Doorstep Collection</h3>
                <p style="color: #365342; font-size: 19px; margin: 0; line-height: 1.5;">Schedule doorstep pickups with certified recycling partners.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div style="background: rgba(255,255,255,0.95); padding: 30px; border-radius: 22px; border: 2px solid #bbf7d0; text-align: center; box-shadow: 0 6px 18px rgba(6, 78, 59, 0.06);">
                <div style="font-size: 52px; margin-bottom: 10px;">🎁</div>
                <h3 style="color: #065f46; margin: 0 0 10px 0; font-size: 28px;">Community Rewards</h3>
                <p style="color: #365342; font-size: 19px; margin: 0; line-height: 1.5;">Trade accumulated points for plant saplings, book coupons, and vouchers.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.subheader("🎯 4 Simple Steps to Recycle")
    step1, step2, step3, step4 = st.columns(4)
    step1.success("**Step 1: Sort**\n\nSeparate plastic bottles, paper, and metal cans into clean streams.")
    step2.info("**Step 2: Scan**\n\nSnap a picture and input weight in grams.")
    step3.warning("**Step 3: Drop/Pickup**\n\nDeposit at nearby centers or call our pickup van.")
    step4.error("**Step 4: Claim**\n\nRedeem coupons and track your leaderboard rank!")

# ----------------- 2. AI Scanner & Classifier -----------------
elif st.session_state.current_page == "📸 AI Scanner":
    st.title("📸 AI Waste Scanner & Classifier")
    st.markdown("<p style='font-size: 22px; color: #365342;'>Upload an image or take a photo to detect material category and log EcoPoints.</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📁 Upload Item Photo", "📷 Snap With Camera"])
    uploaded_image = None

    with tab1:
        file_input = st.file_uploader("Choose a photo from your device", type=["jpg", "jpeg", "png"])
        if file_input:
            uploaded_image = Image.open(file_input)

    with tab2:
        cam_input = st.camera_input("Take a photo of the item")
        if cam_input:
            uploaded_image = Image.open(cam_input)

    detected_category = "🥤 Plastic Bottles"
    confidence_score = 96.5

    if uploaded_image:
        col_img, col_pred = st.columns([1, 2])
        with col_img:
            st.image(uploaded_image, caption="Analyzed Item", use_container_width=True)
        with col_pred:
            possible_categories = list(RATES.keys())
            detected_category = random.choice(possible_categories)
            confidence_score = round(random.uniform(92.0, 99.4), 1)

            st.balloons()
            st.success(f"### 🎉 Classified: **{detected_category}**")
            st.markdown(f"<p style='font-size: 22px;'>Confidence score: <b>{confidence_score}%</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 22px;'>Rate: <b>{RATES[detected_category]} EcoPoints per 1,000 grams</b></p>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("⚖️ Enter Estimated Weight (in Grams)")

    with st.form("waste_log_form"):
        selected_category = st.selectbox(
            "Selected Material",
            list(RATES.keys()),
            index=list(RATES.keys()).index(detected_category) if detected_category in RATES else 0
        )
        
        input_grams = st.number_input(
            "Weight in Grams",
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
            st.success(f"Awesome! Added {calculated_points} EcoPoints to your balance!")
            st.rerun()

# ----------------- 3. Nearby Collection Centers -----------------
elif st.session_state.current_page == "🗺️ Drop-off Map":
    st.title("🗺️ Ecoza Drop-Off Centers")
    st.markdown("<p style='font-size: 22px; color: #365342;'>Find certified circular recycling drop-off centers across Chennai!</p>", unsafe_allow_html=True)

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
    st.markdown("<p style='font-size: 22px; color: #365342;'>Book a verified Ecoza pickup partner directly to your address.</p>", unsafe_allow_html=True)

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
    st.markdown(f"<p style='font-size: 22px; color: #365342;'>Redeem points for eco-conscious rewards! Balance: <b>{st.session_state.ecopoints} EcoPoints</b></p>", unsafe_allow_html=True)

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
    st.markdown("<p style='font-size: 22px; color: #365342;'>Top recyclers contributing to zero waste this week!</p>", unsafe_allow_html=True)

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
    st.markdown("<p style='font-size: 22px; color: #365342;'>Track your total diverted waste and carbon savings!</p>", unsafe_allow_html=True)

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
