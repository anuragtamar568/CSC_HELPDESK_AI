
import os
import json
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st
import streamlit.components.v1 as components
from google import genai

# ==================================================
# CSC HELPDESK AI | PREMIUM DIGITAL SEVA
# ==================================================

st.set_page_config(
    page_title="CSC Helpdesk AI",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded"
)

def setting(key, default=""):
    try:
        return st.secrets.get(key, os.environ.get(key, default))
    except Exception:
        return os.environ.get(key, default)

API_KEY = setting("GEMINI_API_KEY")
APP_USERNAME = setting("APP_USERNAME", "admin")
APP_PASSWORD = setting("APP_PASSWORD", "12345")

if not API_KEY:
    st.error("GEMINI_API_KEY configure karein.")
    st.stop()

@st.cache_resource
def get_client(key):
    return genai.Client(api_key=key)

client = get_client(API_KEY)

# ---------------- SESSION ----------------

for key, default in {
    "authenticated": False,
    "messages": [],
    "voice_enabled": True,
    "voice_style": "BOSS DEEP",
    "pending_prompt": None,
    "audio_hash": None,
    "audio_counter": 0
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

def current_time():
    return datetime.now(ZoneInfo("Asia/Kolkata"))

# ---------------- SERVICES ----------------

SERVICES = [
    ("AD", "Aadhaar Services", 50,
     "Aadhaar print, update aur related services"),
    ("PN", "PAN Card", 350,
     "New PAN aur PAN correction"),
    ("RC", "Ration Card", 100,
     "Ration card aur e-KYC guidance"),
    ("PK", "PM Kisan", 100,
     "Registration aur e-KYC guidance"),
    ("AY", "Ayushman Card", 100,
     "Ayushman card guidance"),
    ("IC", "Income Certificate", 500,
     "Income certificate application guidance"),
    ("CC", "Caste Certificate", 500,
     "Caste certificate application guidance"),
    ("RF", "Residence Certificate", 500,
     "Residence certificate application guidance"),
    ("OF", "Online Forms", 150,
     "Online application form assistance"),
    ("PR", "Printout", 5,
     "Document printing"),
    ("SC", "Document Scan", 10,
     "Document scanning")
]

service_text = "\n".join(
    f"{name}: Centre service charge ₹{charge}. {description}"
    for _, name, charge, description in SERVICES
)

# ---------------- AI PROMPT ----------------

def get_system_prompt():
    now = current_time()
    return f"""
You are CSC HELPDESK AI, a professional digital service assistant.

Current date: {now.strftime("%d %B %Y")}
Current time: {now.strftime("%I:%M %p")} IST.

Your purpose is to help people with CSC and Indian government services.

SERVICES:
{service_text}

Topics:
Aadhaar, PAN Card, Ration Card, PM Kisan, Ayushman Card,
Income Certificate, Caste Certificate, Residence Certificate,
Birth Certificate, Pension, e-District, Government Forms,
CSC services and general digital guidance.

LANGUAGE:
- Reply in Hindi to Hindi messages.
- Reply in natural Hinglish to Hinglish messages.
- Reply in English to English messages.
- Keep explanations simple and practical.

RULES:
- Never invent government fees, rules, eligibility or deadlines.
- Centre service charges are not government fees.
- Explain when information needs official verification.
- Never ask for an OTP, password, UPI PIN or CVV.
- Never claim an application is submitted or approved
  unless a real integration confirms it.
- Explain processes step by step.
- Be polite, clear and professional.
- Address the customer as Boss only when appropriate.
"""

# ==================================================
# PREMIUM THEME
# ==================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #172b45;
    --navy2: #203c5d;
    --teal: #07877e;
    --teal-light: #e7f6f3;
    --saffron: #eea52e;
    --canvas: #f3f5f8;
    --white: #ffffff;
    --text: #243449;
    --muted: #748297;
    --line: #e1e7ed;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp,
[data-testid="stAppViewContainer"] {
    background: var(--canvas) !important;
    color: var(--text) !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    background: transparent !important;
}

.block-container {
    max-width: 1440px !important;
    padding-top: 1rem !important;
    padding-bottom: 3rem !important;
}

[data-testid="stSidebar"] {
    background: #fff !important;
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] > div {
    padding-top: 1.1rem;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: var(--text);
}

/* BRAND */

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 7px 0 19px;
    border-bottom: 1px solid var(--line);
    margin-bottom: 20px;
}

.brand-symbol {
    width: 49px;
    height: 49px;
    flex-shrink: 0;
    border-radius: 13px;
    background: var(--navy);
    display: flex;
    justify-content: center;
    align-items: center;
    color: #fff;
    font-family: 'Manrope', sans-serif;
    font-size: 19px;
    font-weight: 800;
    border-bottom: 4px solid var(--saffron);
}

.brand-title {
    color: var(--navy);
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    font-size: 15px;
    line-height: 1.4;
}

.brand-subtitle {
    font-size: 9px;
    color: var(--muted);
    letter-spacing: 1.1px;
    margin-top: 3px;
}

/* TOP NAV */

.top-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    padding: 12px 18px;
    background: white;
    border: 1px solid var(--line);
    border-radius: 12px;
    margin-bottom: 18px;
}

.nav-label {
    font-size: 12px;
    font-weight: 700;
    color: var(--navy);
}

.nav-status {
    background: #eaf7ef;
    color: #18834c;
    padding: 7px 12px;
    border-radius: 30px;
    font-size: 10px;
    font-weight: 700;
}

/* HERO */

.hero {
    background: var(--navy);
    border-radius: 17px;
    padding: 31px 34px;
    color: white;
    position: relative;
    overflow: hidden;
    margin-bottom: 20px;
    box-shadow: 0 8px 22px rgba(23,43,69,.09);
}

.hero:before {
    content: "";
    position: absolute;
    right: -55px;
    top: -95px;
    width: 290px;
    height: 290px;
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 50%;
}

.hero:after {
    content: "";
    position: absolute;
    right: 20px;
    bottom: -155px;
    width: 280px;
    height: 280px;
    border: 40px solid rgba(255,255,255,.035);
    border-radius: 50%;
}

.hero-label {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 5px;
    background: rgba(255,255,255,.09);
    border: 1px solid rgba(255,255,255,.14);
    color: #dce9f7;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.2px;
}

.hero h1 {
    color: #fff;
    font-family: 'Manrope', sans-serif;
    font-size: clamp(27px, 3.3vw, 40px);
    font-weight: 800;
    margin: 15px 0 9px;
    line-height: 1.2;
}

.hero p {
    color: #d5e0ec;
    font-size: 13px;
    line-height: 1.8;
    max-width: 650px;
    margin: 0;
}

.hero-line {
    height: 4px;
    width: 48px;
    border-radius: 8px;
    background: var(--saffron);
    margin-top: 17px;
}

/* SECTION TITLES */

.section-heading {
    color: var(--navy);
    font-family: 'Manrope', sans-serif;
    font-size: 17px;
    font-weight: 800;
    margin: 24px 0 12px;
}

.section-description {
    color: var(--muted);
    font-size: 12px;
    margin-top: -7px;
    margin-bottom: 15px;
}

/* STATS */

.stat-card {
    min-height: 100px;
    padding: 16px 17px;
    background: white;
    border: 1px solid var(--line);
    border-radius: 12px;
    box-shadow: 0 3px 12px rgba(23,43,69,.025);
}

.stat-top {
    color: var(--muted);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .5px;
}

.stat-number {
    color: var(--navy);
    font-family: 'Manrope', sans-serif;
    font-size: 26px;
    font-weight: 800;
    margin-top: 8px;
}

/* SERVICE CARDS */

.service-card {
    background: #fff;
    border: 1px solid var(--line);
    border-radius: 12px;
    min-height: 119px;
    padding: 14px 8px;
    text-align: center;
    transition: .2s ease;
    box-shadow: 0 3px 12px rgba(23,43,69,.025);
}

.service-card:hover {
    border-color: #82bcb3;
    transform: translateY(-2px);
    box-shadow: 0 7px 18px rgba(23,43,69,.07);
}

.service-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 39px;
    height: 39px;
    margin: 0 auto 9px;
    background: var(--teal-light);
    color: var(--teal);
    border-radius: 10px;
    font-size: 12px;
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    border-bottom: 2px solid #b7e5dc;
}

.service-name {
    color: var(--text);
    font-size: 11px;
    font-weight: 700;
    line-height: 1.4;
}

/* WELCOME */

.welcome {
    background: #fff;
    border: 1px solid var(--line);
    border-radius: 13px;
    padding: 22px;
    text-align: center;
    margin: 18px 0;
}

.welcome-logo {
    width: 53px;
    height: 53px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 10px;
    background: var(--navy);
    border-bottom: 4px solid var(--saffron);
    border-radius: 14px;
    color: white;
    font-size: 19px;
    font-weight: 800;
}

.welcome h3 {
    color: var(--navy);
    font-family: 'Manrope', sans-serif;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 8px;
}

.welcome p {
    color: var(--muted);
    font-size: 12px;
    line-height: 1.8;
}

/* CHAT */

[data-testid="stChatMessage"] {
    background: #fff !important;
    border: 1px solid var(--line) !important;
    border-radius: 12px !important;
    padding: 14px 17px !important;
    box-shadow: 0 3px 12px rgba(23,43,69,.025);
    margin-bottom: 12px;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #26364b !important;
    font-size: 13px !important;
    line-height: 1.75 !important;
}

[data-testid="stChatMessage"] strong {
    color: var(--navy) !important;
}

/* BOTTOM CHAT AREA */

[data-testid="stBottom"],
[data-testid="stBottom"] > div {
    background: var(--canvas) !important;
}

[data-testid="stChatInput"] {
    background: transparent !important;
}

[data-testid="stChatInput"] > div {
    background: white !important;
    border: 1px solid #cbd7e3 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 15px rgba(23,43,69,.055) !important;
}

[data-testid="stChatInput"] textarea {
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    font-size: 13px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #93a0b0 !important;
}

/* BUTTONS */

.stButton > button,
.stDownloadButton > button {
    background: white !important;
    color: var(--navy) !important;
    border: 1px solid #d5dfe9 !important;
    border-radius: 8px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    min-height: 37px;
    transition: .2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: var(--teal-light) !important;
    color: var(--teal) !important;
    border-color: #8bc8bd !important;
}

/* INPUTS */

div[data-baseweb="select"] > div,
.stTextInput input,
.stTextArea textarea {
    background: white !important;
    color: var(--text) !important;
    border-color: #d5dfe9 !important;
    border-radius: 8px !important;
}

.stTextInput label,
.stSelectbox label {
    color: #475569 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}

/* INFO */

.info-box {
    background: #eaf6f3;
    border-left: 4px solid var(--teal);
    padding: 12px 14px;
    border-radius: 7px;
    color: #28564f;
    font-size: 12px;
    line-height: 1.7;
    margin: 12px 0;
}

.footer {
    margin-top: 35px;
    padding: 18px 0;
    border-top: 1px solid var(--line);
    text-align: center;
    font-size: 10px;
    color: #8390a1;
}

@media(max-width: 700px) {
    .block-container {
        padding-left: 12px !important;
        padding-right: 12px !important;
    }
    .hero {
        padding: 23px 20px;
    }
    .hero:before, .hero:after {
        opacity: .4;
    }
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# VOICE REPLY
# ==================================================

def speak_text(text, style="BOSS DEEP"):
    safe_text = json.dumps(str(text), ensure_ascii=False)
    safe_style = json.dumps(style)

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
            const hindi = /[\\u0900-\\u097F]/.test(text);
            const lang = hindi ? "hi" : "en";

            const matching = voices.filter(v =>
                v.lang.toLowerCase().startsWith(lang)
            );

            const female = /zira|samantha|aria|susan|heera/i;
            const male = /david|mark|daniel|alex|james|george|hemant|madhur|guy|ryan/i;

            const voice = matching.find(v => male.test(v.name))
                || matching.find(v => !female.test(v.name))
                || matching[0]
                || voices[0];

            const u = new SpeechSynthesisUtterance(text);
            if (voice) u.voice = voice;

            if (style === "BOSS DEEP") {
                u.rate = 0.82;
                u.pitch = 0.55;
            } else if (style === "ULTRA ROBOTIC") {
                u.rate = 0.76;
                u.pitch = 0.4;
            } else {
                u.rate = 0.91;
                u.pitch = 0.68;
            }

            u.volume = 1;
            synth.speak(u);
        }

        if (synth.getVoices().length) speak();
        else synth.onvoiceschanged = speak;
    })();
    </script>
    """
    html = html.replace("__TEXT__", safe_text)
    html = html.replace("__STYLE__", safe_style)
    components.html(html, height=0)

# ==================================================
# LOGIN
# ==================================================

if not st.session_state.authenticated:
    st.markdown("""
    <div class="welcome" style="max-width:520px;margin:50px auto 20px">
        <div class="welcome-logo">CSC</div>
        <h3>CSC HELPDESK AI</h3>
        <p>Digital Seva Assistant<br>Secure Dashboard Login</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button(
            "Login to Dashboard",
            use_container_width=True
        )

    if submit:
        import hmac
        if (
            hmac.compare_digest(username, APP_USERNAME)
            and hmac.compare_digest(password, APP_PASSWORD)
        ):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Username ya password galat hai.")

    st.stop()

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-symbol">CSC</div>
        <div>
            <div class="brand-title">CSC HELPDESK AI</div>
            <div class="brand-subtitle">DIGITAL SEVA ASSISTANT</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.success("System Online")

    now = current_time()
    st.caption("INDIA STANDARD TIME")
    st.write(now.strftime("%d %B %Y"))
    st.write(now.strftime("%I:%M:%S %p"))

    st.divider()
    st.markdown("#### AI Configuration")

    model_name = st.selectbox(
        "AI Model",
        ["gemini-2.5-flash", "gemini-2.0-flash"]
    )

    st.session_state.voice_enabled = st.toggle(
        "Voice Reply",
        value=st.session_state.voice_enabled
    )

    st.session_state.voice_style = st.selectbox(
        "Voice Profile",
        ["BOSS DEEP", "ULTRA ROBOTIC", "COMMANDER"]
    )

    if st.button("Test Voice", use_container_width=True):
        speak_text(
            "Namaste Boss. CSC Helpdesk AI taiyar hai.",
            st.session_state.voice_style
        )

    st.divider()
    st.markdown("#### Centre Services")

    for _, name, charge, _ in SERVICES:
        st.caption(f"{name}  |  ₹{charge}")

    st.divider()

    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.session_state.audio_hash = None
        st.rerun()

    chat_export = "\n\n".join(
        f"{m['role'].upper()}:\n{m['content']}"
        for m in st.session_state.messages
    )

    st.download_button(
        "Download Chat",
        data=chat_export,
        file_name="CSC_Helpdesk_Chat.txt",
        mime="text/plain",
        use_container_width=True,
        disabled=not bool(chat_export)
    )

    if st.button("Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.messages = []
        st.rerun()

# ==================================================
# DASHBOARD
# ==================================================

now = current_time()

st.markdown("""
<div class="top-nav">
    <div class="nav-label">CSC &nbsp; / &nbsp; Digital Seva Dashboard</div>
    <div class="nav-status">● SYSTEM ONLINE</div>
</div>

<div class="hero">
    <div class="hero-label">DIGITAL INDIA • SMART ASSISTANCE</div>
    <h1>CSC Helpdesk AI</h1>
    <p>
        Your Digital Seva Assistant. Get simple guidance for
        Aadhaar, PAN Card, certificates, government schemes
        and online services, all in one place.
    </p>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# ---------------- STATS ----------------

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-top">AVAILABLE SERVICES</div>
        <div class="stat-number">{len(SERVICES)}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-top">CHAT MESSAGES</div>
        <div class="stat-number">{len(st.session_state.messages)}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-top">TODAY'S DATE</div>
        <div class="stat-number" style="font-size:18px">
            {now.strftime("%d-%m-%Y")}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- SERVICES ----------------

st.markdown(
    '<div class="section-heading">Our Digital Services</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Explore the services available at your digital service centre.'
    '</div>',
    unsafe_allow_html=True
)

for start in range(0, len(SERVICES), 4):
    cols = st.columns(4)
    for i, (symbol, name, charge, description) in enumerate(
        SERVICES[start:start+4]
    ):
        with cols[i]:
            st.markdown(f"""
            <div class="service-card">
                <div class="service-icon">{symbol}</div>
                <div class="service-name">{name}</div>
                <div style="font-size:10px;color:#7c8998;margin-top:6px">
                    From ₹{charge}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ---------------- QUICK QUESTIONS ----------------

st.markdown(
    '<div class="section-heading">Quick Questions</div>',
    unsafe_allow_html=True
)

quick_questions = [
    ("Aadhaar Print", "Aadhaar print ka charge kitna hai?"),
    ("PAN Card", "PAN card ke liye documents aur charge batao."),
    ("Certificate", "Income certificate kaise banega?"),
    ("Online Form", "Online form bharne ki process batao.")
]

quick_cols = st.columns(4)

for i, (label, question) in enumerate(quick_questions):
    with quick_cols[i]:
        if st.button(label, key=f"quick_{i}", use_container_width=True):
            st.session_state.pending_prompt = question
            st.rerun()

# ---------------- CHAT ----------------

st.markdown(
    '<div class="section-heading">AI Helpdesk</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-box">
    <b>CSC AI Assistant</b><br>
    Apna sawaal type karein ya voice recording se poochhein.
    Assistant aapko step-by-step jankari dega.
</div>
""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="welcome">
        <div class="welcome-logo">AI</div>
        <h3>Welcome to CSC Helpdesk</h3>
        <p>
            Namaste! Aadhaar, PAN Card, certificates,
            government schemes aur digital services ke baare mein
            apna sawaal poochhein.
        </p>
    </div>
    """, unsafe_allow_html=True)

for message in st.session_state.messages:
    avatar = "U" if message["role"] == "user" else "AI"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ---------------- VOICE INPUT ----------------

audio = st.audio_input(
    "Record your question",
    key=f"audio_{st.session_state.audio_counter}"
)

prompt = st.session_state.pending_prompt
st.session_state.pending_prompt = None

if audio is not None:
    import hashlib
    audio_data = audio.getvalue()
    audio_hash = hashlib.sha256(audio_data).hexdigest()

    if audio_hash != st.session_state.audio_hash:
        st.session_state.audio_hash = audio_hash

        try:
            with st.spinner("Processing your voice..."):
                result = client.models.generate_content(
                    model=model_name,
                    contents=[
                        "Transcribe the spoken audio accurately. "
                        "Return only the spoken words. The language "
                        "may be Hindi, Hinglish or English.",
                        genai.types.Part.from_bytes(
                            data=audio_data,
                            mime_type=audio.type or "audio/wav"
                        )
                    ]
                )

            transcript = (result.text or "").strip()
            if transcript:
                prompt = transcript
                st.session_state.audio_counter += 1
            else:
                st.warning("Voice samajh nahi aayi. Dobara try karein.")

        except Exception as e:
            st.error(f"Voice processing error: {e}")

# ---------------- GENERATE RESPONSE ----------------

if prompt is None:
    prompt = st.chat_input("Apna sawaal likhiye...")

def direct_date_answer(question):
    q = question.lower()
    now = current_time()

    date_keys = [
        "aaj ki date", "aaj ki tarikh", "aaj kya date",
        "today's date", "current date", "what date is today"
    ]
    time_keys = [
        "abhi kitne baje", "current time", "what time is it",
        "abhi ka time", "kitna baj raha", "time now"
    ]

    is_date = any(x in q for x in date_keys)
    is_time = any(x in q for x in time_keys)

    if is_date or is_time:
        date = now.strftime("%A, %d %B %Y")
        clock = now.strftime("%I:%M %p")
        if is_date and is_time:
            return f"Boss, aaj {date} hai aur abhi {clock} ho rahe hain."
        if is_date:
            return f"Boss, aaj {date} hai."
        return f"Boss, abhi India mein {clock} ho rahe hain."

    return None

def get_history():
    history = []
    for m in st.session_state.messages[:-1]:
        history.append({
            "role": "user" if m["role"] == "user" else "model",
            "parts": [{"text": m["content"]}]
        })
    return history

def get_response(question):
    contents = get_history()
    contents.append({
        "role": "user",
        "parts": [{"text": question}]
    })

    return client.models.generate_content_stream(
        model=model_name,
        contents=contents,
        config={
            "system_instruction": get_system_prompt(),
            "temperature": 0.5
        }
    )

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user", avatar="U"):
        st.markdown(prompt)

    answer = direct_date_answer(prompt)

    if answer:
        with st.chat_message("assistant", avatar="AI"):
            st.markdown(answer)

    else:
        with st.chat_message("assistant", avatar="AI"):
            try:
                def response_stream():
                    for chunk in get_response(prompt):
                        if getattr(chunk, "text", None):
                            yield chunk.text

                answer = st.write_stream(response_stream())

                if not answer or not str(answer).strip():
                    answer = "Maaf kijiye, jawab nahi mila. Dobara poochhein."
                    st.markdown(answer)

            except Exception as e:
                answer = None
                st.error(
                    "AI response nahi aa paya. API key, internet, "
                    "model availability aur quota check karein."
                )
                st.caption(str(e))

    if answer:
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        if st.session_state.voice_enabled:
            speak_text(answer, st.session_state.voice_style)

# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    CSC HELPDESK AI &nbsp; • &nbsp; DIGITAL SEVA ASSISTANT
    <br><br>
    Smart Assistance | Digital Services | Secure Guidance
</div>
""", unsafe_allow_html=True)
