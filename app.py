
import os
import re
import json
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st
import streamlit.components.v1 as components
from google import genai

# =====================================================
# CSC HELPDESK AI - DIGITAL SEVA PROFESSIONAL EDITION
# =====================================================

st.set_page_config(
    page_title="CSC Helpdesk AI | Digital Seva",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CONFIGURATION ----------------

def get_setting(name, default=""):
    try:
        return st.secrets.get(name, os.environ.get(name, default))
    except Exception:
        return os.environ.get(name, default)

API_KEY = get_setting("GEMINI_API_KEY")
APP_USERNAME = get_setting("APP_USERNAME", "admin")
APP_PASSWORD = get_setting("APP_PASSWORD", "12345")

if not API_KEY:
    st.error("GEMINI_API_KEY configure karein.")
    st.stop()

@st.cache_resource
def get_client(key):
    return genai.Client(api_key=key)

client = get_client(API_KEY)

# ---------------- SESSION ----------------

defaults = {
    "authenticated": False,
    "messages": [],
    "pending_prompt": None,
    "voice_enabled": True,
    "voice_style": "BOSS DEEP",
    "voice_language": "Auto",
    "audio_hash": None,
    "audio_counter": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def india_now():
    return datetime.now(ZoneInfo("Asia/Kolkata"))

# ---------------- SERVICES ----------------

SERVICES = {
    "Aadhaar Print": {
        "charge": 50,
        "keywords": ["aadhaar print", "aadhar print", "aadhaar nikalna"],
        "documents": "Aadhaar details"
    },
    "PAN Card": {
        "charge": 350,
        "keywords": ["pan card", "pan banana", "new pan"],
        "documents": "Aadhaar aur zaroori PAN documents"
    },
    "PAN Correction": {
        "charge": 350,
        "keywords": ["pan correction", "pan update"],
        "documents": "Correction ke liye valid proof"
    },
    "Income Certificate": {
        "charge": 500,
        "keywords": ["income certificate", "aay praman patra"],
        "documents": "Identity, address aur income documents"
    },
    "Caste Certificate": {
        "charge": 500,
        "keywords": ["caste certificate", "jati praman patra"],
        "documents": "Identity aur caste-related documents"
    },
    "Residence Certificate": {
        "charge": 500,
        "keywords": ["residence certificate", "niwas praman patra"],
        "documents": "Identity aur address documents"
    },
    "Online Form": {
        "charge": 150,
        "keywords": ["online form", "form bharna", "form filling"],
        "documents": "Form ke anusaar"
    },
    "Printout": {
        "charge": 5,
        "keywords": ["printout", "document print"],
        "documents": "Print karne wali file"
    },
    "Document Scan": {
        "charge": 10,
        "keywords": ["document scan", "scan"],
        "documents": "Original document"
    }
}

service_info = "\n".join(
    f"{name}: Centre charge ₹{data['charge']}, "
    f"Documents: {data['documents']}"
    for name, data in SERVICES.items()
)

# ---------------- SYSTEM PROMPT ----------------

def system_prompt():
    now = india_now()

    return f"""
You are CSC HELPDESK AI, a professional digital service
assistant for CSC and Jan Seva services in India.

Current Indian date: {now.strftime("%d %B %Y")}
Current day: {now.strftime("%A")}
Current time: {now.strftime("%I:%M %p")} IST.

LANGUAGE:
- Hindi input: simple Hindi response.
- Hinglish input: natural Hinglish response.
- English input: English response.

YOUR SERVICES:
Aadhaar, PAN Card, Ration Card, PM Kisan,
Ayushman Card, Income Certificate, Caste Certificate,
Residence Certificate, Birth Certificate, Pension,
e-District, Government Forms and CSC services.

CENTRE SERVICE CHARGES:
{service_info}

Rules:
- Use only the configured centre charges above.
- Centre service charge and government fee are different.
- Do not invent government fees, eligibility, rules or deadlines.
- Clearly explain when official verification is needed.
- Never ask for OTP, password, UPI PIN or CVV.
- Never claim that an application was submitted or approved
  unless a real integration confirms it.
- Give easy, practical, step-by-step answers.
- Be polite, concise and professional.
- You may address the customer as Boss when appropriate.
"""

# =====================================================
# PROFESSIONAL CSC DIGITAL SEVA THEME
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');

:root {
    --blue: #1456a0;
    --dark-blue: #103c72;
    --light-blue: #eaf3ff;
    --saffron: #f59e0b;
    --green: #159957;
    --text: #1e293b;
    --muted: #64748b;
    --border: #dce5f0;
    --surface: #ffffff;
}

.stApp {
    background: #f4f7fb;
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: #f4f7fb;
}

[data-testid="stHeader"] {
    background: rgba(244,247,251,.96);
}

.block-container {
    max-width: 1320px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 4rem !important;
}

[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #334155;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0 20px;
    border-bottom: 1px solid #e5edf6;
    margin-bottom: 20px;
}

.brand-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 13px;
    background: linear-gradient(140deg,#1456a0,#2389d9);
    color: white;
    font-size: 25px;
    box-shadow: 0 5px 15px rgba(20,86,160,.2);
}

.brand-name {
    font-family: 'Poppins',sans-serif;
    font-size: 17px;
    font-weight: 800;
    color: #123f78;
    line-height: 1.35;
}

.brand-sub {
    color: #64748b;
    font-size: 10px;
    letter-spacing: .06em;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #ffffff;
    padding: 13px 20px;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 3px 12px rgba(15,45,80,.035);
}

.topbar-title {
    font-size: 13px;
    font-weight: 700;
    color: #24476f;
}

.online {
    color: #12834c;
    background: #e8f8ef;
    border: 1px solid #c9efd8;
    padding: 7px 12px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 700;
}

.hero {
    position: relative;
    overflow: hidden;
    border-radius: 18px;
    padding: 34px;
    color: white;
    background: linear-gradient(115deg,#103c72,#1765b4 70%,#2888d1);
    box-shadow: 0 12px 28px rgba(20,86,160,.14);
    margin-bottom: 23px;
}

.hero:after {
    content: "🏛️";
    position: absolute;
    right: 7%;
    top: 50%;
    transform: translateY(-50%);
    font-size: 105px;
    opacity: .12;
}

.hero-tag {
    display: inline-block;
    padding: 6px 11px;
    border: 1px solid rgba(255,255,255,.3);
    border-radius: 30px;
    background: rgba(255,255,255,.1);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .09em;
    margin-bottom: 13px;
}

.hero h1 {
    color: white;
    font-family: 'Poppins',sans-serif;
    font-size: clamp(27px,4vw,42px);
    line-height: 1.25;
    font-weight: 800;
    margin: 0;
}

.hero p {
    color: #e6f1ff;
    font-size: 15px;
    line-height: 1.7;
    max-width: 680px;
    margin-top: 12px;
    margin-bottom: 0;
}

.hero-accent {
    width: 58px;
    height: 4px;
    background: #ffbd4a;
    border-radius: 5px;
    margin-top: 18px;
}

.section-title {
    font-family: 'Poppins',sans-serif;
    font-size: 17px;
    font-weight: 700;
    color: #173e6b;
    margin: 25px 0 14px;
}

.stat-card {
    background: white;
    border: 1px solid #e2eaf4;
    border-radius: 13px;
    padding: 17px;
    min-height: 100px;
    box-shadow: 0 4px 15px rgba(20,50,90,.035);
}

.stat-label {
    color: #64748b;
    font-size: 12px;
    font-weight: 600;
}

.stat-value {
    font-family: 'Poppins',sans-serif;
    color: #1456a0;
    font-size: 24px;
    font-weight: 800;
    margin-top: 7px;
}

.service-card {
    background: white;
    border: 1px solid #e0e8f2;
    border-radius: 13px;
    padding: 17px 10px;
    text-align: center;
    min-height: 117px;
    box-shadow: 0 4px 12px rgba(15,45,80,.035);
    transition: .2s ease;
}

.service-card:hover {
    border-color: #8db9ed;
    box-shadow: 0 7px 20px rgba(20,86,160,.1);
    transform: translateY(-2px);
}

.service-icon {
    margin: 0 auto 9px;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 43px;
    height: 43px;
    border-radius: 12px;
    background: #eaf3ff;
    color: #1456a0;
    font-size: 22px;
}

.service-name {
    color: #263e5a;
    font-size: 12px;
    font-weight: 700;
}

.info-card {
    background: #fff;
    border: 1px solid #e0e8f2;
    border-left: 4px solid #159957;
    border-radius: 10px;
    padding: 15px;
    color: #334155;
    font-size: 13px;
    line-height: 1.6;
    margin: 14px 0;
}

.welcome {
    background: white;
    border: 1px solid #e2eaf4;
    border-radius: 14px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 5px 18px rgba(15,45,80,.035);
    margin: 20px 0;
}

.welcome h3 {
    font-family: 'Poppins',sans-serif;
    color: #1456a0;
    font-size: 19px;
    font-weight: 700;
}

.welcome p {
    color: #64748b;
    font-size: 14px;
    line-height: 1.7;
}

[data-testid="stChatMessage"] {
    background: white !important;
    border: 1px solid #e1e9f2 !important;
    border-radius: 13px !important;
    padding: 13px 16px !important;
    box-shadow: 0 4px 14px rgba(15,45,80,.035);
    margin-bottom: 12px;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #26364b !important;
    font-family: 'Inter',sans-serif !important;
    font-size: 14px !important;
    line-height: 1.75 !important;
}

[data-testid="stChatMessage"] strong {
    color: #124c91 !important;
}

[data-testid="stChatInput"] > div {
    background: white !important;
    border: 1px solid #cbd9e9 !important;
    border-radius: 12px !important;
    box-shadow: 0 5px 18px rgba(15,45,80,.06);
}

[data-testid="stChatInput"] textarea {
    color: #1e293b !important;
    -webkit-text-fill-color: #1e293b !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #94a3b8 !important;
}

.stButton > button,
.stDownloadButton > button {
    background: #ffffff !important;
    color: #1456a0 !important;
    border: 1px solid #cbd9e9 !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    transition: .2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #eaf3ff !important;
    color: #103c72 !important;
    border-color: #8db9ed !important;
}

div[data-baseweb="select"] > div,
.stTextInput input {
    background: #ffffff !important;
    color: #1e293b !important;
    border-color: #cbd9e9 !important;
}

.voice-card {
    background: #eaf3ff;
    border: 1px solid #cbdff7;
    border-radius: 10px;
    padding: 12px 15px;
    color: #245b96;
    font-size: 13px;
    margin: 12px 0;
}

.footer {
    text-align: center;
    color: #8291a5;
    font-size: 11px;
    border-top: 1px solid #e1e9f2;
    padding: 20px 0;
    margin-top: 35px;
}

@media(max-width:700px) {
    .block-container {
        padding-left: 12px !important;
        padding-right: 12px !important;
    }
    .hero {
        padding: 23px;
    }
    .hero:after {
        right: 1%;
        font-size: 70px;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------- VOICE ENGINE ----------------

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

        function speak() {
            const voices = synth.getVoices();
            const utterance = new SpeechSynthesisUtterance(text);
            const hindi = /[\\u0900-\\u097F]/.test(text);
            const lang = language === "Hindi" ||
                (language === "Auto" && hindi) ? "hi" : "en";

            const matching = voices.filter(v =>
                v.lang.toLowerCase().startsWith(lang)
            );
            const male = /david|mark|daniel|alex|james|george|hemant|madhur|guy|ryan/i;
            const female = /zira|samantha|aria|susan|heera/i;

            const voice = matching.find(v => male.test(v.name))
                || matching.find(v => !female.test(v.name))
                || matching[0]
                || voices[0];

            if (voice) utterance.voice = voice;

            if (style === "BOSS DEEP") {
                utterance.rate = 0.82;
                utterance.pitch = 0.55;
            } else if (style === "ULTRA ROBOTIC") {
                utterance.rate = 0.76;
                utterance.pitch = 0.4;
            } else {
                utterance.rate = 0.91;
                utterance.pitch = 0.68;
            }

            utterance.volume = 1;
            synth.speak(utterance);
        }

        if (synth.getVoices().length) speak();
        else synth.onvoiceschanged = speak;
    })();
    </script>
    """

    html = html.replace("__TEXT__", safe_text)
    html = html.replace("__STYLE__", safe_style)
    html = html.replace("__LANG__", safe_language)
    components.html(html, height=0)

# =====================================================
# LOGIN PAGE
# =====================================================

if not st.session_state.authenticated:
    st.markdown("""
    <div class="welcome">
        <div style="font-size:55px">🏛️</div>
        <h3>CSC HELPDESK AI</h3>
        <p>Digital Seva • Smart Assistance • Secure Access</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )
        login = st.form_submit_button(
            "🔐 Login to Dashboard",
            use_container_width=True
        )

    if login:
        import hmac
        if (
            hmac.compare_digest(username, APP_USERNAME)
            and hmac.compare_digest(password, APP_PASSWORD)
        ):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect username or password.")

    st.stop()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🏛️</div>
        <div>
            <div class="brand-name">CSC HELPDESK AI</div>
            <div class="brand-sub">DIGITAL SEVA ASSISTANT</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.success("● AI Assistant Online")

    now = india_now()
    st.caption("INDIAN STANDARD TIME")
    st.write(now.strftime("%d %B %Y"))
    st.write(now.strftime("%I:%M:%S %p"))

    st.divider()
    st.markdown("### ⚙️ AI Settings")

    model_name = st.selectbox(
        "AI Model",
        ["gemini-2.5-flash", "gemini-2.0-flash"]
    )

    st.session_state.voice_enabled = st.toggle(
        "🔊 Voice Reply",
        value=st.session_state.voice_enabled
    )

    st.session_state.voice_style = st.selectbox(
        "Voice Profile",
        ["BOSS DEEP", "ULTRA ROBOTIC", "COMMANDER"]
    )

    st.session_state.voice_language = st.selectbox(
        "Voice Language",
        ["Auto", "Hindi", "English"]
    )

    if st.button("🔊 Test Voice", use_container_width=True):
        speak_text(
            "Namaste Boss. CSC Helpdesk AI aapki madad ke liye taiyar hai.",
            st.session_state.voice_style,
            st.session_state.voice_language
        )

    st.divider()
    st.markdown("### 🛠️ Centre Services")

    for name, data in SERVICES.items():
        st.caption(f"{name} — ₹{data['charge']}")

    st.divider()

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.session_state.audio_hash = None
        st.rerun()

    chat_text = "\n\n".join(
        f"{m['role'].upper()}:\n{m['content']}"
        for m in st.session_state.messages
    )

    st.download_button(
        "⬇️ Download Chat",
        data=chat_text,
        file_name="CSC_Helpdesk_Chat.txt",
        mime="text/plain",
        use_container_width=True,
        disabled=not bool(chat_text)
    )

    if st.button("🔒 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.messages = []
        st.rerun()

# =====================================================
# MAIN DASHBOARD
# =====================================================

now = india_now()

st.markdown(f"""
<div class="topbar">
    <div class="topbar-title">
        🏠 &nbsp; Digital Seva / AI Dashboard
    </div>
    <div class="online">● SYSTEM ONLINE</div>
</div>

<div class="hero">
    <div class="hero-tag">WELCOME TO DIGITAL SEVA</div>
    <h1>CSC Helpdesk AI</h1>
    <p>
        Aapka digital assistant. Aadhaar, PAN Card, certificates,
        government schemes aur online services ki jankari
        ab ek hi jagah par.
    </p>
    <div class="hero-accent"></div>
</div>
""", unsafe_allow_html=True)

# ---------------- METRICS ----------------

a, b, c = st.columns(3)

with a:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">AVAILABLE SERVICES</div>
        <div class="stat-value">{len(SERVICES)}</div>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">CHAT MESSAGES</div>
        <div class="stat-value">{len(st.session_state.messages)}</div>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">CURRENT DATE</div>
        <div class="stat-value" style="font-size:17px">
            {now.strftime("%d-%m-%Y")}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- SERVICE GRID ----------------

st.markdown(
    '<div class="section-title">📋 Our Digital Services</div>',
    unsafe_allow_html=True
)

service_cards = [
    ("🪪", "Aadhaar Services"),
    ("💳", "PAN Card"),
    ("🍚", "Ration Card"),
    ("🌾", "PM Kisan"),
    ("🏥", "Ayushman Card"),
    ("📄", "Certificates"),
    ("👴", "Pension"),
    ("🌐", "Online Forms")
]

cols = st.columns(4)

for i, (emoji, name) in enumerate(service_cards):
    with cols[i % 4]:
        st.markdown(f"""
        <div class="service-card">
            <div class="service-icon">{emoji}</div>
            <div class="service-name">{name}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------- QUICK QUESTIONS ----------------

st.markdown(
    '<div class="section-title">⚡ Quick Questions</div>',
    unsafe_allow_html=True
)

questions = [
    ("🪪 Aadhaar Print", "Aadhaar print ka charge kitna hai?"),
    ("💳 PAN Card", "PAN card banwane ke liye documents aur charge batao."),
    ("📄 Certificate", "Income certificate kaise banega aur kya documents lagenge?"),
    ("🌐 Online Form", "Online form bharne ka charge kitna hai?")
]

qcols = st.columns(4)

for i, (label, question) in enumerate(questions):
    with qcols[i]:
        if st.button(label, key=f"quick_{i}", use_container_width=True):
            st.session_state.pending_prompt = question
            st.rerun()

# ---------------- CHAT ----------------

st.markdown(
    '<div class="section-title">💬 Chat with CSC AI</div>',
    unsafe_allow_html=True
)

if not st.session_state.messages:
    st.markdown("""
    <div class="welcome">
        <div style="font-size:38px">🤖</div>
        <h3>Namaste! Main CSC Helpdesk AI hoon.</h3>
        <p>
            Aap mujhse Aadhaar, PAN Card, certificates,
            government schemes aur online services ke baare
            mein kuch bhi pooch sakte hain.
        </p>
    </div>
    """, unsafe_allow_html=True)

for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ---------------- VOICE INPUT ----------------

st.markdown("""
<div class="voice-card">
    🎙️ <b>Voice Assistant</b><br>
    Mic se Hindi, Hinglish ya English mein apna sawaal record karein.
</div>
""", unsafe_allow_html=True)

audio = st.audio_input(
    "🎙️ Record your question",
    key=f"audio_{st.session_state.audio_counter}"
)

prompt = st.session_state.pending_prompt
st.session_state.pending_prompt = None

if audio is not None:
    import hashlib
    audio_bytes = audio.getvalue()
    current_hash = hashlib.sha256(audio_bytes).hexdigest()

    if current_hash != st.session_state.audio_hash:
        st.session_state.audio_hash = current_hash

        try:
            with st.spinner("Voice processing..."):
                audio_result = client.models.generate_content(
                    model=model_name,
                    contents=[
                        "Transcribe the user's audio accurately. "
                        "Return only the spoken words. It may be Hindi, "
                        "Hinglish or English.",
                        genai.types.Part.from_bytes(
                            data=audio_bytes,
                            mime_type=audio.type or "audio/wav"
                        )
                    ]
                )

            transcript = (audio_result.text or "").strip()

            if transcript:
                prompt = transcript
                st.session_state.audio_counter += 1
            else:
                st.warning("Audio samajh nahi aayi. Dobara try karein.")

        except Exception as e:
            st.error(f"Voice error: {e}")

# ---------------- CHAT INPUT ----------------

if prompt is None:
    prompt = st.chat_input("Apna sawaal likhiye...")

# ---------------- RESPONSE ----------------

def current_date_response(text):
    now = india_now()
    t = text.lower()

    date_words = [
        "aaj ki date", "aaj kya date", "aaj ki tarikh",
        "today's date", "current date", "what date is today",
        "aaj ka din"
    ]
    time_words = [
        "abhi kitne baje", "current time", "what time is it",
        "abhi ka time", "kitna baj raha", "time now"
    ]

    is_date = any(x in t for x in date_words)
    is_time = any(x in t for x in time_words)

    if is_date or is_time:
        date = now.strftime("%A, %d %B %Y")
        clock = now.strftime("%I:%M %p")

        if is_date and is_time:
            return f"Boss, aaj {date} hai aur abhi India mein {clock} ho rahe hain."
        if is_date:
            return f"Boss, aaj {date} hai."
        return f"Boss, abhi India mein {clock} ho rahe hain."

    return None

def chat_history():
    history = []
    for item in st.session_state.messages[:-1]:
        history.append({
            "role": "user" if item["role"] == "user" else "model",
            "parts": [{"text": item["content"]}]
        })
    return history

def generate_stream(question):
    history = chat_history()
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

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    direct_answer = current_date_response(prompt)

    if direct_answer:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(direct_answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": direct_answer
        })

        if st.session_state.voice_enabled:
            speak_text(
                direct_answer,
                st.session_state.voice_style,
                st.session_state.voice_language
            )
    else:
        with st.chat_message("assistant", avatar="🤖"):
            try:
                def text_chunks():
                    for chunk in generate_stream(prompt):
                        if getattr(chunk, "text", None):
                            yield chunk.text

                answer = st.write_stream(text_chunks())

                if not answer or not str(answer).strip():
                    answer = "Maaf kijiye, mujhe jawab nahi mila. Dobara poochhein."
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

            except Exception as e:
                st.error(
                    "AI response nahi aa paya. Internet, API key, "
                    "model availability aur API quota check karein."
                )
                st.caption(str(e))

# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    🏛️ CSC HELPDESK AI &nbsp; | &nbsp; DIGITAL SEVA ASSISTANT
    <br><br>
    Smart Assistance • Simple Service • Digital India
</div>
""", unsafe_allow_html=True)
