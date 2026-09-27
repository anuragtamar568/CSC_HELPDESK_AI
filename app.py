import os
import time
import streamlit as st
from google import genai
from PIL import Image, ImageDraw, ImageFilter

# =========================================================
# PAGE
# =========================================================
st.set_page_config(
    page_title="CSC_HELPDESK_AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# LOGIN CONFIG
# =========================================================
# YAHAN LOGIN DETAILS CHANGE KAR SAKTE HO
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "12345"

USERNAME = st.secrets.get("APP_USERNAME", DEFAULT_USERNAME)
PASSWORD = st.secrets.get("APP_PASSWORD", DEFAULT_PASSWORD)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


# =========================================================
# PREMIUM LOGIN CSS
# =========================================================
LOGIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(circle at 50% -10%, rgba(255,180,70,.14), transparent 30%),
        radial-gradient(circle at 0% 100%, rgba(255,110,30,.08), transparent 30%),
        #07090d;
    font-family: Inter, sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 100%;
    padding: 0;
}

.login-wrap {
    min-height: 92vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 30px 18px;
}

.login-card {
    width: min(430px, 100%);
    padding: 38px 34px 32px;
    border-radius: 28px;
    background: rgba(17,20,26,.94);
    border: 1px solid rgba(255,255,255,.09);
    box-shadow:
        0 35px 100px rgba(0,0,0,.65),
        0 0 70px rgba(255,150,50,.07),
        inset 0 1px 0 rgba(255,255,255,.05);
}

.login-logo {
    width: 74px;
    height: 74px;
    margin: 0 auto 18px;
    border-radius: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    background: linear-gradient(145deg,#ffb84d,#ff6b1a);
    box-shadow: 0 12px 35px rgba(255,120,30,.25);
}

.login-title {
    text-align: center;
    color: #fff;
    font-size: 29px;
    font-weight: 800;
    letter-spacing: -.8px;
}

.login-subtitle {
    text-align: center;
    color: #89919e;
    font-size: 13px;
    margin: 7px 0 28px;
}

.login-label {
    color: #c8ced8;
    font-size: 13px;
    font-weight: 600;
    margin: 0 0 7px;
}

.stTextInput > div > div > input {
    background: #0c0f14 !important;
    color: #fff !important;
    border: 1px solid #252b35 !important;
    border-radius: 13px !important;
    min-height: 48px !important;
}

.stTextInput > div > div > input:focus {
    border-color: #ff9d3d !important;
    box-shadow: 0 0 0 1px #ff9d3d !important;
}

.login-btn button {
    width: 100%;
    min-height: 49px;
    border: 0 !important;
    border-radius: 13px !important;
    background: linear-gradient(135deg,#ffb84d,#ff6b1a) !important;
    color: #15100a !important;
    font-weight: 800 !important;
    box-shadow: 0 12px 30px rgba(255,110,20,.18);
}

.login-note {
    text-align: center;
    color: #626b78;
    font-size: 11px;
    margin-top: 20px;
}
</style>
"""

# =========================================================
# MAIN APP CSS
# =========================================================
APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #07090d;
    --panel: #101319;
    --panel2: #0c0f14;
    --border: #202630;
    --orange: #ff9d3d;
    --orange2: #ff6b1a;
    --text: #f4f6f8;
    --muted: #8d96a3;
}

.stApp {
    min-height: 100vh;
    background:
        radial-gradient(circle at 80% 0%, rgba(255,153,61,.08), transparent 24%),
        radial-gradient(circle at 0% 70%, rgba(255,107,26,.05), transparent 25%),
        var(--bg);
    color: var(--text);
    font-family: Inter, sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1280px;
    padding-top: 28px;
    padding-bottom: 55px;
}

.app-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 18px;
    padding: 16px 20px;
    margin-bottom: 24px;
    background: rgba(16,19,25,.86);
    border: 1px solid var(--border);
    border-radius: 18px;
    box-shadow: 0 15px 45px rgba(0,0,0,.28);
    backdrop-filter: blur(16px);
}

.brand {
    display: flex;
    align-items: center;
    gap: 13px;
}

.brand-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 25px;
    background: linear-gradient(145deg,#ffb84d,#ff6b1a);
    box-shadow: 0 8px 24px rgba(255,110,20,.2);
}

.brand-name {
    color: #fff;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: -.3px;
}

.brand-sub {
    color: #7e8794;
    font-size: 11px;
    margin-top: 2px;
}

.status {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #aeb7c4;
    font-size: 12px;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #45e58b;
    box-shadow: 0 0 12px rgba(69,229,139,.7);
}

.hero {
    padding: 34px;
    border-radius: 25px;
    background: linear-gradient(145deg, rgba(18,22,29,.98), rgba(11,13,18,.98));
    border: 1px solid var(--border);
    box-shadow: 0 25px 75px rgba(0,0,0,.34);
    margin-bottom: 26px;
}

.hero-kicker {
    color: var(--orange);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.hero-title {
    color: #fff;
    font-size: clamp(30px,4vw,50px);
    line-height: 1.05;
    font-weight: 800;
    letter-spacing: -1.8px;
    margin-bottom: 12px;
}

.hero-title span {
    color: var(--orange);
}

.hero-desc {
    max-width: 720px;
    color: #929aa6;
    line-height: 1.7;
    font-size: 14px;
}

.section-title {
    color: #fff;
    font-size: 18px;
    font-weight: 800;
    margin: 28px 0 13px;
}

.service-card {
    min-height: 112px;
    padding: 20px 12px;
    text-align: center;
    background: #101319;
    border: 1px solid #202630;
    border-radius: 18px;
    transition: .2s ease;
}

.service-card:hover {
    transform: translateY(-4px);
    border-color: rgba(255,157,61,.55);
    box-shadow: 0 14px 35px rgba(0,0,0,.25);
}

.service-icon {
    font-size: 25px;
    margin-bottom: 10px;
}

.service-name {
    color: #cdd3dc;
    font-size: 12px;
    font-weight: 700;
}

.quick-box {
    padding: 18px;
    background: #0e1116;
    border: 1px solid #202630;
    border-radius: 18px;
}

.stButton > button {
    width: 100%;
    min-height: 42px;
    border-radius: 12px !important;
    background: #12161d !important;
    border: 1px solid #282f3a !important;
    color: #dce1e8 !important;
    font-weight: 700 !important;
    transition: .18s ease;
}

.stButton > button:hover {
    border-color: var(--orange) !important;
    color: #fff !important;
    transform: translateY(-1px);
}

[data-testid="stChatMessage"] {
    background: #101319;
    border: 1px solid #202630;
    border-radius: 17px;
    margin-bottom: 10px;
}

[data-testid="stChatMessage"] p {
    color: #dbe0e7;
    line-height: 1.65;
}

[data-testid="stChatInput"] {
    background: transparent;
}

[data-testid="stChatInput"] textarea {
    background: #0e1116 !important;
    color: #fff !important;
    border: 1px solid #2a313c !important;
    border-radius: 15px !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 1px rgba(255,157,61,.3) !important;
}

.stTextInput label {
    color: #aeb6c2 !important;
}

.sidebar-title {
    color: #fff;
    font-weight: 800;
    font-size: 17px;
}

.footer {
    margin-top: 45px;
    padding-top: 20px;
    border-top: 1px solid #1b2028;
    text-align: center;
    color: #5f6875;
    font-size: 11px;
}

.logout-box {
    color: #8f98a5;
    font-size: 11px;
    margin-top: 5px;
}

@media(max-width:700px) {
    .block-container { padding: 12px; }
    .hero { padding: 24px 20px; }
    .hero-title { font-size: 31px; }
    .app-top { padding: 13px; }
}
</style>
"""

# =========================================================
# LOGIN SCREEN
# =========================================================
if not st.session_state.authenticated:
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)

    st.markdown('<div class="login-wrap"><div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-logo">🤖</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-title">CSC HELPDESK AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="login-subtitle">Secure access • Digital Service Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="login-label">Username</div>', unsafe_allow_html=True)
    login_user = st.text_input(
        "Username",
        placeholder="Enter username",
        label_visibility="collapsed",
        key="login_user"
    )

    st.markdown('<div class="login-label">Password</div>', unsafe_allow_html=True)
    login_pass = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password",
        label_visibility="collapsed",
        key="login_pass"
    )

    st.markdown('<div class="login-btn">', unsafe_allow_html=True)
    login_clicked = st.button("LOGIN  →")
    st.markdown('</div>', unsafe_allow_html=True)

    if login_clicked:
        if login_user == USERNAME and login_pass == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.markdown(
        '<div class="login-note">Authorized users only</div></div></div>',
        unsafe_allow_html=True
    )
    st.stop()


# =========================================================
# GEMINI
# =========================================================
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY is not configured.")
    st.stop()

client = genai.Client(api_key=API_KEY)


# =========================================================
# SERVICE CATALOG
# =========================================================
SERVICE_CATALOG = {
    "Aadhaar Print": {
        "keywords": ["aadhaar print", "aadhar print", "aadhaar nikalna"],
        "service_charge": 50,
        "official_fee": "Official portal/rules ke according",
        "documents": "Aadhaar number/card details",
        "time": "5-10 minute"
    },
    "PAN Card Apply": {
        "keywords": ["pan card", "pan apply", "new pan", "pan banana"],
        "service_charge": 350,
        "official_fee": "Portal ke according",
        "documents": "Aadhaar + required PAN documents",
        "time": "Application submission ke baad processing"
    },
    "PAN Correction": {
        "keywords": ["pan correction", "pan me correction", "pan update"],
        "service_charge": 350,
        "official_fee": "Portal ke according",
        "documents": "Required correction proof",
        "time": "Application processing ke according"
    },
    "Income Certificate": {
        "keywords": ["income certificate", "aay praman patra", "aay certificate"],
        "service_charge": 500,
        "official_fee": "Portal/department ke according",
        "documents": "Required identity/address/income documents",
        "time": "Department processing ke according"
    },
    "Caste Certificate": {
        "keywords": ["caste certificate", "jati praman patra", "jati certificate"],
        "service_charge": 500,
        "official_fee": "Portal/department ke according",
        "documents": "Required identity and caste-related documents",
        "time": "Department processing ke according"
    },
    "Residence Certificate": {
        "keywords": ["residence certificate", "niwas praman patra", "niwas certificate", "domicile"],
        "service_charge": 500,
        "official_fee": "Portal/department ke according",
        "documents": "Required identity/address documents",
        "time": "Department processing ke according"
    },
    "Online Form Filling": {
        "keywords": ["online form", "form bharna", "online application", "form filling"],
        "service_charge": 150,
        "official_fee": "Portal fee, if any, is separate",
        "documents": "Form ke according",
        "time": "10-30 minute"
    },
    "Print": {
        "keywords": ["print", "document print", "printout"],
        "service_charge": 5,
        "official_fee": "N/A",
        "documents": "File/document",
        "time": "2-5 minute"
    },
    "Scan": {
        "keywords": ["scan", "document scan"],
        "service_charge": 10,
        "official_fee": "N/A",
        "documents": "Original document",
        "time": "2-5 minute"
    },
}

SERVICE_CATALOG_TEXT = "\n".join(
    f"- {name}: hamara charge ₹{data['service_charge']}; "
    f"official fee: {data['official_fee']}; "
    f"documents: {data['documents']}; time: {data['time']}; "
    f"keywords: {', '.join(data['keywords'])}"
    for name, data in SERVICE_CATALOG.items()
)


# =========================================================
# SYSTEM PROMPT
# =========================================================
SYSTEM_PROMPT = f"""
You are CSC_HELPDESK_AI, a private customer-service assistant for OUR CSC / Jan Seva / Digital Service Centre.

Your main job is to understand the customer's work, tell them whether OUR CENTRE can help with it, and give the configured service charge.

IMPORTANT:
- You represent OUR SERVICE CENTRE, not a government department.
- Never promise government approval. Say we can help/apply/process; final approval depends on the concerned department.
- Use ONLY SERVICE_CATALOG below for our centre's charges. Never invent a price.
- If the requested service is not configured, say its charge is not configured and ask the customer to contact the centre.
- Do not invent government fees, deadlines, eligibility or rules.
- Never ask for OTP, password, UPI PIN, ATM PIN, CVV or other sensitive credentials.
- For changing government information, advise verification on the official portal.

LANGUAGE:
- Hindi question = Hindi answer.
- Hinglish question = Hinglish answer.
- English question = English answer.

For a service/price question, prefer:
✅ Haan, ye kaam humare yahan ho jayega.
📌 Kaam: <service>
💰 Hamara charge: ₹<service charge>
🏛️ Official/Government fee: <configured value>
📄 Zaroori documents: <configured documents>
⏱️ Approx. time: <configured time>

Then:
"Final approval/processing concerned government department ke rules ke according hota hai."

If the user only asks whether it can be done, answer directly first.
If the user asks only the charge, give the charge directly.
For multiple services, list each separately.

SERVICE CATALOG:
{SERVICE_CATALOG_TEXT}
"""


# =========================================================
# SESSION MEMORY
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ Control Panel</div>', unsafe_allow_html=True)
    st.caption("CSC Helpdesk AI")

    if st.button("🆕 New Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("**Available Services**")
    for service in SERVICE_CATALOG:
        st.write("•", service)


# =========================================================
# TOP BAR
# =========================================================
st.markdown(
    """
    <div class="app-top">
        <div class="brand">
            <div class="brand-icon">🤖</div>
            <div>
                <div class="brand-name">CSC HELPDESK AI</div>
                <div class="brand-sub">Digital Service Assistant</div>
            </div>
        </div>
        <div class="status">
            <span class="status-dot"></span>
            AI Assistant Online
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HERO
# =========================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">SMART DIGITAL SERVICE CENTRE</div>
        <div class="hero-title">Aapka kaam, <span>hamari madad.</span></div>
        <div class="hero-desc">
            Service ke baare mein poochhiye, availability samajhiye,
            required documents aur hamara configured charge jaaniye.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SERVICES
# =========================================================
st.markdown('<div class="section-title">Services</div>', unsafe_allow_html=True)

services = [
    ("🪪", "Aadhaar"),
    ("💳", "PAN Card"),
    ("📦", "Ration Card"),
    ("🌾", "PM Kisan"),
    ("🏥", "Ayushman"),
    ("📄", "Certificates"),
    ("👤", "Pension"),
    ("💻", "e-District"),
    ("🏢", "CSC Services"),
    ("＋", "More Services"),
]

cols = st.columns(10)

for col, (icon, name) in zip(cols, services):
    with col:
        st.markdown(
            f"""
            <div class="service-card">
                <div class="service-icon">{icon}</div>
                <div class="service-name">{name}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# QUICK QUESTIONS
# =========================================================
st.markdown('<div class="section-title">Quick Questions</div>', unsafe_allow_html=True)
st.markdown('<div class="quick-box">', unsafe_allow_html=True)

q1, q2, q3, q4 = st.columns(4)
popular_question = None

with q1:
    if st.button("Aadhaar Print"):
        popular_question = "Aadhaar print ka charge kitna hai?"

with q2:
    if st.button("PAN Card"):
        popular_question = "PAN card banwane ka charge kitna hai aur kya documents lagenge?"

with q3:
    if st.button("Certificate"):
        popular_question = "Income, caste ya residence certificate ka kaam ho jayega? Charge batao."

with q4:
    if st.button("Online Form"):
        popular_question = "Online form bharne ka charge kitna hai?"

st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# OLD MESSAGES
# =========================================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================================================
# USER INPUT
# =========================================================
user_message = st.chat_input(
    "Apna sawaal likhiye... jaise: PAN card banwane ka charge kitna hai?"
)

if popular_question:
    user_message = popular_question


# =========================================================
# AI RESPONSE
# =========================================================
if user_message:

    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        try:
            response = None

            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=user_message,
                        config={
                            "system_instruction": SYSTEM_PROMPT
                        }
                    )
                    break

                except Exception as e:
                    if "503" in str(e) and attempt < 2:
                        time.sleep(3)
                    else:
                        raise e

            reply = response.text
            st.markdown(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

        except Exception:
            reply = (
                "Main abhi thoda busy hoon. Kripya hamare centre ke Owner "
                "Vicky Choudhary Ji se baat kar lijiye. "
                "Mobile No.: 8826066468."
            )

            st.warning(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })


# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div class="footer">
        CSC_HELPDESK_AI • Digital Service Assistant
        <br><br>
        Fast • Simple • Secure
    </div>
    """,
    unsafe_allow_html=True
)
