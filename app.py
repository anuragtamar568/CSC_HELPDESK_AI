import os
import time
import streamlit as st
from google import genai

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="CSC_HELPDESK_AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS / DESIGN
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 5% 5%, rgba(40,130,255,0.20), transparent 28%),
        radial-gradient(circle at 95% 10%, rgba(150,70,255,0.20), transparent 30%),
        linear-gradient(135deg, #f4f8ff 0%, #edf2ff 48%, #faf3ff 100%);
}

/* Main width */
.block-container {
    max-width: 1250px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

/* =====================================================
   HEADER
   ===================================================== */

.hero {
    position: relative;
    text-align: center;
    padding: 30px 20px 25px 20px;
    border-radius: 30px;
    background:
        radial-gradient(circle at 50% 0%, rgba(80,170,255,0.20), transparent 35%),
        linear-gradient(135deg, rgba(255,255,255,0.96), rgba(241,239,255,0.96));
    border: 1px solid rgba(90,110,255,0.20);
    box-shadow:
        0 18px 50px rgba(55,75,180,0.15),
        inset 0 0 40px rgba(110,100,255,0.04);
    overflow: hidden;
}

.hero-logo {
    width: 105px;
    height: 105px;
    margin: auto;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    font-size: 58px;
    background:
        radial-gradient(circle, #ffffff 20%, #dce9ff 55%, #b8aaff 100%);
    border: 5px solid #6d65ff;
    box-shadow:
        0 0 12px #25cfff,
        0 0 28px #6d65ff,
        0 0 55px rgba(100,80,255,0.35);
}

.hero-title {
    margin-top: 14px;
    font-size: 46px;
    font-weight: 900;
    letter-spacing: 1px;
    background: linear-gradient(90deg, #1769ff, #6048ff, #a13cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 18px;
    color: #303c63;
    margin-top: 4px;
}

.online {
    display: inline-block;
    margin-top: 13px;
    padding: 8px 18px;
    border-radius: 30px;
    background: #e9fff1;
    color: #118647;
    border: 1px solid #8de0ad;
    font-weight: 700;
    font-size: 14px;
}

.tagline {
    margin-top: 12px;
    color: #536080;
    font-size: 14px;
}

/* =====================================================
   SECTION
   ===================================================== */

.section-title {
    font-size: 22px;
    font-weight: 800;
    color: #1d2c55;
    margin-top: 25px;
    margin-bottom: 12px;
}

/* =====================================================
   SERVICE CARDS
   ===================================================== */

.service-card {
    text-align: center;
    min-height: 115px;
    padding: 17px 8px;
    border-radius: 20px;
    background: rgba(255,255,255,0.90);
    border: 1px solid rgba(90,110,255,0.16);
    box-shadow: 0 7px 22px rgba(65,75,160,0.08);
    transition: 0.25s;
}

.service-card:hover {
    transform: translateY(-4px);
    box-shadow:
        0 12px 28px rgba(65,75,180,0.16),
        0 0 18px rgba(90,100,255,0.12);
}

.service-icon {
    font-size: 35px;
}

.service-name {
    margin-top: 7px;
    color: #24345e;
    font-size: 14px;
    font-weight: 700;
}

/* =====================================================
   CHAT AREA
   ===================================================== */

.chat-box {
    margin-top: 22px;
    padding: 22px;
    border-radius: 25px;
    background: rgba(255,255,255,0.76);
    border: 1px solid rgba(90,105,255,0.17);
    box-shadow: 0 12px 35px rgba(60,70,150,0.09);
}

/* =====================================================
   POPULAR QUESTIONS
   ===================================================== */

.popular-box {
    padding: 18px;
    border-radius: 22px;
    background: linear-gradient(
        135deg,
        rgba(235,242,255,0.95),
        rgba(248,241,255,0.95)
    );
    border: 1px solid rgba(90,110,255,0.15);
}

.popular-title {
    color: #243a78;
    font-size: 18px;
    font-weight: 800;
}

/* =====================================================
   BUTTONS
   ===================================================== */

.stButton > button {
    width: 100%;
    min-height: 45px;
    border-radius: 15px !important;
    border: 1px solid rgba(75,100,255,0.22) !important;
    background: rgba(255,255,255,0.94) !important;
    color: #25458d !important;
    font-weight: 650 !important;
    box-shadow: 0 5px 15px rgba(65,80,170,0.07);
    transition: 0.2s;
}

.stButton > button:hover {
    border-color: #6558ff !important;
    color: #4c43d8 !important;
    box-shadow:
        0 7px 20px rgba(90,75,220,0.15),
        0 0 12px rgba(90,80,255,0.10);
}

/* New chat button */
.new-chat button {
    background: linear-gradient(135deg, #624bff, #9546ff) !important;
    color: white !important;
}

/* =====================================================
   CHAT INPUT
   ===================================================== */

[data-testid="stChatInput"] {
    margin-top: 15px;
}

[data-testid="stChatInput"] textarea {
    border: 2px solid #7164ff !important;
    border-radius: 20px !important;
    background: white !important;
    color: #17254a !important;
    font-size: 16px !important;
    box-shadow:
        0 0 15px rgba(100,90,255,0.10);
}

[data-testid="stChatInput"] textarea:focus {
    border-color: #4d8cff !important;
    box-shadow:
        0 0 20px rgba(80,100,255,0.20) !important;
}

/* =====================================================
   CHAT MESSAGES
   ===================================================== */

[data-testid="stChatMessage"] {
    border-radius: 20px;
    margin-bottom: 10px;
}

/* =====================================================
   FOOTER
   ===================================================== */

.footer {
    margin-top: 35px;
    padding: 22px;
    text-align: center;
    color: #58627c;
    font-size: 13px;
}

.footer-main {
    font-weight: 800;
    color: #263c72;
    font-size: 15px;
}

.footer-line {
    margin-top: 7px;
}

/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 700px) {

    .hero-title {
        font-size: 30px;
    }

    .hero-subtitle {
        font-size: 14px;
    }

    .hero-logo {
        width: 85px;
        height: 85px;
        font-size: 46px;
    }

    .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# GEMINI API
# =========================================================

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY is not configured.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are CSC_HELPDESK_AI, a helpful digital assistant for CSC
and Indian government service guidance.

You help users with:

Aadhaar
PAN Card
Ration Card
PM Kisan
Ayushman Card
Income Certificate
Caste Certificate
Residence Certificate
Birth Certificate
Pension
e-District
Government forms
CSC services
General digital service guidance

Rules:

1. Reply in Hindi when the user writes Hindi.
2. Reply in Hinglish when the user writes Hinglish.
3. Reply in English when the user writes English.
4. Keep answers simple and easy to understand.
5. Give step-by-step instructions when useful.
6. Do not invent government rules, fees, websites or deadlines.
7. If information may have changed, tell the user to verify it
   on the official government portal.
8. Never ask for OTP, PIN, password or sensitive credentials.
9. Be polite and helpful.
10. Give a direct answer first.
"""

# =========================================================
# CHAT MEMORY
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# HERO HEADER
# =========================================================

st.markdown("""
<div class="hero">

    <div class="hero-logo">
        🤖
    </div>

    <div class="hero-title">
        CSC_HELPDESK_AI
    </div>

    <div class="hero-subtitle">
        Smart Assistant for CSC & Government Services
    </div>

    <div class="online">
        🟢 AI Assistant Online
    </div>

    <div class="tagline">
        Aapka Sawal &nbsp; | &nbsp; Hamari Madad &nbsp; | &nbsp; Digital Bharat
    </div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# SERVICES
# =========================================================

st.markdown(
    '<div class="section-title">🛠️ CSC Services</div>',
    unsafe_allow_html=True
)

services = [
    ("🪪", "Aadhaar"),
    ("💳", "PAN Card"),
    ("🛒", "Ration Card"),
    ("🌱", "PM Kisan"),
    ("🏥", "Ayushman"),
    ("📜", "Certificates"),
    ("👨‍👩‍👧", "Pension"),
    ("🖥️", "e-District"),
    ("🏛️", "CSC Services"),
    ("•••", "More Services")
]

service_columns = st.columns(10)

for column, (icon, name) in zip(service_columns, services):

    with column:
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
# NEW CHAT + HISTORY
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([6, 1.5, 1.5])

with col2:

    if st.button("🔄 New Chat", use_container_width=True):

        st.session_state.messages = []
        st.rerun()

with col3:

    if st.button("🕘 History", use_container_width=True):

        if st.session_state.messages:

            st.info(
                f"{len(st.session_state.messages)} messages इस chat में हैं।"
            )

        else:

            st.info("अभी कोई chat history नहीं है।")

# =========================================================
# POPULAR QUESTIONS
# =========================================================

st.markdown(
    '<div class="section-title">💡 Popular Questions</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="popular-box">'
    '<div class="popular-title">'
    '💡 एक क्लिक में अपना सवाल पूछें'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

questions = [
    "Aadhaar kaise banega?",
    "PAN card kaise banega?",
    "Ration card kaise banega?",
    "PM Kisan registration kaise kare?",
    "Ayushman card kaise banega?",
    "Income certificate kaise banega?"
]

q1, q2, q3 = st.columns(3)

selected_question = None

with q1:
    if st.button("🪪 Aadhaar kaise banega?"):
        selected_question = questions[0]

with q2:
    if st.button("💳 PAN card kaise banega?"):
        selected_question = questions[1]

with q3:
    if st.button("🛒 Ration card kaise banega?"):
        selected_question = questions[2]

q4, q5, q6 = st.columns(3)

with q4:
    if st.button("🌱 PM Kisan registration kaise kare?"):
        selected_question = questions[3]

with q5:
    if st.button("🏥 Ayushman card kaise banega?"):
        selected_question = questions[4]

with q6:
    if st.button("📜 Income certificate kaise banega?"):
        selected_question = questions[5]

# =========================================================
# DISPLAY OLD CHAT
# =========================================================

for message in st.session_state.messages:

    avatar = "👤" if message["role"] == "user" else "🤖"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.markdown(message["content"])

# =========================================================
# USER INPUT
# =========================================================

user_message = st.chat_input(
    "अपना सवाल लिखें... जैसे: Aadhaar card kaise banega?"
)

# Popular question clicked
if selected_question:
    user_message = selected_question

# =========================================================
# AI RESPONSE
# =========================================================

if user_message:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_message)

    # AI response
    with st.chat_message("assistant", avatar="🤖"):

        try:

            response = None

            # Retry up to 3 times for temporary 503 errors
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

                    error_text = str(e)

                    if "503" in error_text and attempt < 2:

                        time.sleep(3)

                    else:

                        raise e

            # Get AI reply
            reply = response.text

            st.markdown(reply)

            # Save AI reply
            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

        except Exception as e:

            error_text = str(e)

            if "503" in error_text:

                reply = (
                    "⚠️ Gemini server अभी busy है। "
                    "कुछ सेकंड बाद फिर से कोशिश करें।"
                )

            else:

                reply = f"⚠️ AI Error: {error_text}"

            st.markdown(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

# =========================================================
# INPUT HELP
# =========================================================

st.markdown("""
<div style="
    text-align:center;
    margin-top:15px;
    color:#66708b;
    font-size:12px;
">
💡 यह AI सहायक है। महत्वपूर्ण जानकारी के लिए संबंधित
आधिकारिक सरकारी पोर्टल पर भी पुष्टि करें।
</div>
""", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

    <div class="footer-main">
        🛡️ Trusted Information &nbsp; • &nbsp;
        CSC_HELPDESK_AI • Digital Service Assistant
    </div>

    <div class="footer-line">
        🇮🇳 Digital India &nbsp; | &nbsp;
        Common Service Center &nbsp; | &nbsp;
        Jan Seva &nbsp; | &nbsp;
        Viksit Bharat
    </div>

    <div class="footer-line">
        ⚡ Fast &nbsp; | &nbsp; ⚙️ Simple &nbsp; | &nbsp; 🛡️ Reliable
    </div>

</div>
""", unsafe_allow_html=True)
