import os
import time
import streamlit as st
from google import genai

# =========================================================
# PAGE
# =========================================================
st.set_page_config(
    page_title="CSC Helpdesk AI",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# LOGIN SETTINGS
# =========================================================
# CHANGE THESE IF YOU WANT
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "12345"

USERNAME = st.secrets.get("APP_USERNAME", DEFAULT_USERNAME)
PASSWORD = st.secrets.get("APP_PASSWORD", DEFAULT_PASSWORD)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# GLOBAL CSS
# =========================================================
GLOBAL_CSS = r"""
<style>
/* ---------- RESET / BASE ---------- */
html, body, [class*="css"] {
    font-family: Inter, Arial, Helvetica, sans-serif !important;
}

.stApp {
    background: #07090c !important;
    color: #f5f5f5 !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 85% 5%, rgba(246,166,35,.08), transparent 25%),
        radial-gradient(circle at 5% 80%, rgba(246,166,35,.045), transparent 25%),
        #07090c !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    background: transparent !important;
}

.block-container {
    max-width: 1220px !important;
    padding-top: 28px !important;
    padding-bottom: 60px !important;
}

/* ---------- LOGIN ---------- */
.login-page {
    min-height: 88vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.login-card {
    width: 410px;
    max-width: 94vw;
    padding: 42px 38px 34px;
    background: #101319;
    border: 1px solid #252b34;
    border-radius: 24px;
    box-shadow: 0 35px 90px rgba(0,0,0,.60);
}

.login-mark {
    width: 72px;
    height: 72px;
    margin: 0 auto 20px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(145deg, #ffc15a, #f47a18);
    color: #111;
    font-size: 28px;
    font-weight: 900;
    box-shadow: 0 12px 35px rgba(244,122,24,.22);
}

.login-title {
    text-align: center;
    color: #ffffff;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -.8px;
}

.login-subtitle {
    text-align: center;
    color: #858d99;
    font-size: 13px;
    margin-top: 7px;
    margin-bottom: 28px;
}

.login-label {
    color: #cbd1d9;
    font-size: 12px;
    font-weight: 700;
    margin: 13px 0 7px;
}

.login-info {
    text-align: center;
    color: #606975;
    font-size: 11px;
    margin-top: 18px;
}

/* ---------- INPUTS ---------- */
.stTextInput > div > div > input {
    height: 48px !important;
    background: #0a0d11 !important;
    color: #ffffff !important;
    border: 1px solid #2a3039 !important;
    border-radius: 12px !important;
    padding: 0 14px !important;
}

.stTextInput > div > div > input:focus {
    border-color: #f3a437 !important;
    box-shadow: 0 0 0 1px #f3a437 !important;
}

.stTextInput label {
    display: none !important;
}

/* ---------- ALL BUTTONS ---------- */
.stButton > button {
    width: 100% !important;
    min-height: 43px !important;
    border-radius: 11px !important;
    background: #12161c !important;
    border: 1px solid #2a313b !important;
    color: #e5e8ed !important;
    font-weight: 700 !important;
    transition: all .18s ease !important;
}

.stButton > button:hover {
    border-color: #f3a437 !important;
    color: #ffffff !important;
    transform: translateY(-1px) !important;
    background: #171b21 !important;
}

.login-button .stButton > button {
    background: linear-gradient(135deg, #ffc15a, #f47a18) !important;
    border: none !important;
    color: #17120b !important;
    min-height: 49px !important;
    font-size: 14px !important;
    box-shadow: 0 12px 28px rgba(244,122,24,.18) !important;
}

.login-button .stButton > button:hover {
    background: linear-gradient(135deg, #ffd078, #ff8730) !important;
    color: #17120b !important;
}

/* ---------- TOP BAR ---------- */
.topbar {
    height: 70px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 19px;
    background: rgba(16,19,25,.96);
    border: 1px solid #242a33;
    border-radius: 18px;
    margin-bottom: 24px;
    box-shadow: 0 18px 45px rgba(0,0,0,.28);
}

.brand-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-mark {
    width: 43px;
    height: 43px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(145deg,#ffc15a,#f47a18);
    color: #15100a;
    font-weight: 900;
    font-size: 19px;
}

.brand-title {
    color: #ffffff;
    font-size: 16px;
    font-weight: 800;
}

.brand-caption {
    color: #707986;
    font-size: 10px;
    margin-top: 2px;
}

.online-pill {
    display: flex;
    align-items: center;
    gap: 7px;
    color: #aab2bd;
    font-size: 11px;
}

.online-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #45d98a;
    box-shadow: 0 0 10px rgba(69,217,138,.7);
}

/* ---------- HERO ---------- */
.hero {
    position: relative;
    overflow: hidden;
    padding: 42px 40px;
    border-radius: 24px;
    background:
        linear-gradient(135deg, rgba(20,23,30,.98), rgba(11,13,17,.98));
    border: 1px solid #242a33;
    box-shadow: 0 25px 70px rgba(0,0,0,.32);
    margin-bottom: 28px;
}

.hero:after {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    right: -100px;
    top: -130px;
    border-radius: 50%;
    background: rgba(246,166,35,.07);
    filter: blur(25px);
}

.hero-small {
    color: #f1a53a;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 10px;
}

.hero-title {
    color: #ffffff;
    font-size: clamp(31px, 4vw, 49px);
    line-height: 1.06;
    font-weight: 800;
    letter-spacing: -1.8px;
    margin-bottom: 13px;
}

.hero-title span {
    color: #f4a63a;
}

.hero-description {
    max-width: 760px;
    color: #8e97a3;
    font-size: 14px;
    line-height: 1.75;
}

/* ---------- SECTION ---------- */
.section-title {
    color: #f7f7f7;
    font-size: 18px;
    font-weight: 800;
    margin: 30px 0 14px;
}

/* ---------- SERVICE CARDS ---------- */
.service-card {
    height: 112px;
    box-sizing: border-box;
    padding: 19px 8px;
    text-align: center;
    background: #101319;
    border: 1px solid #222932;
    border-radius: 16px;
    transition: all .18s ease;
}

.service-card:hover {
    transform: translateY(-4px);
    border-color: rgba(244,166,58,.55);
    box-shadow: 0 15px 35px rgba(0,0,0,.28);
}

.service-icon {
    color: #f4a63a;
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 11px;
}

.service-name {
    color: #c8ced7;
    font-size: 11px;
    font-weight: 700;
}

/* ---------- QUICK BOX ---------- */
.quick-box {
    padding: 17px;
    background: #0e1116;
    border: 1px solid #222932;
    border-radius: 18px;
}

/* ---------- CHAT ---------- */
[data-testid="stChatMessage"] {
    background: #101319 !important;
    border: 1px solid #222932 !important;
    border-radius: 17px !important;
    margin-bottom: 11px !important;
}

[data-testid="stChatMessage"] p {
    color: #d9dee5 !important;
    line-height: 1.7 !important;
}

[data-testid="stChatInput"] {
    background: transparent !important;
}

[data-testid="stChatInput"] > div {
    background: #0e1116 !important;
    border: 1px solid #292f39 !important;
    border-radius: 15px !important;
}

[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
    background: transparent !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: #f4a63a !important;
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background: #0b0e12 !important;
    border-right: 1px solid #242a33 !important;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 28px !important;
}

.sidebar-heading {
    color: #ffffff;
    font-size: 17px;
    font-weight: 800;
}

.sidebar-sub {
    color: #69727f;
    font-size: 11px;
    margin: 4px 0 20px;
}

/* ---------- ALERT ---------- */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
}

/* ---------- FOOTER ---------- */
.footer {
    color: #59616d;
    font-size: 10px;
    text-align: center;
    margin-top: 45px;
    padding-top: 20px;
    border-top: 1px solid #1c222a;
}

/* ---------- MOBILE ---------- */
@media(max-width: 700px) {
    .block-container {
        padding: 14px !important;
    }

    .hero {
        padding: 28px 22px;
    }

    .hero-title {
        font-size: 31px;
    }

    .topbar {
        padding: 0 13px;
    }

    .online-pill {
        display: none;
    }
}
</style>
"""

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# =========================================================
# LOGIN
# =========================================================
if not st.session_state.authenticated:

    st.markdown('<div class="login-page"><div class="login-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="login-mark">C</div>'
        '<div class="login-title">CSC HELPDESK AI</div>'
        '<div class="login-subtitle">Secure access to your digital service assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="login-label">USERNAME</div>', unsafe_allow_html=True)
    login_user = st.text_input(
        "Username",
        placeholder="Enter username",
        label_visibility="collapsed",
        key="login_user"
    )

    st.markdown('<div class="login-label">PASSWORD</div>', unsafe_allow_html=True)
    login_pass = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password",
        label_visibility="collapsed",
        key="login_pass"
    )

    st.markdown('<div class="login-button">', unsafe_allow_html=True)
    clicked = st.button("SIGN IN  →")
    st.markdown('</div>', unsafe_allow_html=True)

    if clicked:
        if login_user == USERNAME and login_pass == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Username ya password galat hai.")

    st.markdown(
        '<div class="login-info">Authorized users only • Secure dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown('</div></div>', unsafe_allow_html=True)
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
# AI PROMPT
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
Haan, ye kaam humare yahan ho jayega.
Kaam: <service>
Hamara charge: ₹<service charge>
Official/Government fee: <configured value>
Zaroori documents: <configured documents>
Approx. time: <configured time>

Final approval/processing concerned government department ke rules ke according hota hai.

SERVICE CATALOG:
{SERVICE_CATALOG_TEXT}
"""


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown('<div class="sidebar-heading">CSC HELPDESK AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Control Panel</div>', unsafe_allow_html=True)

    if st.button("New Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("**Configured Services**")

    for name in SERVICE_CATALOG:
        st.caption(name)


# =========================================================
# TOP BAR
# =========================================================
st.markdown(
    """
    <div class="topbar">
        <div class="brand-left">
            <div class="brand-mark">C</div>
            <div>
                <div class="brand-title">CSC HELPDESK AI</div>
                <div class="brand-caption">Digital Service Assistant</div>
            </div>
        </div>
        <div class="online-pill">
            <span class="online-dot"></span>
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
        <div class="hero-small">SMART DIGITAL SERVICE CENTRE</div>
        <div class="hero-title">Aapka kaam, <span>hamari madad.</span></div>
        <div class="hero-description">
            Kisi bhi configured service ke baare mein poochhiye.
            AI aapko service, documents, approximate time aur centre ka charge batayega.
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
    ("A", "Aadhaar"),
    ("P", "PAN Card"),
    ("R", "Ration Card"),
    ("K", "PM Kisan"),
    ("H", "Ayushman"),
    ("C", "Certificates"),
    ("P", "Pension"),
    ("E", "e-District"),
    ("C", "CSC Services"),
    ("+", "More Services"),
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
# CHAT HISTORY
# =========================================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================================================
# INPUT
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
        CSC HELPDESK AI &nbsp; • &nbsp; Digital Service Assistant
        <br><br>
        Fast &nbsp; • &nbsp; Simple &nbsp; • &nbsp; Secure
    </div>
    """,
    unsafe_allow_html=True
)
