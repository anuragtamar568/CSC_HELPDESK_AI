
import os
import re
import json
import time
import hashlib
import hmac
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st
import streamlit.components.v1 as components
from google import genai

# ==========================================================
# CSC HELPDESK AI | ADVANCED ROBOTIC EDITION
# ==========================================================

st.set_page_config(
    page_title="CSC HELPDESK AI | Advanced",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# 1. CONFIGURATION
# ==========================================================

def get_setting(name, default=""):
    try:
        return st.secrets.get(name, os.environ.get(name, default))
    except Exception:
        return os.environ.get(name, default)

API_KEY = get_setting("GEMINI_API_KEY")
USERNAME = get_setting("APP_USERNAME", "admin")
PASSWORD = get_setting("APP_PASSWORD", "12345")
LOCK_PIN = get_setting("ROBOTIC_LOCK_PIN", "")

if not API_KEY:
    st.error("GEMINI_API_KEY configure nahi hai.")
    st.code(
        'GEMINI_API_KEY = "YOUR_API_KEY"\n'
        'APP_USERNAME = "admin"\n'
        'APP_PASSWORD = "CHANGE_YOUR_PASSWORD"\n'
        'ROBOTIC_LOCK_PIN = "1234"',
        language="toml"
    )
    st.stop()

# ==========================================================
# 2. SESSION STATE
# ==========================================================

DEFAULTS = {
    "authenticated": False,
    "messages": [],
    "pending_prompt": None,
    "voice_enabled": True,
    "voice_style": "BOSS DEEP",
    "voice_language": "Auto",
    "last_audio_hash": None,
    "audio_counter": 0,
    "request_count": 0
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================================================
# 3. LIVE INDIAN DATE AND TIME
# ==========================================================

def get_indian_time():
    return datetime.now(ZoneInfo("Asia/Kolkata"))

# ==========================================================
# 4. GEMINI CLIENT
# ==========================================================

@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)

client = get_client(API_KEY)

# ==========================================================
# 5. SERVICE CATALOG
# ==========================================================

SERVICE_CATALOG = {
    "Aadhaar Print": {
        "keywords": [
            "aadhaar print", "aadhar print",
            "aadhaar nikalna", "aadhar printout"
        ],
        "charge": 50,
        "official_fee": "Applicable official rules ke according",
        "documents": "Aadhaar number/card details",
        "time": "5-10 minute"
    },
    "PAN Card Apply": {
        "keywords": [
            "pan card", "pan apply",
            "new pan", "pan banana"
        ],
        "charge": 350,
        "official_fee": "Portal ke according",
        "documents": "Aadhaar aur required PAN documents",
        "time": "Application processing ke according"
    },
    "PAN Correction": {
        "keywords": [
            "pan correction", "pan me correction",
            "pan update"
        ],
        "charge": 350,
        "official_fee": "Portal ke according",
        "documents": "Required correction proof",
        "time": "Application processing ke according"
    },
    "Income Certificate": {
        "keywords": [
            "income certificate", "aay praman patra",
            "aay certificate"
        ],
        "charge": 500,
        "official_fee": "Portal/department ke according",
        "documents": "Required identity, address and income documents",
        "time": "Department processing ke according"
    },
    "Caste Certificate": {
        "keywords": [
            "caste certificate", "jati praman patra",
            "jati certificate"
        ],
        "charge": 500,
        "official_fee": "Portal/department ke according",
        "documents": "Required identity and caste-related documents",
        "time": "Department processing ke according"
    },
    "Residence Certificate": {
        "keywords": [
            "residence certificate", "niwas praman patra",
            "niwas certificate", "domicile"
        ],
        "charge": 500,
        "official_fee": "Portal/department ke according",
        "documents": "Required identity and address documents",
        "time": "Department processing ke according"
    },
    "Online Form Filling": {
        "keywords": [
            "online form", "form bharna",
            "online application", "form filling"
        ],
        "charge": 150,
        "official_fee": "Portal fee, if any, is separate",
        "documents": "Form ke according",
        "time": "10-30 minute"
    },
    "Print": {
        "keywords": [
            "print", "document print", "printout"
        ],
        "charge": 5,
        "official_fee": "N/A",
        "documents": "File/document",
        "time": "2-5 minute"
    },
    "Scan": {
        "keywords": [
            "scan", "document scan"
        ],
        "charge": 10,
        "official_fee": "N/A",
        "documents": "Original document",
        "time": "2-5 minute"
    }
}

def catalog_text():
    lines = []
    for name, data in SERVICE_CATALOG.items():
        lines.append(
            f"{name}: Centre charge ₹{data['charge']}; "
            f"Official fee: {data['official_fee']}; "
            f"Documents: {data['documents']}; "
            f"Time: {data['time']}; "
            f"Keywords: {', '.join(data['keywords'])}"
        )
    return "\n".join(lines)

# ==========================================================
# 6. SYSTEM PROMPT
# ==========================================================

def make_system_prompt():
    now = get_indian_time()

    return f"""
You are CSC HELPDESK AI, an advanced digital service assistant
for a private CSC / Jan Seva / Digital Service Centre.

You help customers understand services, documents, centre charges
and general government service procedures.

IDENTITY:
- You are CSC HELPDESK AI.
- Address the customer politely.
- When suitable, you may call the customer Boss.
- Never claim to be a government official.
- Never promise that a government application will be approved.

LIVE DATE AND TIME:
- Current date: {now.strftime("%d %B %Y")}
- Current day: {now.strftime("%A")}
- Current time: {now.strftime("%I:%M %p")}
- Timezone: Asia/Kolkata (IST)
- Use this date and time for current-date questions.
- Never present 2024 as the current year.

LANGUAGE:
- Hindi question: Reply in simple Hindi.
- Hinglish question: Reply in natural Hinglish.
- English question: Reply in English.
- Keep explanations easy to understand.

SERVICE CHARGES:
Use ONLY the centre charges in the service catalog below.
Never invent or change a configured centre charge.
If a service is not listed, say its centre charge is not configured.
Government fees and centre service charges are different.
Never invent government fees, deadlines, eligibility or rules.

SERVICE CATALOG:
{catalog_text()}

SERVICE RESPONSE FORMAT:
For service and price questions, provide:
1. Service name
2. Centre service charge
3. Official fee, if verified/configured
4. Required documents
5. Approximate time, if configured
6. Important note about department approval

GOVERNMENT SAFETY:
- Government approval depends on the concerned department.
- Advise customers to verify rules on the official portal.
- Never ask customers to share OTP, password, UPI PIN,
  ATM PIN, CVV or other confidential credentials.
- Do not claim to submit applications unless a real submission
  integration is available.
- For uncertain or changing information, clearly say it needs
  verification from the official source.

RESPONSE STYLE:
- Give direct answers.
- Use short paragraphs, bullet points and numbered steps.
- Avoid repeating the same information.
- Do not generate fake application status or reference numbers.
"""

# ==========================================================
# 7. ADVANCED ROBOTIC THEME
# ==========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@400;500;600;700&display=swap');

:root {
    --cyan: #00eaff;
    --blue: #168bff;
    --dark: #030914;
    --panel: #071727;
    --text: #d9fbff;
    --border: rgba(0,234,255,.34);
}

.stApp {
    background:
        radial-gradient(ellipse at 50% -15%,
            rgba(0,150,220,.18), transparent 55%),
        linear-gradient(145deg,#020711,#071727 50%,#020711);
    color: var(--text);
    font-family: 'Rajdhani', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: transparent;
}

[data-testid="stHeader"],
[data-testid="stToolbar"] {
    background: transparent !important;
}

.block-container {
    max-width: 1300px !important;
    padding-top: 24px !important;
    padding-bottom: 70px !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#041323,#020711) !important;
    border-right: 1px solid var(--border);
    box-shadow: 5px 0 30px rgba(0,234,255,.08);
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #9ffaff !important;
}

.robot-title {
    text-align: center;
    font-family: 'Orbitron',sans-serif;
    font-size: clamp(34px,5vw,65px);
    font-weight: 900;
    letter-spacing: .12em;
    color: #dffcff;
    text-shadow:
        0 0 8px #00eaff,
        0 0 22px #00eaff,
        0 0 48px rgba(0,130,255,.8);
    animation: titlePulse 3s ease-in-out infinite;
}

@keyframes titlePulse {
    0%,100% {
        text-shadow: 0 0 8px #00eaff,0 0 22px #00eaff;
    }
    50% {
        text-shadow: 0 0 15px #00eaff,0 0 38px #00aaff;
    }
}

.robot-sub {
    text-align: center;
    color: #6cefff;
    font-family: 'Orbitron',sans-serif;
    font-size: 10px;
    letter-spacing: .16em;
    text-shadow: 0 0 9px #00eaff;
    margin: 5px 0 22px;
}

.status-bar {
    text-align: center;
    color: #9ffaff;
    background: rgba(0,234,255,.04);
    border: 1px solid var(--border);
    border-radius: 9px;
    padding: 12px;
    font-family: 'Orbitron',sans-serif;
    font-size: 10px;
    letter-spacing: .08em;
    box-shadow: 0 0 20px rgba(0,234,255,.09);
    margin-bottom: 20px;
}

.status-dot {
    color: #36ff9b;
    text-shadow: 0 0 12px #36ff9b;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 30px;
    border-radius: 18px;
    border: 1px solid rgba(0,234,255,.42);
    background:
        radial-gradient(circle at 90% 10%,
            rgba(0,234,255,.12), transparent 30%),
        linear-gradient(135deg,rgba(5,28,48,.97),rgba(2,10,22,.96));
    box-shadow:
        0 0 28px rgba(0,234,255,.08),
        inset 0 0 25px rgba(0,234,255,.025);
    margin: 20px 0 28px;
}

.hero-label {
    color: #00eaff;
    font-family: 'Orbitron',sans-serif;
    font-size: 10px;
    letter-spacing: .15em;
    text-shadow: 0 0 9px #00eaff;
    margin-bottom: 12px;
}

.hero-title {
    color: #e6fdff;
    font-family: 'Orbitron',sans-serif;
    font-size: clamp(25px,3.5vw,43px);
    font-weight: 800;
    line-height: 1.25;
    text-shadow: 0 0 10px rgba(0,234,255,.7);
}

.hero-title span {
    color: #00eaff;
    text-shadow: 0 0 13px #00eaff;
}

.hero-description {
    color: #a4d8e1;
    font-size: 16px;
    line-height: 1.65;
    margin-top: 12px;
}

.section-heading {
    color: #bffaff;
    font-family: 'Orbitron',sans-serif;
    font-size: 14px;
    letter-spacing: .08em;
    margin: 27px 0 14px;
    text-shadow: 0 0 9px rgba(0,234,255,.75);
}

.service-card {
    height: 112px;
    border: 1px solid rgba(0,234,255,.22);
    background: linear-gradient(145deg,#0a1b2d,#06111e);
    border-radius: 13px;
    text-align: center;
    padding: 16px 4px;
    box-shadow: 0 0 12px rgba(0,234,255,.04);
    transition: all .2s ease;
}

.service-card:hover {
    border-color: #00eaff;
    box-shadow: 0 0 20px rgba(0,234,255,.2);
    transform: translateY(-3px);
}

.service-icon {
    color: #00eaff;
    font-family: 'Orbitron',sans-serif;
    font-size: 24px;
    font-weight: 800;
    text-shadow: 0 0 12px #00eaff;
    margin-bottom: 9px;
}

.service-name {
    color: #c6faff;
    font-size: 12px;
    font-weight: 700;
}

.welcome-card {
    padding: 25px;
    border: 1px solid rgba(0,234,255,.4);
    border-radius: 15px;
    text-align: center;
    background: linear-gradient(135deg,#071e33,#030c19);
    box-shadow: 0 0 25px rgba(0,234,255,.08);
    margin: 22px 0;
}

.welcome-card h3 {
    color: #00eaff;
    font-family: 'Orbitron',sans-serif;
    text-shadow: 0 0 12px #00eaff;
}

.welcome-card p {
    color: #d9fbff;
    font-size: 17px;
    line-height: 1.7;
    text-shadow: 0 0 6px rgba(0,234,255,.4);
}

[data-testid="stChatMessage"] {
    background: rgba(5,20,36,.93) !important;
    border: 1px solid rgba(0,234,255,.25) !important;
    border-radius: 13px !important;
    padding: 13px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 4px 18px rgba(0,0,0,.2);
    transition: border-color .2s ease;
}

[data-testid="stChatMessage"]:hover {
    border-color: rgba(0,234,255,.6) !important;
    box-shadow: 0 0 18px rgba(0,234,255,.1);
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #d9fbff !important;
    font-family: 'Rajdhani',sans-serif !important;
    font-size: 17px !important;
    line-height: 1.65 !important;
    text-shadow: 0 0 5px rgba(0,234,255,.38);
}

[data-testid="stChatMessage"] strong {
    color: #ffffff !important;
    text-shadow: 0 0 8px #00eaff;
}

[data-testid="stChatInput"] > div {
    background: #041323 !important;
    border: 1px solid #00eaff !important;
    border-radius: 12px !important;
    box-shadow: 0 0 13px rgba(0,234,255,.22);
}

[data-testid="stChatInput"] textarea {
    color: #e1fcff !important;
    -webkit-text-fill-color: #e1fcff !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #6c9ba7 !important;
}

.stButton > button,
.stDownloadButton > button {
    min-height: 39px;
    border: 1px solid rgba(0,234,255,.55) !important;
    border-radius: 8px !important;
    background: linear-gradient(100deg,#07516f,#087d98) !important;
    color: #e7fdff !important;
    font-family: 'Orbitron',sans-serif !important;
    font-size: 10px !important;
    letter-spacing: .04em;
    box-shadow: 0 0 10px rgba(0,234,255,.12);
    transition: all .2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #00eaff !important;
    box-shadow: 0 0 19px rgba(0,234,255,.35);
    transform: translateY(-2px);
}

.stTextInput input,
.stTextArea textarea,
div[data-baseweb="select"] > div {
    background: #071727 !important;
    color: #d9fbff !important;
    border-color: rgba(0,234,255,.3) !important;
}

.voice-panel {
    padding: 12px 15px;
    border: 1px solid rgba(0,234,255,.32);
    border-radius: 10px;
    background: rgba(0,234,255,.04);
    color: #a9faff;
    font-size: 14px;
    text-shadow: 0 0 7px rgba(0,234,255,.45);
    margin: 14px 0;
}

.metric-card {
    background: #071727;
    border: 1px solid rgba(0,234,255,.24);
    border-radius: 11px;
    padding: 14px;
    text-align: center;
}

.metric-number {
    color: #00eaff;
    font-family: 'Orbitron',sans-serif;
    font-size: 22px;
    text-shadow: 0 0 12px #00eaff;
}

.metric-label {
    color: #91cbd6;
    font-size: 11px;
}

.footer {
    text-align: center;
    color: #65838e;
    font-size: 11px;
    border-top: 1px solid rgba(0,234,255,.15);
    padding: 20px 0;
    margin-top: 35px;
}

@media(max-width:700px) {
    .block-container {
        padding: 12px !important;
    }
    .hero {
        padding: 21px;
    }
    .robot-title {
        letter-spacing: .06em;
    }
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# 8. BOSS VOICE ENGINE
# ==========================================================

def speak_text(text, style="BOSS DEEP", language="Auto"):
    safe_text = json.dumps(str(text), ensure_ascii=False)
    safe_style = json.dumps(style)
    safe_language = json.dumps(language)

    html = """
    <script>
    (() => {
        const text = __TEXT__;
        const style = __STYLE__;
        const language = __LANG__;

        if (!window.speechSynthesis || !text) return;

        const synth = window.speechSynthesis;
        synth.cancel();

        function start() {
            const voices = synth.getVoices();
            const u = new SpeechSynthesisUtterance(text);

            const isHindi = /[\\u0900-\\u097F]/.test(text);
            const target = language === "Hindi" || (language === "Auto" && isHindi)
                ? "hi"
                : "en";

            let filtered = voices.filter(v => v.lang.toLowerCase().startsWith(target));

            const maleNames = /david|mark|daniel|alex|james|george|hemant|madhur|male|guy|ryan/i;
            const femaleNames = /zira|samantha|female|aria|susan|heera/i;

            let chosen = filtered.find(v => maleNames.test(v.name))
                || filtered.find(v => !femaleNames.test(v.name))
                || filtered[0]
                || voices.find(v => maleNames.test(v.name))
                || voices[0];

            if (chosen) u.voice = chosen;

            if (style === "BOSS DEEP") {
                u.rate = 0.82;
                u.pitch = 0.55;
            } else if (style === "ULTRA ROBOTIC") {
                u.rate = 0.76;
                u.pitch = 0.40;
            } else {
                u.rate = 0.91;
                u.pitch = 0.68;
            }

            u.volume = 1;
            synth.speak(u);
        }

        if (synth.getVoices().length) {
            start();
        } else {
            synth.onvoiceschanged = () => {
                synth.onvoiceschanged = null;
                start();
            };
        }
    })();
    </script>
    """

    html = html.replace("__TEXT__", safe_text)
    html = html.replace("__STYLE__", safe_style)
    html = html.replace("__LANG__", safe_language)
    components.html(html, height=0)

# ==========================================================
# 9. LOGIN
# ==========================================================

if not st.session_state.authenticated:
    st.markdown(
        '<div class="robot-title">CSC AI</div>'
        '<div class="robot-sub">SECURE ACCESS TERMINAL</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="welcome-card">
        <h3>🔐 SYSTEM LOCKED</h3>
        <p>CSC HELPDESK AI • AUTHORIZED ACCESS ONLY</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        login_user = st.text_input(
            "USERNAME",
            placeholder="Enter username"
        )
        login_pass = st.text_input(
            "PASSWORD",
            type="password",
            placeholder="Enter password"
        )
        submitted = st.form_submit_button(
            "🔓 ACCESS SYSTEM",
            use_container_width=True
        )

    if submitted:
        if (
            hmac.compare_digest(login_user, USERNAME)
            and hmac.compare_digest(login_pass, PASSWORD)
        ):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("ACCESS DENIED — Incorrect login details.")

    st.stop()

# ==========================================================
# 10. SIDEBAR CONTROL PANEL
# ==========================================================

with st.sidebar:
    st.markdown("## 🤖 CSC HELPDESK AI")
    st.caption("ADVANCED ROBOTIC CONTROL PANEL")
    st.success("● SYSTEM ONLINE")

    now = get_indian_time()
    st.markdown("### 📡 SYSTEM READOUT")
    st.caption("INDIA DATE")
    st.write(now.strftime("%d %B %Y"))
    st.caption("INDIA TIME")
    st.write(now.strftime("%I:%M:%S %p"))

    st.divider()

    model_name = st.selectbox(
        "⚙️ AI ENGINE",
        ["gemini-2.5-flash", "gemini-2.0-flash"],
        index=0
    )

    st.session_state.voice_enabled = st.toggle(
        "🔊 AI VOICE REPLY",
        value=st.session_state.voice_enabled
    )

    voice_style = st.selectbox(
        "🎙️ VOICE PROFILE",
        ["BOSS DEEP", "ULTRA ROBOTIC", "COMMANDER"],
        index=0
    )
    st.session_state.voice_style = voice_style

    voice_language = st.selectbox(
        "VOICE LANGUAGE",
        ["Auto", "Hindi", "English"],
        index=0
    )
    st.session_state.voice_language = voice_language

    if st.button("🔊 TEST BOSS VOICE", use_container_width=True):
        speak_text(
            "Greetings Boss. CSC Helpdesk AI is online. "
            "All systems are ready. How may I assist you?",
            voice_style,
            voice_language
        )

    st.divider()

    st.markdown("### 🛡️ SECURITY")

    if st.button("🔒 LOGOUT", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.messages = []
        st.rerun()

    if st.button("🧹 NEW CHAT", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.session_state.last_audio_hash = None
        st.rerun()

    st.divider()
    st.markdown("### 📚 SERVICES")

    for name, data in SERVICE_CATALOG.items():
        st.caption(f"• {name} — ₹{data['charge']}")

    st.divider()

    st.download_button(
        "⬇️ DOWNLOAD CHAT LOG",
        data="\n\n".join(
            f"{m['role'].upper()}:\n{m['content']}"
            for m in st.session_state.messages
        ),
        file_name="CSC_Helpdesk_Chat.txt",
        mime="text/plain",
        use_container_width=True,
        disabled=not bool(st.session_state.messages)
    )

# ==========================================================
# 11. HEADER
# ==========================================================

now = get_indian_time()

st.markdown(
    '<div class="robot-title">CSC HELPDESK AI</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="robot-sub">'
    'ADVANCED DIGITAL SERVICE INTELLIGENCE'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="status-bar">'
    '<span class="status-dot">●</span> SYSTEM ONLINE '
    '&nbsp; | &nbsp; NEURAL CORE ACTIVE '
    '&nbsp; | &nbsp; SECURE ACCESS '
    '&nbsp; | &nbsp; INDIA IST'
    '</div>',
    unsafe_allow_html=True
)

# ==========================================================
# 12. HERO
# ==========================================================

st.markdown("""
<div class="hero">
    <div class="hero-label">SMART DIGITAL SERVICE CENTRE</div>
    <div class="hero-title">
        Aapka kaam,<br><span>hamari madad.</span>
    </div>
    <div class="hero-description">
        CSC, Aadhaar, PAN Card, certificates aur online services ke
        baare mein poochhiye. VEER-style robotic intelligence ke saath
        apne sawalon ke simple aur step-by-step jawab paaiye.
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# 13. DASHBOARD METRICS
# ==========================================================

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-number">{len(SERVICE_CATALOG)}</div>'
        f'<div class="metric-label">CONFIGURED SERVICES</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with m2:
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-number">{len(st.session_state.messages)}</div>'
        f'<div class="metric-label">CHAT MESSAGES</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with m3:
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-number">ONLINE</div>'
        f'<div class="metric-label">AI CORE STATUS</div>'
        f'</div>',
        unsafe_allow_html=True
    )

# ==========================================================
# 14. SERVICE CARDS
# ==========================================================

st.markdown(
    '<div class="section-heading">▣ DIGITAL SERVICE MODULES</div>',
    unsafe_allow_html=True
)

services = [
    ("A", "Aadhaar"),
    ("P", "PAN Card"),
    ("R", "Ration Card"),
    ("K", "PM Kisan"),
    ("H", "Ayushman"),
    ("C", "Certificates"),
    ("P", "Pension"),
    ("E", "e-District")
]

service_cols = st.columns(4)

for i, (symbol, name) in enumerate(services):
    with service_cols[i % 4]:
        st.markdown(
            f"""
            <div class="service-card">
                <div class="service-icon">{symbol}</div>
                <div class="service-name">{name}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==========================================================
# 15. QUICK QUESTIONS
# ==========================================================

st.markdown(
    '<div class="section-heading">⚡ QUICK QUESTIONS</div>',
    unsafe_allow_html=True
)

quick_questions = [
    "Aadhaar print ka charge kitna hai?",
    "PAN card banwane ke liye kya documents lagenge?",
    "Income certificate ka charge aur documents batao.",
    "Online form bharne ka charge kitna hai?"
]

qcols = st.columns(4)

for i, question in enumerate(quick_questions):
    with qcols[i]:
        if st.button(
            ["🪪 Aadhaar Print", "💳 PAN Card",
             "📄 Certificate", "🌐 Online Form"][i],
            use_container_width=True,
            key=f"quick_{i}"
        ):
            st.session_state.pending_prompt = question
            st.rerun()

# ==========================================================
# 16. CHAT HISTORY
# ==========================================================

st.markdown(
    '<div class="section-heading">◈ NEURAL CONVERSATION</div>',
    unsafe_allow_html=True
)

for message in st.session_state.messages:
    avatar = "👑" if message["role"] == "user" else "🤖"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ==========================================================
# 17. VOICE INPUT
# ==========================================================

st.markdown(
    '<div class="voice-panel">'
    '🎙️ <b>VOICE INPUT MODULE</b> — '
    'Mic se Hindi, English ya Hinglish mein apna sawaal boliye.'
    '</div>',
    unsafe_allow_html=True
)

audio = st.audio_input(
    "🎙️ Record your question",
    key=f"audio_{st.session_state.audio_counter}"
)

active_prompt = st.session_state.pending_prompt
st.session_state.pending_prompt = None

# Process each new recording once
if audio is not None:
    audio_bytes = audio.getvalue()
    audio_hash = hashlib.sha256(audio_bytes).hexdigest()

    if audio_hash != st.session_state.last_audio_hash:
        st.session_state.last_audio_hash = audio_hash

        with st.spinner("🎙️ Voice processing..."):
            try:
                audio_result = client.models.generate_content(
                    model=model_name,
                    contents=[
                        "Understand the spoken audio. Return ONLY the "
                        "transcription of the user's request. "
                        "The audio may be Hindi, Hinglish or English.",
                        genai.types.Part.from_bytes(
                            data=audio_bytes,
                            mime_type=audio.type or "audio/wav"
                        )
                    ]
                )

                spoken_text = (audio_result.text or "").strip()

                if spoken_text:
                    active_prompt = spoken_text
                    st.session_state.audio_counter += 1
                else:
                    st.warning("Voice samajh nahi aayi. Dobara record karein.")

            except Exception as exc:
                st.error(f"Voice input error: {exc}")

# ==========================================================
# 18. CHAT INPUT
# ==========================================================

if active_prompt is None:
    active_prompt = st.chat_input(
        "Boss, apna sawaal likhiye..."
    )

# ==========================================================
# 19. AI RESPONSE ENGINE
# ==========================================================

def get_live_date_answer(prompt):
    now = get_indian_time()
    date_question = bool(re.search(
        r"(aaj ki date|aaj kya date|today'?s date|current date|"
        r"aaj ki tarikh|aaj ka din|what day is today)",
        prompt.lower()
    ))
    time_question = bool(re.search(
        r"(abhi kitne baje|current time|what time is it|"
        r"abhi ka time|kitna baj raha|time now)",
        prompt.lower()
    ))

    if date_question or time_question:
        date = now.strftime("%A, %d %B %Y")
        clock = now.strftime("%I:%M %p")

        if date_question and time_question:
            return f"Boss, aaj {date} hai aur abhi India mein {clock} ho rahe hain."
        if date_question:
            return f"Boss, aaj {date} hai."
        return f"Boss, abhi India mein {clock} ho rahe hain."

    return None


def create_history(messages):
    history = []

    for item in messages:
        role = "user" if item["role"] == "user" else "model"
        history.append({
            "role": role,
            "parts": [{"text": item["content"]}]
        })

    return history


def stream_gemini(prompt, model_name):
    history = create_history(st.session_state.messages[:-1])
    history.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })

    config = {
        "system_instruction": make_system_prompt(),
        "temperature": 0.5
    }

    response_stream = client.models.generate_content_stream(
        model=model_name,
        contents=history,
        config=config
    )

    for chunk in response_stream:
        if getattr(chunk, "text", None):
            yield chunk.text


if active_prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": active_prompt
    })

    with st.chat_message("user", avatar="👑"):
        st.markdown(active_prompt)

    live_answer = get_live_date_answer(active_prompt)

    if live_answer:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(live_answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": live_answer
        })

        if st.session_state.voice_enabled:
            speak_text(
                live_answer,
                st.session_state.voice_style,
                st.session_state.voice_language
            )

    else:
        with st.chat_message("assistant", avatar="🤖"):
            try:
                answer = st.write_stream(
                    stream_gemini(active_prompt, model_name)
                )

                if not answer or not answer.strip():
                    answer = (
                        "Boss, mujhe is baar clear response nahi mila. "
                        "Kripya apna sawaal dobara poochhein."
                    )
                    st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                if st.session_state.voice_enabled:
                    speak_text(
                        answer,
                        st.session_state.voice_style,
                        st.session_state.voice_language
                    )

            except Exception as exc:
                st.error(
                    "AI Core error. API key, model name, internet "
                    "connection aur API quota check karein."
                )
                st.caption(str(exc))

# ==========================================================
# 20. FOOTER
# ==========================================================

st.markdown("""
<div class="footer">
    CSC HELPDESK AI • ADVANCED ROBOTIC EDITION
    <br><br>
    SMART DIGITAL SERVICES • SECURE • RESPONSIVE • AI POWERED
</div>
""", unsafe_allow_html=True)
