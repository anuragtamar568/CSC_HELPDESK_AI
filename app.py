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
# PREMIUM DARK CINEMATIC CSS
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(0, 183, 255, 0.14), transparent 25%),
        radial-gradient(circle at 85% 15%, rgba(79, 70, 229, 0.14), transparent 28%),
        radial-gradient(circle at 50% 100%, rgba(0, 255, 200, 0.06), transparent 35%),
        linear-gradient(135deg, #030712 0%, #050816 45%, #020617 100%);
    color: #e5f7ff;
}

.block-container {
    max-width: 1350px;
    padding-top: 25px;
    padding-bottom: 60px;
}

.hero-box {
    position: relative;
    text-align: center;
    padding: 30px 25px;
    border-radius: 30px;
    background: linear-gradient(135deg, rgba(10, 25, 45, 0.88), rgba(5, 12, 28, 0.82));
    border: 1px solid rgba(0, 200, 255, 0.25);
    box-shadow: 0 0 40px rgba(0, 180, 255, 0.08), inset 0 0 30px rgba(0, 150, 255, 0.035);
    backdrop-filter: blur(18px);
}

.hero-box::before {
    content: "";
    position: absolute;
    top: 0;
    left: 12%;
    width: 76%;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00d9ff, #6d5dfc, #00d9ff, transparent);
    box-shadow: 0 0 15px #00d9ff, 0 0 30px rgba(0, 217, 255, 0.5);
    border-radius: 10px;
}

.title {
    font-size: 48px;
    font-weight: 900;
    letter-spacing: 2px;
    background: linear-gradient(90deg, #ffffff, #5ee7ff, #00c8ff, #7c6cff, #ffffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 25px rgba(0, 200, 255, 0.25);
}

.subtitle {
    color: #9fc8d8;
    font-size: 18px;
    margin-top: 5px;
}

.online {
    display: inline-block;
    margin-top: 15px;
    padding: 8px 20px;
    border-radius: 30px;
    color: #5dffcb;
    background: rgba(0, 255, 180, 0.07);
    border: 1px solid rgba(0, 255, 180, 0.35);
    font-weight: 700;
    box-shadow: 0 0 18px rgba(0, 255, 180, 0.08);
}

.tagline {
    margin-top: 14px;
    color: #6f91a1;
    font-size: 14px;
}

.section {
    font-size: 23px;
    font-weight: 800;
    color: #d9f8ff;
    margin-top: 30px;
    margin-bottom: 15px;
    letter-spacing: 0.3px;
    text-shadow: 0 0 15px rgba(0, 200, 255, 0.18);
}

.service-card {
    position: relative;
    text-align: center;
    padding: 20px 7px;
    min-height: 110px;
    border-radius: 20px;
    background: linear-gradient(145deg, rgba(12, 30, 50, 0.88), rgba(4, 14, 28, 0.92));
    border: 1px solid rgba(0, 190, 255, 0.16);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.35), inset 0 0 20px rgba(0, 160, 255, 0.025);
    transition: all 0.25s ease;
}

.service-card:hover {
    transform: translateY(-5px);
    border-color: rgba(0, 210, 255, 0.5);
    box-shadow: 0 0 25px rgba(0, 190, 255, 0.12), 0 12px 30px rgba(0, 0, 0, 0.45);
}

.service-icon {
    font-size: 34px;
    filter: drop-shadow(0 0 8px rgba(0, 210, 255, 0.3));
}

.service-name {
    color: #b9dbe6;
    font-size: 13px;
    font-weight: 700;
    margin-top: 8px;
}

.popular {
    padding: 20px;
    border-radius: 24px;
    background: linear-gradient(145deg, rgba(10, 27, 45, 0.82), rgba(3, 12, 25, 0.88));
    border: 1px solid rgba(0, 190, 255, 0.15);
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(15px);
}

.stButton > button {
    width: 100%;
    min-height: 42px;
    border-radius: 14px;
    border: 1px solid rgba(0, 200, 255, 0.25);
    background: linear-gradient(135deg, rgba(8, 28, 48, 0.95), rgba(5, 17, 32, 0.95));
    color: #c9f5ff;
    font-weight: 700;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.25);
    transition: all 0.25s ease;
}

.stButton > button:hover {
    border-color: #00d9ff;
    color: #ffffff;
    background: linear-gradient(135deg, rgba(0, 150, 220, 0.18), rgba(70, 80, 255, 0.15));
    box-shadow: 0 0 18px rgba(0, 210, 255, 0.18);
    transform: translateY(-2px);
}

[data-testid="stChatMessage"] {
    background: rgba(5, 18, 32, 0.55);
    border: 1px solid rgba(0, 190, 255, 0.08);
    border-radius: 18px;
    margin-bottom: 10px;
    padding: 8px 12px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.18);
}

[data-testid="stChatInput"] {
    background: rgba(3, 12, 24, 0.85);
    border-radius: 22px;
    box-shadow: 0 0 25px rgba(0, 170, 255, 0.06);
}

[data-testid="stChatInput"] textarea {
    background: #071321 !important;
    color: #e8faff !important;
    border: 2px solid rgba(0, 200, 255, 0.35) !important;
    border-radius: 20px !important;
    font-size: 16px !important;
    caret-color: #00d9ff !important;
}

[data-testid="stChatInput"] textarea:focus {
    border: 2px solid #00d9ff !important;
    box-shadow: 0 0 18px rgba(0, 217, 255, 0.15) !important;
}

[data-testid="stChatMessage"] p {
    color: #d7edf5;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020812, #030b16, #020611);
    border-right: 1px solid rgba(0, 200, 255, 0.12);
}

hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0, 200, 255, 0.25), transparent);
}

.footer {
    text-align: center;
    margin-top: 45px;
    padding: 25px;
    color: #668392;
    font-size: 13px;
    border-top: 1px solid rgba(0, 190, 255, 0.08);
}

.stMarkdown {
    color: #d7edf5;
}

::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-track {
    background: #020611;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(#00bfe7, #5d5cff);
    border-radius: 10px;
}

@media(max-width: 700px) {
    .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }

    .title {
        font-size: 30px;
        letter-spacing: 1px;
    }

    .subtitle {
        font-size: 14px;
    }

    .hero-box {
        padding: 20px 12px;
        border-radius: 22px;
    }

    .service-card {
        min-height: 95px;
    }

    .service-icon {
        font-size: 27px;
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
# OUR SERVICE CATALOG / PRICE LIST
# =========================================================
# APNE ACTUAL CHARGES YAHAN EDIT KARO.
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
Hindi question = Hindi answer.
Hinglish question = Hinglish answer.
English question = English answer.

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
    if st.button("🪪 Aadhaar Print"):
        popular_question = "Aadhaar print ka charge kitna hai?"

with p2:
    if st.button("💳 PAN Card"):
        popular_question = "PAN card banwane ka charge kitna hai aur kya documents lagenge?"

with p3:
    if st.button("📜 Certificate"):
        popular_question = "Income, caste ya residence certificate ka kaam ho jayega? Charge batao."

with p4:
    if st.button("📝 Online Form"):
        popular_question = "Online form bharne ka charge kitna hai?"

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
