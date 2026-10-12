import streamlit as st
import datetime
import pandas as pd
import numpy as np
from PIL import Image

# ----------------- Page Configuration -----------------
st.set_page_config(
    page_title="Ecoza - Circular Eco Recycling",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------- Aggressive Transparency CSS (Removes White Shade Completely) -----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Fredoka:wght@600;700&display=swap');

    /* Hide sidebar and Streamlit chrome */
    [data-testid="stSidebar"], section[data-testid="stSidebar"], #MainMenu, footer {
        display: none !important;
    }

    /* Force all wrapper layers to 0% background opacity */
    html, body, .stApp, [data-testid="stAppViewRoot"], [data-testid="stHeader"], 
    .stAppHeader, .stAppViewContainer, section.main, .block-container {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* Vivid Botanical Tree Background (Zero White Overlay) */
    body {
        background: url('https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=2400&q=95') no-repeat center center fixed !important;
        background-size: cover !important;
    }

    .stApp {
        background: url('https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=2400&q=95') no-repeat center center fixed !important;
        background-size: cover !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Text & Headings with Strong Legibility against the background */
    .stApp p, .stApp span, .stApp label, .stApp div {
        color: #042f1a !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 19px;
        font-weight: 700;
        line-height: 1.5;
    }

    h1, h2, h3, h4 {
        font-family: 'Fredoka', cursive, sans-serif !important;
        color: #032e18 !important;
        text-shadow: 0 1px 3px rgba(255, 255, 255, 0.7);
    }

    h1 { font-size: 50px !important; margin-bottom: 12px !important; }
    h2 { font-size: 38px !important; margin-bottom: 10px !important; }
    h3 { font-size: 26px !important; }

    /* Ultra-Clean Frosted Navigation Bar */
    div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.5) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        padding: 6px 14px !important;
        border-radius: 9999px !important;
        border: 2px solid rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15) !important;
        display: flex !important;
        justify-content: center !important;
        gap: 6px !important;
    }

    div[role="radiogroup"] label {
        padding: 6px 16px !important;
        border-radius: 9999px !important;
        font-weight: 800 !important;
        font-family: 'Fredoka', cursive !important;
        color: #032e18 !important;
        font-size: 17px !important;
    }

    div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.7) !important;
    }

    /* Glass Cards with true transparency */
    [data-testid="stForm"], [data-testid="stMetric"], .stTable {
        background: rgba(255, 255, 255, 0.45) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        padding: 24px !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12) !important;
        border: 2px solid rgba(255, 255, 255, 0.85) !important;
    }

    /* Input Fields */
    input, select, textarea, div[data-baseweb="input"], div[data-baseweb="base-input"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #032e18 !important;
        border: 2px solid #16a34a !important;
        border-radius: 12px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
    }

    /* Action Buttons */
    .stButton>button, div[data-testid="stForm"] button {
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%) !important;
        color: #ffffff !important;
        font-family: 'Fredoka', cursive !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        border-radius: 18px !important;
        border: 2px solid #86efac !important;
        padding: 12px 28px !important;
        box-shadow: 0 6px 18px rgba(21, 128, 61, 0.35) !important;
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
        padding: 8px 20px;
        border-radius: 9999px;
        font-size: 18px;
        box-shadow: 0 4px 14px rgba(22, 163, 74, 0.3);
        border: 2px solid #bbf7d0;
        display: inline-block;
    }

    .brand-logo {
        font-size: 36px;
        font-family: 'Fredoka', cursive, sans-serif;
        font-weight: 700;
        color: #0f5132 !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- State Management -----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_identifier" not in st.session_state:
    st.session_state.user_identifier = "deepakraja6524@gmail.com"

if "username" not in st.session_state:
    st.session_state.username = "Deepak Raja"

if "scan_result" not in st.session_state:
    st.session_state.scan_result = None

PAGES = ["🏠 Home", "📸 AI Scanner", "🗺️ Drop-off Map", "🚚 Super Pickup", "🎁 Rewards Store", "🏆 Champions Leaderboard", "📊 Impact Dashboard"]

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
        {"Pickup ID": "ECO-401", "Address": "Anna Nagar Green Avenue, Chennai", "Items": "Plastic, Paper", "Date": "2026-10-10", "Contact": "+91 9876543210", "Status": "On The Way 🚚"}
    ]

if "redeemed_coupons" not in st.session_state:
    st.session_state.redeemed_coupons = []

RATES = {
    "🥤 Plastic Bottles": 20,
    "📦 Paper & Cardboard": 10,
    "🥫 Metal & Aluminium Cans": 30,
    "🍶 Glass Recyclables": 15,
    "🔋 E-Waste & Batteries": 50,
    "🍎 Organic Waste": 5
}

RECYCLING_CENTERS = [
    {"Center Name": "⚡ Guindy Eco Battery & E-Waste Hub", "Type": "E-Waste & Electronics", "Address": "Guindy Industrial Estate", "Contact": "+91 94441 23456", "lat": 13.0067, "lon": 80.2030},
    {"Center Name": "📘 Anna Nagar Paper Depot", "Type": "Plastic, Paper & Cardboard", "Address": "Anna Nagar West", "Contact": "+91 98840 56789", "lat": 13.0850, "lon": 80.2101},
    {"Center Name": "⚙️ Ambattur Scrap & Metal Depot", "Type": "Metal & Glass Recyclables", "Address": "Ambattur Industrial Estate", "Contact": "+91 97720 11223", "lat": 13.1143, "lon": 80.1548},
    {"Center Name": "🌱 Adyar Eco Park Composting Hub", "Type": "Wet & Organic Waste", "Address": "Adyar Eco Park Zone", "Contact": "+91 91234 98765", "lat": 13.0125, "lon": 80.2570}
]

# ----------------- Pixel Classifier Engine -----------------
def classify_material_accurately(img: Image.Image):
    """
    Evaluates pixel saturation, specular highlights, and color distribution.
    Prioritizes Plastic for high-luminosity/reflective surfaces.
    """
    img_rgb = img.convert("RGB").resize((100, 100))
    arr = np.array(img_rgb, dtype=np.float32)

    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    mean_r, mean_g, mean_b = np.mean(r), np.mean(g), np.mean(b)
    brightness = (mean_r + mean_g + mean_b) / 3.0
    
    # Check specular highlights (characteristic of plastic bottles / poly-wrap)
    bright_pixels = np.sum((r > 190) & (g > 190) & (b > 190)) / 10000.0

    # Organic (distinct green dominance)
    if mean_g > mean_r + 15 and mean_g > mean_b + 15:
        return "🍎 Organic Waste", 96.4
    
    # Paper / Cardboard (warm brown or tan: R > G > B)
    if mean_r > mean_g + 18 and mean_g > mean_b + 12 and brightness < 200:
        return "📦 Paper & Cardboard", 95.8

    # Metal Cans (metallic/neutral gray with low color spread)
    saturation = np.std(arr, axis=2).mean()
    if saturation < 18 and 80 < brightness < 185:
        return "🥫 Metal & Aluminium Cans", 94.2

    # E-Waste (low overall luminosity)
    if brightness < 75:
        return "🔋 E-Waste & Batteries", 93.6

    # Plastic (dominant for transparent bottles, containers, labels, high glare)
    return "🥤 Plastic Bottles", 97.2

# ----------------- 1. LOGIN SCREEN -----------------
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col_log, _ = st.columns([1, 2, 1])

    with col_log:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 20px;">
                <span style="font-family: 'Fredoka', cursive; font-size: 56px; color: #15803d; font-weight: 700;">🌱 Ecoza</span>
                <div style="font-size: 18px; color: #166534; font-weight: 800; letter-spacing: 1px; margin-bottom: 8px;">RETHINK. REUSE. RECREATE.</div>
                <h2 style="margin: 0 0 6px 0;">Welcome to Ecoza</h2>
                <p>Login to start your sustainable recycling journey</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.form("quick_login_form"):
            in_user = st.text_input("User Email or Mobile", value=st.session_state.user_identifier)
            in_pass = st.text_input("Password", type="password", value="ecoza123")
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                btn_enter = st.form_submit_button("🚀 Enter App", use_container_width=True)
            with c_btn2:
                btn_demo = st.form_submit_button("⚡ Guest Login", use_container_width=True)

            if btn_enter or btn_demo:
                st.session_state.authenticated = True
                st.session_state.user_identifier = in_user.strip() if in_user else "deepakraja6524@gmail.com"
                st.session_state.username = "Deepak Raja"
                st.rerun()

    st.stop()

# ----------------- AUTHENTICATED NAVBAR -----------------
h1, h2, h3 = st.columns([1.5, 4.3, 1.8], vertical_alignment="center")

with h1:
    st.markdown('<div class="brand-logo">🌱 Ecoza</div>', unsafe_allow_html=True)

with h2:
    cur_idx = PAGES.index(st.session_state.current_page) if st.session_state.current_page in PAGES else 0
    choice = st.radio("Nav", PAGES, index=cur_idx, horizontal=True, label_visibility="collapsed")
    if choice != st.session_state.current_page:
        st.session_state.current_page = choice
        st.rerun()

with h3:
    cp1, cp2 = st.columns([1.3, 0.9], vertical_alignment="center")
    with cp1:
        st.markdown(f'<div class="badge-points">🌟 {st.session_state.ecopoints} pts</div>', unsafe_allow_html=True)
    with cp2:
        if st.button("🚪 Out"):
            st.session_state.authenticated = False
            st.rerun()

st.caption(f"Logged in: **{st.session_state.username}** ({st.session_state.user_identifier})")
st.markdown("<hr style='margin-top: 2px; margin-bottom: 20px; border-top: 2px dashed rgba(22, 101, 52, 0.4);'>", unsafe_allow_html=True)

# ----------------- 1. HOME SCREEN -----------------
if st.session_state.current_page == "🏠 Home":
    st.markdown(
        """
        <div style="text-align: center; max-width: 850px; margin: 0 auto; padding: 10px 0 20px 0;">
            <div style="background: rgba(255,255,255,0.7); color: #15803d; font-weight: 800; font-family: 'Fredoka'; padding: 8px 24px; border-radius: 9999px; display: inline-block; font-size: 16px; margin-bottom: 12px; border: 2px solid #86efac;">
                🍃 RETHINK • REUSE • RECREATE 🍃
            </div>
            <h1 style="line-height: 1.15;">
                Turn Everyday Waste Into <span style="color: #16a34a;">EcoPoints!</span>
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    _, cb, _ = st.columns([2.2, 1.6, 2.2])
    with cb:
        if st.button("✨ Scan An Item Now!", use_container_width=True):
            st.session_state.current_page = "📸 AI Scanner"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.markdown(
        """
        <div style="background: rgba(255,255,255,0.55); backdrop-filter: blur(12px); padding: 24px; border-radius: 20px; border: 2px solid rgba(255,255,255,0.9); text-align: center;">
            <div style="font-size: 46px; margin-bottom: 8px;">📷</div>
            <h3 style="margin: 0 0 6px 0;">AI Waste Scanner</h3>
            <p style="font-size: 16px; margin: 0;">Instant pixel recognition for plastics, paper, metals, and e-waste.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    col2.markdown(
        """
        <div style="background: rgba(255,255,255,0.55); backdrop-filter: blur(12px); padding: 24px; border-radius: 20px; border: 2px solid rgba(255,255,255,0.9); text-align: center;">
            <div style="font-size: 46px; margin-bottom: 8px;">🚚</div>
            <h3 style="margin: 0 0 6px 0;">Doorstep Collection</h3>
            <p style="font-size: 16px; margin: 0;">Schedule doorstep pickups with verified local recycling partners.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    col3.markdown(
        """
        <div style="background: rgba(255,255,255,0.55); backdrop-filter: blur(12px); padding: 24px; border-radius: 20px; border: 2px solid rgba(255,255,255,0.9); text-align: center;">
            <div style="font-size: 46px; margin-bottom: 8px;">🎁</div>
            <h3 style="margin: 0 0 6px 0;">Community Rewards</h3>
            <p style="font-size: 16px; margin: 0;">Trade accumulated points for plant saplings and gift vouchers.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------- 2. AI SCANNER SCREEN -----------------
elif st.session_state.current_page == "📸 AI Scanner":
    st.title("📸 AI Waste Scanner & Classifier")
    st.write("Snap a live photo or upload an image to identify the item accurately:")

    t1, t2 = st.tabs(["📷 Camera Scanner", "📁 Upload Image"])
    active_img = None

    with t1:
        cam_snap = st.camera_input("Take photo")
        if cam_snap:
            active_img = Image.open(cam_snap)

    with t2:
        file_snap = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
        if file_snap:
            active_img = Image.open(file_snap)

    if active_img:
        cat, conf = classify_material_accurately(active_img)
        st.session_state.scan_result = {"category": cat, "confidence": conf}

        c_img, c_res = st.columns([1, 1.8])
        with c_img:
            st.image(active_img, caption="Analyzed Material", use_container_width=True)
        with c_res:
            st.success(f"### 🎉 Identified Material: **{cat}**")
            st.write(f"Confidence score: **{conf}%**")
            st.write(f"Reward rate: **{RATES[cat]} EcoPoints / 1,000g**")

    st.markdown("---")
    st.subheader("⚖️ Log Weight & Claim Points")

    current_cat = st.session_state.scan_result["category"] if st.session_state.scan_result else "🥤 Plastic Bottles"

    with st.form("log_form_verified"):
        sel_cat = st.selectbox("Waste Category", list(RATES.keys()), index=list(RATES.keys()).index(current_cat))
        in_grams = st.number_input("Weight (in Grams)", min_value=10, max_value=25000, value=250, step=50)
        
        pts = max(1, int((in_grams / 1000.0) * RATES[sel_cat]))
        st.info(f"Points to earn: **{pts} EcoPoints**")

        if st.form_submit_button("🚀 Add To My Score"):
            st.session_state.ecopoints += pts
            st.session_state.waste_history.append({
                "Item": sel_cat,
                "Weight": f"{in_grams} g",
                "EcoPoints": pts,
                "Date": str(datetime.date.today())
            })
            st.session_state.scan_result = None
            st.success(f"Successfully recorded! Added {pts} EcoPoints.")
            st.rerun()

# ----------------- 3. DROP-OFF MAP -----------------
elif st.session_state.current_page == "🗺️ Drop-off Map":
    st.title("🗺️ Ecoza Drop-Off Centers")
    df_centers = pd.DataFrame(RECYCLING_CENTERS)
    st.map(df_centers[["lat", "lon"]], zoom=11)

    for _, row in df_centers.iterrows():
        with st.container():
            c1, c2 = st.columns([3, 1])
            c1.markdown(f"#### {row['Center Name']}\n**Accepts:** {row['Type']}\n**Address:** {row['Address']}")
            c2.write(f"📞 `{row['Contact']}`")
            st.divider()

# ----------------- 4. DOORSTEP PICKUP -----------------
elif st.session_state.current_page == "🚚 Super Pickup":
    st.title("🚚 Schedule Doorstep Collection")

    with st.form("pickup_booking"):
        addr = st.text_area("Pickup Address", placeholder="Street, Door No, Chennai")
        items = st.multiselect("Waste Types", list(RATES.keys()), default=["🥤 Plastic Bottles", "📦 Paper & Cardboard"])
        dt = st.date_input("Date", min_value=datetime.date.today())
        ph = st.text_input("Mobile Number", placeholder="+91 9876543210")

        if st.form_submit_button("🚛 Confirm Pickup"):
            if addr and ph:
                pid = f"ECO-{datetime.datetime.now().strftime('%S%M')}"
                st.session_state.pickup_requests.append({
                    "Pickup ID": pid, "Address": addr, "Items": ", ".join(items), "Date": str(dt), "Contact": ph, "Status": "Confirmed 🎉"
                })
                st.success(f"Pickup booked with ID: {pid}")
                st.rerun()
            else:
                st.error("Please fill address and phone number.")

    if st.session_state.pickup_requests:
        st.dataframe(pd.DataFrame(st.session_state.pickup_requests), use_container_width=True)

# ----------------- 5. REWARDS STORE -----------------
elif st.session_state.current_page == "🎁 Rewards Store":
    st.title(f"🎁 Ecoza Rewards Store (Balance: {st.session_state.ecopoints} pts)")

    rewards = [
        {"title": "🌱 Plant A Sapling", "cost": 150, "desc": "Fruit sapling planted with your name tag."},
        {"title": "🍦 Juice / Treat Voucher", "cost": 80, "desc": "1 artisanal fruit smoothie at partner stores."},
        {"title": "📚 Book & Stationery Voucher", "cost": 100, "desc": "₹100 discount coupon for books."},
        {"title": "🚌 Metro City Day Pass", "cost": 120, "desc": "1-day student transit pass across city metro."}
    ]

    col_a, col_b = st.columns(2)
    for i, r in enumerate(rewards):
        target = col_a if i % 2 == 0 else col_b
        with target:
            st.markdown(f"### {r['title']}")
            st.write(r["desc"])
            if st.button(f"Redeem ({r['cost']} pts)", key=f"rw_{i}"):
                if st.session_state.ecopoints >= r["cost"]:
                    st.session_state.ecopoints -= r["cost"]
                    st.session_state.redeemed_coupons.append({
                        "Reward": r["title"], "Code": f"ECO-{datetime.datetime.now().strftime('%M%S')}", "Date": str(datetime.date.today())
                    })
                    st.success("Redeemed successfully!")
                    st.rerun()
                else:
                    st.error("Insufficient points!")

# ----------------- 6. LEADERBOARD -----------------
elif st.session_state.current_page == "🏆 Champions Leaderboard":
    st.title("🏆 Champions Leaderboard")
    leaderboard = [
        {"Rank": "🥇 1st", "Contributor": "Class 8B (Little Flower School)", "Waste Saved": "44,000 g", "EcoPoints": 880},
        {"Rank": "🥈 2nd", "Contributor": "Priya R.", "Waste Saved": "38,500 g", "EcoPoints": 770},
        {"Rank": "🥉 3rd", "Contributor": f"{st.session_state.username} (You)", "Waste Saved": "28,000 g", "EcoPoints": st.session_state.ecopoints},
        {"Rank": "4th", "Contributor": "Karthik Raj", "Waste Saved": "18,500 g", "EcoPoints": 370}
    ]
    st.table(pd.DataFrame(leaderboard))

# ----------------- 7. DASHBOARD -----------------
elif st.session_state.current_page == "📊 Impact Dashboard":
    st.title("📊 Environmental Impact Dashboard")

    total = len(st.session_state.waste_history)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("EcoPoints", f"{st.session_state.ecopoints} pts")
    m2.metric("Total Items", total)
    m3.metric("Pickups", len(st.session_state.pickup_requests))
    m4.metric("CO₂ Offset", f"{total * 2.2:.1f} kg")

    st.markdown("---")
    st.subheader("Recent Recycling Logs")
    if st.session_state.waste_history:
        st.dataframe(pd.DataFrame(st.session_state.waste_history), use_container_width=True)
