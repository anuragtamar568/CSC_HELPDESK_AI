import os
import time
import io

import streamlit as st
from google import genai
from PIL import Image, ImageDraw, ImageFilter

# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="CSC_HELPDESK_AI",
    page_icon="🤖",
    layout="wide"
)

# =========================================================
# CREATE ROBOT LOGO AUTOMATICALLY
# =========================================================

def create_robot_logo():
    img = Image.new("RGBA", (500, 500), (0, 0, 0, 0))

    glow = Image.new("RGBA", (500, 500), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)

    gd.ellipse(
        (55, 55, 445, 445),
        fill=(70, 120, 255, 90)
    )

    glow = glow.filter(ImageFilter.GaussianBlur(25))
    img.alpha_composite(glow)

    d = ImageDraw.Draw(img)

    # Outer rings
    d.ellipse(
        (70, 70, 430, 430),
        outline=(30, 205, 255, 255),
        width=10
    )

    d.ellipse(
        (95, 95, 405, 405),
        outline=(145, 75, 255, 230),
        width=8
    )

    # Antenna
    d.line(
        (250, 155, 250, 105),
        fill=(55, 75, 160, 255),
        width=8
    )

    d.ellipse(
        (237, 82, 263, 108),
        fill=(70, 200, 255, 255)
    )

    # Ears
    d.rounded_rectangle(
        (90, 210, 135, 295),
        radius=18,
        fill=(145, 165, 215, 255)
    )

    d.rounded_rectangle(
        (365, 210, 410, 295),
        radius=18,
        fill=(145, 165, 215, 255)
    )

    # Robot head
    d.rounded_rectangle(
        (120, 145, 380, 350),
        radius=60,
        fill=(247, 249, 255, 255),
        outline=(65, 85, 170, 255),
        width=8
    )

    # Face
    d.rounded_rectangle(
        (155, 190, 345, 305),
        radius=35,
        fill=(18, 28, 68, 255)
    )

    # Eyes
    d.ellipse(
        (195, 225, 230, 260),
        fill=(60, 225, 255, 255)
    )

    d.ellipse(
        (270, 225, 305, 260),
        fill=(60, 225, 255, 255)
    )

    # AI badge
    d.rounded_rectangle(
        (195, 315, 305, 365),
        radius=16,
        fill=(85, 65, 230, 255)
    )

    d.text(
        (228, 326),
        "AI",
        fill=(255, 255, 255, 255)
    )

    return img


logo = create_robot_logo()

# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at 10% 5%,
            rgba(40, 150, 255, 0.22),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 5%,
            rgba(160, 80, 255, 0.22),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #eef6ff,
            #f2f0ff,
            #faf4ff
        );
}

.block-container {
    max-width: 1250px;
    padding-top: 20px;
    padding-bottom: 50px;
}

/* HERO */

.hero-box {
    text-align: center;
    padding: 25px;
    border-radius: 30px;
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(90,100,255,0.18);
    box-shadow:
        0 15px 45px rgba(60,80,180,0.14);
}

.title {
    font-size: 46px;
    font-weight: 900;
    letter-spacing: 1px;
    background: linear-gradient(
        90deg,
        #1769ff,
        #6248ff,
        #a33cff
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #344268;
    font-size: 18px;
}

.online {
    display: inline-block;
    margin-top: 12px;
    padding: 8px 20px;
    border-radius: 30px;
    color: #118348;
    background: #e8fff0;
    border: 1px solid #8ce0ad;
    font-weight: 700;
}

.tagline {
    margin-top: 12px;
    color: #66708b;
}

/* SERVICE CARDS */

.service-card {
    text-align: center;
    padding: 18px 7px;
    min-height: 105px;
    border-radius: 20px;
    background: rgba(255,255,255,0.90);
    border: 1px solid rgba(90,110,255,0.15);
    box-shadow: 0 7px 22px rgba(60,75,160,0.08);
}

.service-icon {
    font-size: 34px;
}

.service-name {
    color: #26365f;
    font-size: 13px;
    font-weight: 700;
    margin-top: 7px;
}

/* SECTION */

.section {
    font-size: 22px;
    font-weight: 800;
    color: #203260;
    margin-top: 25px;
    margin-bottom: 12px;
}

/* POPULAR */

.popular {
    padding: 18px;
    border-radius: 22px;
    background: rgba(255,255,255,0.78);
    border: 1px solid rgba(90,100,255,0.15);
    box-shadow: 0 8px 25px rgba(70,80,160,0.07);
}

/* BUTTON */

.stButton > button {
    width: 100%;
    border-radius: 15px;
    border: 1px solid #b9c5ff;
    background: white;
    color: #24458f;
    font-weight: 650;
}

.stButton > button:hover {
    border-color: #6655ff;
    color: #5544dc;
    box-shadow: 0 0 15px rgba(90,80,255,0.15);
}

/* CHAT INPUT */

[data-testid="stChatInput"] textarea {
    background: white !important;
    border: 2px solid #675cff !important;
    border-radius: 20px !important;
    font-size: 16px !important;
}

/* FOOTER */

.footer {
    text-align: center;
    margin-top: 35px;
    padding: 20px;
    color: #66708b;
    font-size: 13px;
}

@media(max-width:700px) {

    .title {
        font-size: 30px;
    }

    .subtitle {
        font-size: 14px;
    }

}

</style>
""",
    unsafe_allow_html=True
)

# =========================================================
# GEMINI
# =========================================================

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY is not configured.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# =========================================================
# AI PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are CSC_HELPDESK_AI.

You are a helpful assistant for CSC and Indian government
digital services.

Help users with:

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

Rules:

1. Hindi question = Hindi answer.
2. Hinglish question = Hinglish answer.
3. English question = English answer.
4. Keep answers simple.
5. Give step-by-step instructions.
6. Never invent fees, rules or deadlines.
7. Tell users to verify changing information on official portals.
8. Never ask for OTP, password, PIN or sensitive credentials.
9. Be polite.
10. Give the direct answer first.
"""

# =========================================================
# CHAT MEMORY
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="hero-box">',
    unsafe_allow_html=True
)

col_logo, col_title = st.columns([1, 4])

with col_logo:
    st.image(
        logo,
        width=145
    )

with col_title:
    st.markdown(
        '<div class="title">CSC_HELPDESK_AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Smart Assistant for CSC & Government Services'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="online">'
        '🟢 AI Assistant Online'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tagline">'
        'Aapka Sawal &nbsp; | &nbsp; Hamari Madad '
        '&nbsp; | &nbsp; Digital Bharat'
        '</div>',
        unsafe_allow_html=True
    )

st.markdown(
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# SERVICES
# =========================================================

st.markdown(
    '<div class="section">🛠️ CSC Services</div>',
    unsafe_allow_html=True
)

services = [
    ("🪪", "Aadhaar"),
    ("💳", "PAN Card"),
    ("🛍️", "Ration Card"),
    ("🌱", "PM Kisan"),
    ("🏥", "Ayushman"),
    ("📜", "Certificates"),
    ("👨‍👩‍👧", "Pension"),
    ("🖥️", "e-District"),
    ("🏛️", "CSC Services"),
    ("•••", "More Services")
]

columns = st.columns(10)

for col, item in zip(columns, services):

    with col:

        st.markdown(
            f"""
            <div class="service-card">
                <div class="service-icon">{item[0]}</div>
                <div class="service-name">{item[1]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# NEW CHAT / HISTORY
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([7, 1.5, 1.5])

with c2:

    if st.button("🔄 New Chat"):

        st.session_state.messages = []
        st.rerun()

with c3:

    if st.button("🕘 History"):

        st.info(
            f"Current chat में "
            f"{len(st.session_state.messages)} messages हैं।"
        )

# =========================================================
# POPULAR QUESTIONS
# =========================================================

st.markdown(
    '<div class="section">💡 Popular Questions</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="popular">',
    unsafe_allow_html=True
)

p1, p2, p3, p4 = st.columns(4)

popular_question = None

with p1:
    if st.button("🪪 Aadhaar kaise banega?"):
        popular_question = "Aadhaar card kaise banega?"

with p2:
    if st.button("💳 PAN card kaise banega?"):
        popular_question = "PAN card kaise banega?"

with p3:
    if st.button("🛍️ Ration card kaise banega?"):
        popular_question = "Ration card kaise banega?"

with p4:
    if st.button("🌱 PM Kisan registration?"):
        popular_question = "PM Kisan registration kaise kare?"

st.markdown(
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# OLD MESSAGES
# =========================================================

for message in st.session_state.messages:

    avatar = (
        "👤"
        if message["role"] == "user"
        else "🤖"
    )

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

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_message)

    with st.chat_message("assistant", avatar="🤖"):

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

        except Exception as e:

            if "503" in str(e):

                reply = (
                    "⚠️ Gemini server अभी busy है। "
                    "कुछ सेकंड बाद फिर से कोशिश करें।"
                )

            else:

                reply = (
                    f"⚠️ AI Error: {str(e)}"
                )

            st.markdown(reply)

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
        🛡️ Trusted Information For A Better Tomorrow
        <br><br>
        <b>CSC_HELPDESK_AI</b>
        • Digital Service Assistant
        <br>
        🇮🇳 Digital India &nbsp; | &nbsp;
        Common Service Center &nbsp; | &nbsp;
        Jan Seva
        <br><br>
        ⚡ Fast &nbsp; | &nbsp;
        ⚙️ Simple &nbsp; | &nbsp;
        🛡️ Reliable
    </div>
    """,
    unsafe_allow_html=True
)
