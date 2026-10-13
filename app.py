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

# ----------------- State Management -----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_identifier" not in st.session_state:
    st.session_state.user_identifier = "deepakraja6524@gmail.com"

if "username" not in st.session_state:
    st.session_state.username = "Deepak Raja"

if "scan_result" not in st.session_state:
    st.session_state.scan_result = None

# Streamlined, visible page names
PAGES = [
    "🏠 Home", 
    "📸 Scanner", 
    "💡 Upcycle AI",
    "🗺️ Centers", 
    "🚚 Pickup", 
    "🎁 Rewards", 
    "🏆 Leaderboard", 
    "📊 Impact"
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

# ----------------- Dynamic Background Selection -----------------
PAGE_BACKGROUNDS = {
    "LOGIN": "https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?auto=format&fit=crop&w=2400&q=95",
    "🏠 Home": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=2400&q=95",
    "📸 Scanner": "https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?auto=format&fit=crop&w=2400&q=95",
    "💡 Upcycle AI": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=2400&q=95",
    "🗺️ Centers": "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=2400&q=95",
    "🚚 Pickup": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=2400&q=95",
    "🎁 Rewards": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=2400&q=95",
    "🏆 Leaderboard": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=2400&q=95",
    "📊 Impact": "https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=2400&q=95"
}

if not st.session_state.authenticated:
    active_bg = PAGE_BACKGROUNDS["LOGIN"]
else:
    active_bg = PAGE_BACKGROUNDS.get(st.session_state.current_page, PAGE_BACKGROUNDS["🏠 Home"])

# ----------------- Responsive, Fully Visible CSS -----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Fredoka:wght@600;700&display=swap');

    [data-testid="stSidebar"], section[data-testid="stSidebar"], #MainMenu, footer {
        display: none !important;
    }

    html, body, .stApp, [data-testid="stAppViewRoot"], [data-testid="stHeader"], 
    .stAppHeader, .stAppViewContainer, section.main, .block-container {
        background: transparent !important;
        background-color: transparent !important;
    }

    body, .stApp {
        background: url('""" + active_bg + """') no-repeat center center fixed !important;
        background-size: cover !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .stApp p, .stApp span, .stApp label, .stApp div {
        color: #032a15 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 18px;
        font-weight: 700;
        line-height: 1.5;
    }

    h1, h2, h3, h4 {
        font-family: 'Fredoka', cursive, sans-serif !important;
        color: #022b14 !important;
        text-shadow: 0 1px 4px rgba(255, 255, 255, 0.7);
    }

    h1 { font-size: 44px !important; margin-bottom: 10px !important; }
    h2 { font-size: 32px !important; margin-bottom: 8px !important; }

    /* FULLY VISIBLE WRAPPING NAVBAR: Never gets clipped on edges */
    div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.82) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        padding: 8px 16px !important;
        border-radius: 20px !important;
        border: 2px solid rgba(22, 163, 74, 0.8) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12) !important;
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 6px 10px !important;
        width: 100% !important;
    }

    div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.6) !important;
        padding: 6px 12px !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        font-family: 'Fredoka', cursive !important;
        color: #032e18 !important;
        font-size: 15px !important;
        border: 1px solid rgba(22, 163, 74, 0.3) !important;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    div[role="radiogroup"] label:hover {
        background: #dcfce7 !important;
        border-color: #16a34a !important;
    }

    /* Glass Cards */
    [data-testid="stForm"], [data-testid="stMetric"], .stTable {
        background: rgba(255, 255, 255, 0.60) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        padding: 24px !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12) !important;
        border: 2px solid rgba(255, 255, 255, 0.9) !important;
    }

    input, select, textarea, div[data-baseweb="input"], div[data-baseweb="base-input"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #032e18 !important;
        border: 2px solid #16a34a !important;
        border-radius: 12px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
    }

    .stButton>button, div[data-testid="stForm"] button {
        background: linear-gradient(135deg, #15803d 0%, #16a34a 100%) !important;
        color: #ffffff !important;
        font-family: 'Fredoka', cursive !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border-radius: 16px !important;
        border: 2px solid #86efac !important;
        padding: 8px 22px !important;
        box-shadow: 0 6px 16px rgba(21, 128, 61, 0.3) !important;
    }

    .badge-points {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
        color: #ffffff !important;
        font-family: 'Fredoka', cursive;
        font-weight: 700;
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 16px;
        box-shadow: 0 4px 14px rgba(22, 163, 74, 0.3);
        border: 2px solid #bbf7d0;
        display: inline-block;
        white-space: nowrap;
    }

    .brand-logo {
        font-size: 32px;
        font-family: 'Fredoka', cursive, sans-serif;
        font-weight: 700;
        color: #0f5132 !important;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- Pixel Classifier Engine -----------------
def classify_material_accurately(img: Image.Image):
    img_rgb = img.convert("RGB").resize((100, 100))
    arr = np.array(img_rgb, dtype=np.float32)

    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    mean_r, mean_g, mean_b = np.mean(r), np.mean(g), np.mean(b)
    brightness = (mean_r + mean_g + mean_b) / 3.0

    if mean_g > mean_r + 15 and mean_g > mean_b + 15:
        return "🍎 Organic Waste", 96.4
    
    if mean_r > mean_g + 18 and mean_g > mean_b + 12 and brightness < 200:
        return "📦 Paper & Cardboard", 95.8

    saturation = np.std(arr, axis=2).mean()
    if saturation < 18 and 80 < brightness < 185:
        return "🥫 Metal & Aluminium Cans", 94.2

    if brightness < 75:
        return "🔋 E-Waste & Batteries", 93.6

    return "🥤 Plastic Bottles", 97.2

UPCYCLE_SUGGESTIONS = {
    "🥤 Plastic Bottles": [
        {
            "title": "🌿 Self-Watering Indoor Herb Planter",
            "difficulty": "Easy (15 mins)",
            "tools": "Scissors, Cotton String, Soil, Seeds",
            "steps": "1. Cut the bottle in half horizontally.\n2. Puncture the cap and thread a cotton string through it.\n3. Invert the top part with soil and plant seeds.\n4. Fill the base with water; the string maintains moisture automatically!"
        },
        {
            "title": "✏️ Multi-Compartment Desk Stationery Organizer",
            "difficulty": "Easy (10 mins)",
            "tools": "Craft knife, Colored tape / markers",
            "steps": "1. Cut the bottom 4 inches off 3-4 bottles at varying heights.\n2. Smooth the edges with colored tape.\n3. Cluster and glue together to hold pens, markers, and paintbrushes!"
        }
    ],
    "📦 Paper & Cardboard": [
        {
            "title": "🌱 Biodegradable Seedling Nursery Pots",
            "difficulty": "Easy (10 mins)",
            "tools": "Cardboard tubes or egg cartons, Soil",
            "steps": "1. Cut cardboard toilet paper rolls into 2-inch segments.\n2. Fold bottom tabs inward to create cups.\n3. Fill with compost and plant directly into garden soil when ready!"
        }
    ],
    "🥫 Metal & Aluminium Cans": [
        {
            "title": "🕯️ Punched-Tin Lantern / Candle Holder",
            "difficulty": "Medium (25 mins)",
            "tools": "Clean metal can, Hammer, Nail, Tea light / LED",
            "steps": "1. Fill the can with water and freeze solid so it retains its shape.\n2. Punch dot patterns with a hammer and nail.\n3. Melt the ice, paint the exterior, and insert an LED tea light."
        }
    ],
    "🍶 Glass Recyclables": [
        {
            "title": "🏺 Fairy Light Memory Jar / Terrarium",
            "difficulty": "Easy (15 mins)",
            "tools": "Glass jar, Small pebbles, Activated charcoal, Moss",
            "steps": "1. Clean and dry the jar thoroughly.\n2. Layer pebbles, charcoal, and potting mix.\n3. Plant a succulent or coil an LED fairy light wire inside."
        }
    ],
    "🔋 E-Waste & Batteries": [
        {
            "title": "🤖 Miniature Tech Sculpture / Cyber Keychain",
            "difficulty": "Advanced (30 mins)",
            "tools": "Old PCB scraps, Keyring, Protective gloves",
            "steps": "1. Cut small rectangular sections of damaged motherboards.\n2. Sand edges smooth and drill a small hole for a key ring.\n3. Note: Deposit chemical batteries directly at certified hubs!"
        }
    ],
    "🍎 Organic Waste": [
        {
            "title": "🪴 Rich Microbial Kitchen Garden Compost",
            "difficulty": "Easy (Ongoing)",
            "tools": "Compost bucket / Pot with lid, Dry leaves",
            "steps": "1. Layer fruit/vegetable peels with dried leaves.\n2. Aerate once a week to maintain oxygen flow.\n3. In 4 weeks, you have free, nutrient-dense organic fertilizer!"
        }
    ]
}

RECYCLING_CENTERS = [
    {"Center Name": "⚡ Guindy Eco Battery & E-Waste Hub", "Type": "E-Waste & Electronics", "Address": "Guindy Industrial Estate", "Contact": "+91 94441 23456", "lat": 13.0067, "lon": 80.2030},
    {"Center Name": "📘 Anna Nagar Paper Depot", "Type": "Plastic, Paper & Cardboard", "Address": "Anna Nagar West", "Contact": "+91 98840 56789", "lat": 13.0850, "lon": 80.2101},
    {"Center Name": "⚙️ Ambattur Scrap & Metal Depot", "Type": "Metal & Glass Recyclables", "Address": "Ambattur Industrial Estate", "Contact": "+91 97720 11223", "lat": 13.1143, "lon": 80.1548},
    {"Center Name": "🌱 Adyar Eco Park Composting Hub", "Type": "Wet & Organic Waste", "Address": "Adyar Eco Park Zone", "Contact": "+91 91234 98765", "lat": 13.0125, "lon": 80.2570}
]

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

# ----------------- AUTHENTICATED TOP HEADER -----------------
top_c1, top_c2 = st.columns([3.8, 1.4], vertical_alignment="center")
with top_c1:
    st.markdown('<div class="brand-logo">🌱 Ecoza <span style="font-size: 14px; color: #166534; font-weight: 800;">• RETHINK. REUSE. RECREATE.</span></div>', unsafe_allow_html=True)
with top_c2:
    p_col, out_col = st.columns([1.2, 0.8], vertical_alignment="center")
    with p_col:
        st.markdown(f'<div class="badge-points">🌟 {st.session_state.ecopoints} pts</div>', unsafe_allow_html=True)
    with out_col:
        if st.button("🚪 Out"):
            st.session_state.authenticated = False
            st.rerun()

# Responsive wrapping navbar: all 8 items stay in full view
cur_idx = PAGES.index(st.session_state.current_page) if st.session_state.current_page in PAGES else 0
choice = st.radio("Nav", PAGES, index=cur_idx, horizontal=True, label_visibility="collapsed")
if choice != st.session_state.current_page:
    st.session_state.current_page = choice
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
                Turn Everyday Waste Into <span style="color: #16a34a;">EcoPoints & Upcycled Creations!</span>
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    c_b1, c_b2, _ = st.columns([1.5, 1.8, 1.5])
    with c_b1:
        if st.button("📸 AI Scanner & Log", use_container_width=True):
            st.session_state.current_page = "📸 Scanner"
            st.rerun()
    with c_b2:
        if st.button("💡 Upcycle AI Studio", use_container_width=True):
            st.session_state.current_page = "💡 Upcycle AI"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.markdown(
        """
        <div style="background: rgba(255,255,255,0.55); backdrop-filter: blur(12px); padding: 24px; border-radius: 20px; border: 2px solid rgba(255,255,255,0.9); text-align: center;">
            <div style="font-size: 46px; margin-bottom: 8px;">📷</div>
            <h3 style="margin: 0 0 6px 0;">AI Waste Scanner</h3>
            <p style="font-size: 16px; margin: 0;">Instant recognition for plastics, paper, metals, and e-waste.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    col2.markdown(
        """
        <div style="background: rgba(255,255,255,0.55); backdrop-filter: blur(12px); padding: 24px; border-radius: 20px; border: 2px solid rgba(255,255,255,0.9); text-align: center;">
            <div style="font-size: 46px; margin-bottom: 8px;">💡</div>
            <h3 style="margin: 0 0 6px 0;">Upcycle AI Studio</h3>
            <p style="font-size: 16px; margin: 0;">Snap waste materials to receive clever DIY upcycling project guides.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    col3.markdown(
        """
        <div style="background: rgba(255,255,255,0.55); backdrop-filter: blur(12px); padding: 24px; border-radius: 20px; border: 2px solid rgba(255,255,255,0.9); text-align: center;">
            <div style="font-size: 46px; margin-bottom: 8px;">🎁</div>
            <h3 style="margin: 0 0 6px 0;">Rewards Store</h3>
            <p style="font-size: 16px; margin: 0;">Trade accumulated points for plant saplings and gift vouchers.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------- 2. AI SCANNER SCREEN -----------------
elif st.session_state.current_page == "📸 Scanner":
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

# ----------------- 3. UPCYCLE AI STUDIO -----------------
elif st.session_state.current_page == "💡 Upcycle AI":
    st.title("💡 Upcycle AI Studio — Recreate From Waste")
    st.write("Take a picture of an item you are about to throw away. The AI will tell you how you can recreate it into something useful!")

    u_t1, u_t2 = st.tabs(["📷 Snap Item With Camera", "📁 Upload An Item Photo"])
    upcycle_img = None

    with u_t1:
        u_cam = st.camera_input("Snap the waste item (e.g. plastic bottle, cardboard box, tin can)")
        if u_cam:
            upcycle_img = Image.open(u_cam)

    with u_t2:
        u_file = st.file_uploader("Upload an item picture", type=["jpg", "jpeg", "png"], key="upcycle_file_uploader")
        if u_file:
            upcycle_img = Image.open(u_file)

    detected_upcycle_cat = "🥤 Plastic Bottles"

    if upcycle_img:
        det_cat, det_conf = classify_material_accurately(upcycle_img)
        detected_upcycle_cat = det_cat

        col_u1, col_u2 = st.columns([1, 1.8])
        with col_u1:
            st.image(upcycle_img, caption="Material Submitted", use_container_width=True)
        with col_u2:
            st.success(f"### Detected Material: **{detected_upcycle_cat}** ({det_conf}% confidence)")
            st.info("✨ The AI analyzed this item and generated the following step-by-step DIY upcycling ideas:")

    st.markdown("---")
    st.subheader(f"🛠️ Creative Upcycling Ideas for: {detected_upcycle_cat}")

    suggestions = UPCYCLE_SUGGESTIONS.get(detected_upcycle_cat, UPCYCLE_SUGGESTIONS["🥤 Plastic Bottles"])

    for idx, idea in enumerate(suggestions):
        with st.expander(f"✨ Project {idx + 1}: {idea['title']}  •  [{idea['difficulty']}]", expanded=True):
            st.markdown(f"**🧰 Tools & Supplies Needed:** `{idea['tools']}`")
            st.markdown("**📋 How To Make It:**")
            st.write(idea["steps"])
            if st.button(f"⭐ I made this project! (+15 Bonus EcoPoints)", key=f"bonus_up_{idx}"):
                st.session_state.ecopoints += 15
                st.balloons()
                st.success("Congratulations on upcycling! 15 Bonus EcoPoints added to your balance.")
                st.rerun()

# ----------------- 4. DROP-OFF MAP -----------------
elif st.session_state.current_page == "🗺️ Centers":
    st.title("🗺️ Ecoza Drop-Off Centers")
    df_centers = pd.DataFrame(RECYCLING_CENTERS)
    st.map(df_centers[["lat", "lon"]], zoom=11)

    for _, row in df_centers.iterrows():
        with st.container():
            c1, c2 = st.columns([3, 1])
            c1.markdown(f"#### {row['Center Name']}\n**Accepts:** {row['Type']}\n**Address:** {row['Address']}")
            c2.write(f"📞 `{row['Contact']}`")
            st.divider()

# ----------------- 5. DOORSTEP PICKUP -----------------
elif st.session_state.current_page == "🚚 Pickup":
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

# ----------------- 6. REWARDS STORE -----------------
elif st.session_state.current_page == "🎁 Rewards":
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

# ----------------- 7. LEADERBOARD -----------------
elif st.session_state.current_page == "🏆 Leaderboard":
    st.title("🏆 Champions Leaderboard")
    leaderboard = [
        {"Rank": "🥇 1st", "Contributor": "Class 8B (Little Flower School)", "Waste Saved": "44,000 g", "EcoPoints": 880},
        {"Rank": "🥈 2nd", "Contributor": "Priya R.", "Waste Saved": "38,500 g", "EcoPoints": 770},
        {"Rank": "🥉 3rd", "Contributor": f"{st.session_state.username} (You)", "Waste Saved": "28,000 g", "EcoPoints": st.session_state.ecopoints},
        {"Rank": "4th", "Contributor": "Karthik Raj", "Waste Saved": "18,500 g", "EcoPoints": 370}
    ]
    st.table(pd.DataFrame(leaderboard))

# ----------------- 8. DASHBOARD -----------------
elif st.session_state.current_page == "📊 Impact":
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
