
import os
import json
import hashlib
import hmac
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st
import streamlit.components.v1 as components
from google import genai

# =====================================================
# CSC HELPDESK AI | FUTURISTIC COMMAND CENTER
# =====================================================

st.set_page_config(
    page_title="CSC HELPDESK AI | COMMAND CENTER",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_secret(key, default=""):
    try:
        return st.secrets.get(key, os.environ.get(key, default))
    except Exception:
        return os.environ.get(key, default)

API_KEY = get_secret("GEMINI_API_KEY")
APP_USERNAME = get_secret("APP_USERNAME", "admin")
APP_PASSWORD = get_secret("APP_PASSWORD", "12345")

if not API_KEY:
    st.error("GEMINI_API_KEY set nahi hai. Streamlit Secrets check karein.")
    st.stop()

@st.cache_resource
def get_client(key):
    return genai.Client(api_key=key)

client = get_client(API_KEY)

# =====================================================
# SESSION STATE
# =====================================================

defaults = {
    "authenticated": False,
    "messages": [],
    "voice_enabled": True,
    "voice_style": "BOSS DEEP",
    "pending_prompt": None,
    "audio_hash": None,
    "audio_counter": 0,
    "selected_model": "gemini-2.5-flash"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def india_now():
    return datetime.now(ZoneInfo("Asia/Kolkata"))

# =====================================================
# SERVICE DATA
# =====================================================

SERVICES = [
    {"icon": "🪪", "name": "Aadhaar Services", "price": 50,
     "desc": "Aadhaar print, update aur guidance"},
    {"icon": "💳", "name": "PAN Card", "price": 350,
     "desc": "New PAN aur correction"},
    {"icon": "🌾", "name": "Ration Card", "price": 100,
     "desc": "Ration card aur e-KYC"},
    {"icon": "🌱", "name": "PM Kisan", "price": 100,
     "desc": "Registration aur e-KYC"},
    {"icon": "🏥", "name": "Ayushman Card", "price": 100,
     "desc": "Ayushman card guidance"},
    {"icon": "📄", "name": "Income Certificate", "price": 500,
     "desc": "Income certificate assistance"},
    {"icon": "📜", "name": "Caste Certificate", "price": 500,
     "desc": "Caste certificate assistance"},
    {"icon": "🏠", "name": "Residence Certificate", "price": 500,
     "desc": "Residence certificate assistance"},
    {"icon": "📝", "name": "Online Forms", "price": 150,
     "desc": "Online application assistance"},
    {"icon": "🖨️", "name": "Printout", "price": 5,
     "desc": "Document printing"},
    {"icon": "📑", "name": "Document Scan", "price": 10,
     "desc": "Document scanning"}
]

service_list = "\n".join(
    f"{s['name']}: Centre service charge ₹{s['price']}. {s['desc']}"
    for s in SERVICES
)

# =====================================================
# AI SYSTEM PROMPT
# =====================================================

def system_prompt():
    return f"""
You are CSC HELPDESK AI, a professional digital service assistant.

Current India date and time:
{india_now().strftime("%d-%m-%Y %I:%M %p")} IST.

You help users with Indian government and CSC services.

AVAILABLE CENTRE SERVICES:
{service_list}

You can guide users about:
Aadhaar, PAN Card, Ration Card, PM Kisan, Ayushman Card,
Income Certificate, Caste Certificate, Residence Certificate,
Birth Certificate, Pension, e-District, Government Forms,
CSC services and digital literacy.

LANGUAGE:
- Hindi input: answer in simple Hindi.
- Hinglish input: answer in natural Hinglish.
- English input: answer in clear English.
- Explain difficult concepts in easy steps.

BEHAVIOUR:
- Be professional, friendly and helpful.
- Address the user as Boss when it feels natural.
- Give step-by-step instructions.
- Use headings and bullet points when useful.
- Keep simple questions concise.
- Never invent government rules, fees, deadlines or eligibility.
- Clearly distinguish centre service charges from government fees.
- Suggest checking the official government portal for changing rules.
- Never ask for OTP, passwords, UPI PIN or CVV.
- Never claim that an application has been submitted or approved
  without confirmation from an actual integration.
- Do not claim to have live access to government records.
"""

# =====================================================
# FUTURISTIC THEME
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Orbitron:wght@500;600;700;800&display=swap');

:root {
    --bg: #070d1c;
    --panel: #101a30;
    --panel2: #121f39;
    --cyan: #00e5ff;
    --blue: #3984ff;
    --purple: #a855f7;
    --green: #00f5a0;
    --gold: #ffc857;
    --white: #edf6ff;
    --muted: #91a8c8;
    --line: rgba(0,229,255,.20);
}

/* MAIN BACKGROUND */

.stApp {
    background:
        radial-gradient(ellipse at 12% 12%, rgba(0,180,255,.14), transparent 32%),
        radial-gradient(ellipse at 90% 15%, rgba(168,85,247,.15), transparent 34%),
        radial-gradient(ellipse at 60% 95%, rgba(0,245,160,.07), transparent 36%),
        linear-gradient(135deg, #070d1c 0%, #0a1022 48%, #0b1026 100%) !important;
    color: var(--white) !important;
}

[data-testid="stAppViewContainer"] {
    background: transparent !important;
}

[data-testid="stHeader"] {
    background: rgba(7,13,28,.7) !important;
}

[data-testid="stToolbar"] {
    background: transparent !important;
}

.block-container {
    max-width: 1500px !important;
    padding-top: 1.2rem !important;
    padding-bottom: 5rem !important;
}

/* SUBTLE GRID BACKGROUND */

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background-image:
        linear-gradient(rgba(0,229,255,.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,229,255,.025) 1px, transparent 1px);
    background-size: 35px 35px;
    mask-image: linear-gradient(to bottom, black, transparent 90%);
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background:
        radial-gradient(ellipse at top left, rgba(0,229,255,.13), transparent 48%),
        linear-gradient(180deg, #0c172d, #091020) !important;
    border-right: 1px solid rgba(0,229,255,.28) !important;
}

[data-testid="stSidebar"] > div {
    background: transparent !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] small {
    color: #b7c9e5 !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #dcecff !important;
}

/* BRAND */

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0 20px;
    margin-bottom: 20px;
    border-bottom: 1px solid rgba(0,229,255,.23);
}

.brand-logo {
    width: 54px;
    height: 54px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    border: 1px solid rgba(0,229,255,.7);
    border-radius: 15px;
    background: linear-gradient(145deg,#153d68,#101b39);
    color: #00e5ff;
    font-family: Orbitron, sans-serif;
    font-weight: 800;
    font-size: 15px;
    box-shadow: 0 0 12px rgba(0,229,255,.20),
                inset 0 0 15px rgba(0,229,255,.10);
}

.brand-title {
    font-family: Orbitron, sans-serif;
    color: #00e5ff;
    font-size: 13px;
    font-weight: 800;
    text-shadow: 0 0 12px rgba(0,229,255,.5);
}

.brand-subtitle {
    font-size: 8px;
    letter-spacing: 1.3px;
    color: #92a9ca;
    margin-top: 6px;
}

/* TOP BAR */

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    padding: 13px 19px;
    border: 1px solid rgba(0,229,255,.24);
    border-radius: 12px;
    background: linear-gradient(100deg,
        rgba(16,33,61,.94),rgba(19,24,52,.90));
    box-shadow: 0 0 22px rgba(0,150,255,.06);
    margin-bottom: 20px;
}

.topbar-title {
    font-family: Orbitron, sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: #b8eaff;
    letter-spacing: .7px;
}

.online-pill {
    border: 1px solid rgba(0,245,160,.35);
    background: rgba(0,245,160,.08);
    color: #00f5a0;
    padding: 7px 11px;
    border-radius: 30px;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: .7px;
    box-shadow: 0 0 12px rgba(0,245,160,.08);
}

/* HERO */

.hero {
    position: relative;
    overflow: hidden;
    padding: 32px 34px;
    border-radius: 19px;
    border: 1px solid rgba(0,229,255,.38);
    background:
        radial-gradient(ellipse at 88% 40%, rgba(0,229,255,.15), transparent 40%),
        radial-gradient(ellipse at 60% 100%, rgba(168,85,247,.15), transparent 50%),
        linear-gradient(120deg,#102345,#14244a 55%,#172044);
    box-shadow: 0 10px 35px rgba(0,0,0,.23),
                0 0 24px rgba(0,229,255,.07);
    margin-bottom: 22px;
}

.hero::after {
    content: "AI";
    position: absolute;
    right: 7%;
    top: 50%;
    transform: translateY(-50%);
    font-family: Orbitron, sans-serif;
    font-size: clamp(75px, 13vw, 155px);
    font-weight: 900;
    color: rgba(0,229,255,.055);
    text-shadow: 0 0 28px rgba(0,229,255,.14);
    pointer-events: none;
}

.hero-tag {
    display: inline-block;
    border: 1px solid rgba(0,229,255,.35);
    border-radius: 5px;
    padding: 7px 10px;
    color: #00e5ff;
    background: rgba(0,229,255,.07);
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

.hero h1 {
    position: relative;
    z-index: 1;
    font-family: Orbitron, sans-serif;
    font-size: clamp(25px, 4vw, 43px);
    font-weight: 800;
    letter-spacing: -.8px;
    color: #f2fbff;
    margin: 19px 0 11px;
    text-shadow: 0 0 20px rgba(0,229,255,.19);
}

.hero p {
    position: relative;
    z-index: 1;
    max-width: 690px;
    color: #b5c9e6;
    font-size: 13px;
    line-height: 1.9;
}

.hero-line {
    width: 65px;
    height: 4px;
    border-radius: 10px;
    margin-top: 20px;
    background: linear-gradient(90deg,#00e5ff,#a855f7,#ffc857);
    box-shadow: 0 0 14px rgba(0,229,255,.55);
}

/* HEADINGS */

.section-title {
    font-family: Orbitron, sans-serif;
    font-size: 14px;
    color: #e6f7ff;
    font-weight: 700;
    letter-spacing: .4px;
    margin: 25px 0 5px;
}

.section-subtitle {
    font-size: 11px;
    color: #8299bb;
    margin-bottom: 15px;
}

/* STATS */

.stat-card {
    position: relative;
    overflow: hidden;
    min-height: 105px;
    padding: 17px;
    border-radius: 13px;
    border: 1px solid rgba(0,229,255,.22);
    background: linear-gradient(145deg,
        rgba(19,36,65,.98),rgba(13,23,44,.98));
    box-shadow: 0 6px 18px rgba(0,0,0,.14);
}

.stat-card::after {
    content: "";
    position: absolute;
    width: 90px;
    height: 90px;
    border-radius: 50%;
    right: -40px;
    top: -45px;
    background: rgba(0,229,255,.08);
    filter: blur(5px);
}

.stat-label {
    color: #8ca9cb;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1px;
}

.stat-number {
    font-family: Orbitron, sans-serif;
    font-size: 25px;
    font-weight: 800;
    margin-top: 11px;
    color: #00e5ff;
    text-shadow: 0 0 13px rgba(0,229,255,.30);
}

.stat-blue .stat-number {
    color: #6da6ff;
    text-shadow: 0 0 13px rgba(57,132,255,.35);
}

.stat-purple .stat-number {
    color: #c59aff;
    text-shadow: 0 0 13px rgba(168,85,247,.35);
}

/* SERVICE CARDS */

.service-card {
    position: relative;
    overflow: hidden;
    min-height: 145px;
    padding: 16px 11px;
    text-align: center;
    border-radius: 13px;
    border: 1px solid rgba(0,229,255,.19);
    background: linear-gradient(145deg,
        rgba(18,34,61,.97),rgba(12,22,43,.98));
    box-shadow: 0 5px 17px rgba(0,0,0,.13);
    transition: all .22s ease;
}

.service-card:hover {
    transform: translateY(-4px);
    border-color: rgba(0,229,255,.75);
    box-shadow: 0 8px 25px rgba(0,229,255,.12);
}

.service-icon {
    width: 47px;
    height: 47px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 12px;
    border: 1px solid rgba(0,229,255,.27);
    border-radius: 13px;
    background: linear-gradient(140deg,
        rgba(0,229,255,.15),rgba(168,85,247,.13));
    font-size: 22px;
    box-shadow: inset 0 0 15px rgba(0,229,255,.07);
}

.service-name {
    color: #e7f4ff;
    font-size: 11px;
    font-weight: 700;
    line-height: 1.5;
}

.service-price {
    color: #00e5ff;
    font-family: Orbitron, sans-serif;
    font-size: 9px;
    margin-top: 8px;
}

.service-desc {
    color: #8399b9;
    font-size: 9px;
    margin-top: 7px;
    line-height: 1.5;
}

/* QUICK BUTTONS */

.stButton > button {
    background: linear-gradient(110deg,#122747,#162344) !important;
    color: #ccecff !important;
    border: 1px solid rgba(0,229,255,.27) !important;
    border-radius: 9px !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    min-height: 39px !important;
    transition: .2s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(100deg,#075b79,#26356e) !important;
    color: #fff !important;
    border-color: #00e5ff !important;
    box-shadow: 0 0 16px rgba(0,229,255,.17) !important;
    transform: translateY(-1px);
}

/* CHAT MESSAGES */

[data-testid="stChatMessage"] {
    background: linear-gradient(120deg,
        rgba(16,30,54,.98),rgba(13,24,46,.98)) !important;
    border: 1px solid rgba(0,229,255,.20) !important;
    border-radius: 13px !important;
    padding: 15px 17px !important;
    box-shadow: 0 5px 18px rgba(0,0,0,.15) !important;
    margin-bottom: 12px !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    border-left: 3px solid #a855f7 !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    border-left: 3px solid #00e5ff !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #d7e7fa !important;
    font-size: 13px !important;
    line-height: 1.8 !important;
}

[data-testid="stChatMessage"] strong {
    color: #00e5ff !important;
}

/* WELCOME */

.welcome {
    text-align: center;
    padding: 24px;
    margin: 17px 0;
    border: 1px solid rgba(0,229,255,.27);
    border-radius: 15px;
    background:
        radial-gradient(ellipse at 50% 0%,rgba(0,229,255,.10),transparent 65%),
        linear-gradient(145deg,#111f3a,#0e1931);
    box-shadow: 0 7px 23px rgba(0,0,0,.17);
}

.welcome-logo {
    width: 62px;
    height: 62px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 14px;
    border: 1px solid rgba(0,229,255,.65);
    border-radius: 17px;
    background: linear-gradient(140deg,#133b61,#211d51);
    color: #00e5ff;
    font-family: Orbitron, sans-serif;
    font-size: 17px;
    font-weight: 900;
    box-shadow: 0 0 22px rgba(0,229,255,.17);
}

.welcome h3 {
    color: #f2f8ff;
    font-family: Orbitron, sans-serif;
    font-size: 15px;
    font-weight: 700;
}

.welcome p {
    color: #95adcc;
    font-size: 11px;
    line-height: 1.8;
}

/* INFO */

.info-box {
    border: 1px solid rgba(0,229,255,.20);
    border-left: 3px solid #00e5ff;
    border-radius: 10px;
    padding: 13px 15px;
    color: #a9c3df;
    background: linear-gradient(100deg,
        rgba(0,229,255,.07),rgba(168,85,247,.05));
    font-size: 11px;
    line-height: 1.8;
    margin: 10px 0 16px;
}

.info-box b {
    color: #00e5ff;
}

/* CHAT INPUT */

[data-testid="stBottom"] {
    background: rgba(7,13,28,.97) !important;
    border-top: 1px solid rgba(0,229,255,.20) !important;
}

[data-testid="stBottom"] > div {
    background: transparent !important;
}

[data-testid="stChatInput"] > div {
    background: #101c33 !important;
    border: 1px solid rgba(0,229,255,.38) !important;
    border-radius: 12px !important;
    box-shadow: 0 0 19px rgba(0,229,255,.06) !important;
}

[data-testid="stChatInput"] textarea {
    color: #edf6ff !important;
    -webkit-text-fill-color: #edf6ff !important;
    font-size: 13px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #7993b6 !important;
    -webkit-text-fill-color: #7993b6 !important;
}

/* OTHER INPUTS */

.stTextInput input,
.stTextArea textarea,
div[data-baseweb="select"] > div {
    background: #101c33 !important;
    color: #edf6ff !important;
    border: 1px solid rgba(0,229,255,.24) !important;
    border-radius: 9px !important;
}

.stTextInput label,
.stSelectbox label {
    color: #b7c9e5 !important;
}

[data-testid="stAudioInput"] {
    background: rgba(16,28,51,.7) !important;
    border: 1px solid rgba(0,229,255,.2) !important;
    border-radius: 10px !important;
    padding: 10px !important;
}

.stAlert {
    border-radius: 10px !important;
}

/* DIVIDER + FOOTER */

hr {
    border-color: rgba(0,229,255,.16) !important;
}

.footer {
    text-align: center;
    margin-top: 30px;
    padding: 19px 5px;
    border-top: 1px solid rgba(0,229,255,.15);
    color: #6f87a8;
    font-size: 9px;
    letter-spacing: 1px;
    line-height: 2;
}

.footer b {
    color: #00e5ff;
}

/* MOBILE */

@media(max-width: 700px) {
    .block-container {
        padding-left: 12px !important;
        padding-right: 12px !important;
    }

    .hero {
        padding: 23px 19px;
    }

    .hero::after {
        right: 4%;
        opacity: .55;
    }

    .stat-card {
        padding: 12px;
        min-height: 90px;
    }

    .service-card {
        min-height: 135px;
    }

    .topbar {
        padding: 11px;
    }
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# VOICE ENGINE
# =====================================================

def speak_text(text, style):
    text_json = json.dumps(str(text), ensure_ascii=False)
    style_json = json.dumps(style)

    html = """
    <script>
    (() => {
        const text = __TEXT__;
        const style = __STYLE__;

        if (!window.speechSynthesis || !text) return;

        const synth = window.speechSynthesis;
        synth.cancel();

        function speak() {
            const voices = synth.getVoices();
            const isHindi = /[\\u0900-\\u097F]/.test(text);
            const lang = isHindi ? "hi" : "en";

            const matches = voices.filter(v =>
                v.lang.toLowerCase().startsWith(lang)
            );

            const femaleNames = /zira|samantha|aria|susan|heera/i;
            const maleNames = /david|mark|daniel|alex|james|george|hemant|madhur|guy|ryan/i;

            const voice =
                matches.find(v => maleNames.test(v.name)) ||
                matches.find(v => !femaleNames.test(v.name)) ||
                matches[0] ||
                voices[0];

            const utterance = new SpeechSynthesisUtterance(text);

            if (voice) {
                utterance.voice = voice;
                utterance.lang = voice.lang;
            } else {
                utterance.lang = isHindi ? "hi-IN" : "en-US";
            }

            if (style === "BOSS DEEP") {
                utterance.rate = 0.82;
                utterance.pitch = 0.55;
            } else if (style === "ULTRA ROBOTIC") {
                utterance.rate = 0.76;
                utterance.pitch = 0.4;
            } else {
                utterance.rate = 0.90;
                utterance.pitch = 0.68;
            }

            utterance.volume = 1;
            synth.speak(utterance);
        }

        if (synth.getVoices().length) {
            speak();
        } else {
            synth.onvoiceschanged = speak;
        }
    })();
    </script>
    """

    html = html.replace("__TEXT__", text_json)
    html = html.replace("__STYLE__", style_json)
    components.html(html, height=0)

# =====================================================
# LOGIN SCREEN
# =====================================================

if not st.session_state.authenticated:
    st.markdown("""
    <div class="welcome" style="max-width:570px;margin:65px auto 20px">
        <div class="welcome-logo">CSC</div>
        <div style="color:#00e5ff;font-size:9px;letter-spacing:2px">
            SECURE ACCESS TERMINAL
        </div>
        <h3 style="font-size:21px;margin-top:12px">
            CSC HELPDESK AI
        </h3>
        <p>Futuristic Digital Seva Command Center</p>
    </div>
    """, unsafe_allow_html=True)

    _, login_col, _ = st.columns([1, 1.2, 1])

    with login_col:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password"
            )
            submitted = st.form_submit_button(
                "🔐  ACCESS SYSTEM",
                use_container_width=True
            )

        if submitted:
            if (
                hmac.compare_digest(username, APP_USERNAME)
                and hmac.compare_digest(password, APP_PASSWORD)
            ):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Access denied. Check username and password.")

    st.stop()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-logo">CSC</div>
        <div>
            <div class="brand-title">HELPDESK AI</div>
            <div class="brand-subtitle">DIGITAL COMMAND CENTER</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        🟢 <b>CORE SYSTEM ONLINE</b><br>
        AI response engine is ready.
    </div>
    """, unsafe_allow_html=True)

    now = india_now()
    st.caption("SYSTEM DATE & TIME")
    st.markdown(f"**{now.strftime('%d %B %Y')}**")
    st.caption(now.strftime("%I:%M:%S %p IST"))

    st.divider()
    st.markdown("#### ⚙️ AI CONFIGURATION")

    model_name = st.selectbox(
        "Gemini Engine",
        ["gemini-2.5-flash", "gemini-2.0-flash"],
        key="selected_model"
    )

    st.session_state.voice_enabled = st.toggle(
        "🔊 AI Voice Reply",
        value=st.session_state.voice_enabled
    )

    st.session_state.voice_style = st.selectbox(
        "VOICE PROFILE",
        ["BOSS DEEP", "ULTRA ROBOTIC", "COMMANDER"]
    )

    if st.button("▶ TEST VOICE", use_container_width=True):
        speak_text(
            "Namaste Boss. CSC Helpdesk AI system online hai.",
            st.session_state.voice_style
        )

    st.divider()
    st.markdown("#### 🗂️ CENTRE SERVICES")

    for service in SERVICES:
        st.caption(
            f"{service['icon']}  {service['name']}  |  ₹{service['price']}"
        )

    st.divider()

    if st.button("＋ NEW CHAT", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.session_state.audio_hash = None
        st.rerun()

    chat_text = "\n\n".join(
        f"{m['role'].upper()}:\n{m['content']}"
        for m in st.session_state.messages
    )

    st.download_button(
        "⬇ DOWNLOAD CHAT",
        data=chat_text,
        file_name="CSC_Helpdesk_Chat.txt",
        mime="text/plain",
        use_container_width=True,
        disabled=not bool(chat_text)
    )

    if st.button("⏻ LOGOUT", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.messages = []
        st.rerun()

# =====================================================
# MAIN DASHBOARD
# =====================================================

now = india_now()

st.markdown("""
<div class="topbar">
    <div class="topbar-title">◈ DIGITAL SEVA / COMMAND CENTER</div>
    <div class="online-pill">● SYSTEM ONLINE</div>
</div>

<div class="hero">
    <div class="hero-tag">✦ WELCOME TO DIGITAL INDIA</div>
    <h1>CSC HELPDESK AI</h1>
    <p>
        Your intelligent digital service assistant.
        Aadhaar, PAN Card, government certificates, online forms
        aur digital services ke liye smart assistance.
    </p>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# DASHBOARD STATS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">◈ AVAILABLE SERVICES</div>
        <div class="stat-number">{len(SERVICES):02d}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card stat-blue">
        <div class="stat-label">◈ CHAT MESSAGES</div>
        <div class="stat-number">{len(st.session_state.messages):02d}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card stat-purple">
        <div class="stat-label">◈ SYSTEM DATE</div>
        <div class="stat-number" style="font-size:18px">
            {now.strftime("%d-%m-%Y")}
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# DIGITAL SERVICE CARDS
# =====================================================

st.markdown(
    '<div class="section-title">◈ DIGITAL SERVICES</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Select a service to explore centre assistance.'
    '</div>',
    unsafe_allow_html=True
)

for start in range(0, len(SERVICES), 4):
    cols = st.columns(4)

    for i, service in enumerate(SERVICES[start:start+4]):
        with cols[i]:
            st.markdown(f"""
            <div class="service-card">
                <div class="service-icon">{service['icon']}</div>
                <div class="service-name">{service['name']}</div>
                <div class="service-price">FROM ₹{service['price']}</div>
                <div class="service-desc">{service['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

# =====================================================
# QUICK QUESTIONS
# =====================================================

st.markdown(
    '<div class="section-title">◈ QUICK COMMANDS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Choose a quick command or enter your own question.'
    '</div>',
    unsafe_allow_html=True
)

quick_questions = [
    ("🪪  Aadhaar Print", "Aadhaar print ka charge aur process batao."),
    ("💳  PAN Card", "PAN card banwane ke documents aur process batao."),
    ("📜  Certificate", "Income certificate kaise banwayen?"),
    ("📝  Online Form", "Online form bharne ka tarika batao.")
]

qcols = st.columns(4)

for i, (label, question) in enumerate(quick_questions):
    with qcols[i]:
        if st.button(label, key=f"quick_{i}", use_container_width=True):
            st.session_state.pending_prompt = question
            st.rerun()

# =====================================================
# AI HELPDESK
# =====================================================

st.markdown(
    '<div class="section-title">◈ AI HELPDESK</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-box">
    <b>🤖 NEURAL ASSISTANCE ACTIVE</b><br>
    Boss, apna sawaal type karein ya voice recording se poochhein.
    AI aapko simple aur step-by-step guidance dega.
</div>
""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="welcome">
        <div class="welcome-logo">AI</div>
        <h3>SYSTEM INITIALIZED</h3>
        <p>
            Namaste Boss! Main CSC Helpdesk AI hoon.
            Aadhaar, PAN Card, certificates aur online services
            ke liye aapki madad karne ke liye taiyar hoon.
        </p>
        <div style="color:#00e5ff;font-size:9px;letter-spacing:1px">
            ◈ AI ENGINE READY &nbsp; ◈ VOICE ENABLED
        </div>
    </div>
    """, unsafe_allow_html=True)

# Important: use emoji avatars, not "AI" as an image path.
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# =====================================================
# VOICE INPUT
# =====================================================

audio = st.audio_input(
    "🎙️ Record your question",
    key=f"audio_input_{st.session_state.audio_counter}"
)

prompt = st.session_state.pending_prompt
st.session_state.pending_prompt = None

if audio is not None:
    audio_bytes = audio.getvalue()
    current_hash = hashlib.sha256(audio_bytes).hexdigest()

    if current_hash != st.session_state.audio_hash:
        st.session_state.audio_hash = current_hash

        try:
            with st.spinner("◈ Processing voice input..."):
                transcription = client.models.generate_content(
                    model=model_name,
                    contents=[
                        "Transcribe this audio accurately. "
                        "The speaker may use Hindi, Hinglish or English. "
                        "Return only the transcribed words.",
                        genai.types.Part.from_bytes(
                            data=audio_bytes,
                            mime_type=audio.type or "audio/wav"
                        )
                    ]
                )

            transcript = (transcription.text or "").strip()

            if transcript:
                prompt = transcript
                st.session_state.audio_counter += 1
            else:
                st.warning("Voice samajh nahi aayi. Dobara record karein.")

        except Exception as e:
            st.error("Voice processing nahi ho payi.")
            st.caption(str(e))

# =====================================================
# AI RESPONSE
# =====================================================

if prompt is None:
    prompt = st.chat_input("Boss, apna command ya sawaal likhiye...")

def get_direct_answer(question):
    q = question.lower()
    now = india_now()

    date_terms = [
        "aaj ki date", "aaj ki tarikh", "aaj kya date",
        "today's date", "current date", "what date is today"
    ]

    time_terms = [
        "abhi kitne baje", "current time", "what time is it",
        "abhi ka time", "kitna baj raha", "time now"
    ]

    wants_date = any(term in q for term in date_terms)
    wants_time = any(term in q for term in time_terms)

    if wants_date or wants_time:
        date = now.strftime("%A, %d %B %Y")
        clock = now.strftime("%I:%M %p")

        if wants_date and wants_time:
            return f"Boss, aaj {date} hai aur abhi {clock} ho rahe hain."
        if wants_date:
            return f"Boss, aaj {date} hai."
        return f"Boss, abhi India mein {clock} ho rahe hain."

    return None

def generate_answer(question):
    history = []

    for item in st.session_state.messages[:-1]:
        history.append({
            "role": "user" if item["role"] == "user" else "model",
            "parts": [{"text": item["content"]}]
        })

    history.append({
        "role": "user",
        "parts": [{"text": question}]
    })

    return client.models.generate_content_stream(
        model=model_name,
        contents=history,
        config={
            "system_instruction": system_prompt(),
            "temperature": 0.5
        }
    )

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    answer = get_direct_answer(prompt)

    if answer:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(answer)
    else:
        with st.chat_message("assistant", avatar="🤖"):
            try:
                with st.spinner("◈ AI is thinking..."):
                    def stream_text():
                        for chunk in generate_answer(prompt):
                            if getattr(chunk, "text", None):
                                yield chunk.text

                    answer = st.write_stream(stream_text())

                if not answer or not str(answer).strip():
                    answer = "Boss, jawab nahi mil paya. Dobara poochhein."
                    st.markdown(answer)

            except Exception as e:
                answer = None
                st.error("AI response mein error aaya.")
                st.caption(str(e))

    if answer:
        st.session_state.messages.append({
            "role": "assistant",
            "content": str(answer)
        })

        if st.session_state.voice_enabled:
            speak_text(str(answer), st.session_state.voice_style)

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">
    <b>CSC HELPDESK AI</b><br>
    FUTURISTIC DIGITAL COMMAND CENTER<br>
    SMART ASSISTANCE • DIGITAL SERVICES • SECURE GUIDANCE
</div>
""", unsafe_allow_html=True)
