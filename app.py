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
    page_icon="&#129302;",
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
# SAFE INLINE ICONS
# =========================================================
# No external emoji images: inline SVGs avoid square-box/font problems.
def icon_svg(code, size=30):
    labels = {
        "1f6e0": ("⚙", "#61dafb"), "1f4c4": ("A", "#00e5ff"),
        "1f4b3": ("P", "#a78bfa"), "1f4e6": ("R", "#f59e0b"),
        "1f331": ("K", "#4ade80"), "1f3e5": ("H", "#fb7185"),
        "1f4cb": ("C", "#22d3ee"), "1f464": ("P", "#fbbf24"),
        "1f4bb": ("E", "#60a5fa"), "1f3e2": ("C", "#c084fc"),
        "1f4a1": ("?", "#facc15"), "1f64f": ("✓", "#4ade80"),
        "1f4de": ("☎", "#38bdf8"),
    }
    label, accent = labels.get(code, ("•", "#67e8f9"))
    return f"""<span class="svg-icon" style="width:{size}px;height:{size}px;">
<svg viewBox="0 0 64 64" width="{size}" height="{size}" aria-hidden="true">
<defs><linearGradient id="g{code}{size}" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="white"/><stop offset="100%" stop-color="{accent}"/></linearGradient></defs>
<circle cx="32" cy="32" r="29" fill="rgba(4,15,30,.92)" stroke="url(#g{code}{size})" stroke-width="2.5"/>
<circle cx="32" cy="32" r="22" fill="none" stroke="{accent}" stroke-opacity=".22"/>
<text x="32" y="40" text-anchor="middle" font-size="25" font-family="Arial,sans-serif" font-weight="800" fill="white">{label}</text>
</svg></span>"""

# =========================================================
# PREMIUM DARK CINEMATIC CSS
# =========================================================

st.markdown(
    """
<style>
:root { --cyan:#00e5ff; --purple:#a855f7; --pink:#ec4899; --green:#39ff88; --text:#eaf8ff; }
.stApp { min-height:100vh; color:var(--text); background:radial-gradient(circle at 8% 8%,rgba(0,229,255,.16),transparent 24%),radial-gradient(circle at 92% 12%,rgba(168,85,247,.18),transparent 25%),radial-gradient(circle at 50% 105%,rgba(236,72,153,.10),transparent 30%),linear-gradient(135deg,#02040b 0%,#050816 42%,#080414 100%); font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",Arial,sans-serif; }
.stApp::before { content:""; position:fixed; inset:0; pointer-events:none; background:linear-gradient(115deg,transparent,rgba(0,229,255,.025),rgba(168,85,247,.025),transparent); animation:sweep 10s ease-in-out infinite alternate; }
@keyframes sweep { from{transform:translateX(-8%)} to{transform:translateX(8%)} }
@keyframes pulseGlow { 0%,100%{box-shadow:0 0 10px rgba(0,229,255,.15)} 50%{box-shadow:0 0 28px rgba(0,229,255,.30)} }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-3px)} }
@keyframes gradientText { to{background-position:250% center} }
.block-container { max-width:1400px; padding-top:24px; padding-bottom:55px; }
.hero-box { position:relative; overflow:hidden; text-align:center; padding:30px 25px 26px; border-radius:32px; background:linear-gradient(135deg,rgba(8,18,35,.82),rgba(10,5,25,.78)); border:1px solid rgba(0,229,255,.20); box-shadow:0 25px 80px rgba(0,0,0,.48),inset 0 1px 0 rgba(255,255,255,.06); backdrop-filter:blur(22px); }
.hero-box::before { content:""; position:absolute; top:0; left:8%; width:84%; height:2px; background:linear-gradient(90deg,transparent,var(--cyan),var(--purple),var(--pink),transparent); box-shadow:0 0 20px var(--cyan),0 0 40px rgba(168,85,247,.45); }
.hero-box::after { content:""; position:absolute; width:220px; height:220px; border-radius:50%; right:-110px; top:-130px; background:rgba(168,85,247,.14); filter:blur(30px); }
.title { font-size:clamp(34px,5vw,58px); font-weight:950; letter-spacing:3px; background:linear-gradient(90deg,#fff,var(--cyan),#fff,var(--purple),#fff); background-size:250% auto; -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; animation:gradientText 5s linear infinite; text-shadow:0 0 30px rgba(0,229,255,.22); }
.subtitle { color:#b5d8e8; font-size:17px; margin-top:7px; }
.online { display:inline-flex; align-items:center; gap:8px; margin-top:15px; padding:8px 18px; border-radius:999px; color:#6dffb1; background:rgba(57,255,136,.06); border:1px solid rgba(57,255,136,.30); font-weight:800; animation:pulseGlow 3s ease-in-out infinite; }
.tagline { margin-top:13px; color:#718b9b; font-size:13px; letter-spacing:.4px; }
.section { display:flex; align-items:center; gap:10px; font-size:23px; font-weight:900; color:#f0fbff; margin-top:30px; margin-bottom:15px; letter-spacing:.2px; text-shadow:0 0 20px rgba(0,229,255,.22); }
.svg-icon { display:inline-flex; align-items:center; justify-content:center; vertical-align:middle; flex:none; }
.service-card { position:relative; overflow:hidden; text-align:center; padding:17px 6px; min-height:108px; border-radius:22px; background:linear-gradient(145deg,rgba(11,29,49,.82),rgba(8,8,22,.88)); border:1px solid rgba(0,229,255,.14); box-shadow:0 12px 35px rgba(0,0,0,.34),inset 0 1px 0 rgba(255,255,255,.04); transition:.28s ease; backdrop-filter:blur(16px); }
.service-card::after { content:""; position:absolute; left:10%; right:10%; bottom:-20px; height:35px; background:rgba(0,229,255,.12); filter:blur(22px); }
.service-card:hover { transform:translateY(-7px) scale(1.025); border-color:rgba(0,229,255,.60); box-shadow:0 0 30px rgba(0,229,255,.16),0 18px 40px rgba(0,0,0,.45); }
.service-icon { display:flex; justify-content:center; animation:float 4s ease-in-out infinite; }
.service-name { color:#c9e5ef; font-size:12px; font-weight:800; margin-top:9px; letter-spacing:.2px; }
.popular { padding:18px; border-radius:25px; background:linear-gradient(145deg,rgba(11,22,42,.76),rgba(10,5,24,.78)); border:1px solid rgba(168,85,247,.18); box-shadow:0 18px 50px rgba(0,0,0,.35); backdrop-filter:blur(18px); }
.stButton > button { width:100%; min-height:42px; border-radius:14px; border:1px solid rgba(0,229,255,.24); background:linear-gradient(135deg,rgba(8,31,50,.92),rgba(18,8,38,.92)); color:#d9f8ff; font-weight:800; box-shadow:0 7px 20px rgba(0,0,0,.28); transition:.22s ease; }
.stButton > button:hover { border-color:var(--cyan); color:#fff; transform:translateY(-2px); box-shadow:0 0 24px rgba(0,229,255,.20); }
[data-testid="stChatMessage"] { background:linear-gradient(135deg,rgba(7,20,36,.72),rgba(14,7,28,.68)); border:1px solid rgba(0,229,255,.10); border-radius:20px; margin-bottom:12px; padding:10px 14px; box-shadow:0 10px 30px rgba(0,0,0,.20); backdrop-filter:blur(14px); }
[data-testid="stChatMessage"] p { color:#d9edf5; line-height:1.65; }
[data-testid="stChatInput"] { background:rgba(3,8,20,.86); border-radius:24px; box-shadow:0 0 35px rgba(0,229,255,.07); }
[data-testid="stChatInput"] textarea { background:#071321 !important; color:#e8faff !important; border:2px solid rgba(0,229,255,.28) !important; border-radius:20px !important; font-size:16px !important; caret-color:var(--cyan) !important; }
[data-testid="stChatInput"] textarea:focus { border-color:var(--cyan) !important; box-shadow:0 0 22px rgba(0,229,255,.16) !important; }
.error-card { display:flex; gap:14px; align-items:flex-start; padding:18px 20px; margin:2px 0 5px; border-radius:18px; background:linear-gradient(135deg,rgba(10,30,38,.92),rgba(14,8,28,.92)); border:1px solid rgba(57,255,136,.25); box-shadow:0 0 28px rgba(57,255,136,.07),inset 0 1px 0 rgba(255,255,255,.05); }
.error-card .big { font-size:16px; font-weight:850; color:#f2ffff; }
.error-card .small { color:#a8c3ce; margin-top:5px; line-height:1.55; }
.error-card .phone { color:#69e7ff; font-weight:900; font-size:18px; margin-top:8px; }
section[data-testid="stSidebar"] { background:linear-gradient(180deg,#020611,#080416,#02030a); border-right:1px solid rgba(0,229,255,.12); }
.footer { text-align:center; margin-top:48px; padding:26px; color:#668392; font-size:12px; border-top:1px solid rgba(0,229,255,.08); }
.stMarkdown { color:#d7edf5; }
::-webkit-scrollbar { width:7px; } ::-webkit-scrollbar-track { background:#02040a; } ::-webkit-scrollbar-thumb { background:linear-gradient(var(--cyan),var(--purple)); border-radius:10px; }
@media(max-width:700px) { .block-container{padding-left:12px;padding-right:12px}.title{font-size:30px}.hero-box{padding:20px 12px;border-radius:22px}.service-card{min-height:95px}.service-name{font-size:11px} }
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
&#9989; Haan, ye kaam humare yahan ho jayega.
&#128204; Kaam: <service>
&#128176; Hamara charge: ₹<service charge>
&#127963;&#65039; Official/Government fee: <configured value>
&#128196; Zaroori documents: <configured documents>
&#9201;&#65039; Approx. time: <configured time>

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
        '&#128994; AI Assistant Online'
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
    f'<div class="section">{icon_svg("1f6e0", 28)} CSC Services</div>',
    unsafe_allow_html=True
)

services = [
    ("1f4c4", "Aadhaar"),
    ("1f4b3", "PAN Card"),
    ("1f4e6", "Ration Card"),
    ("1f331", "PM Kisan"),
    ("1f3e5", "Ayushman"),
    ("1f4cb", "Certificates"),
    ("1f464", "Pension"),
    ("1f4bb", "e-District"),
    ("1f3e2", "CSC Services"),
    ("", "More Services")
]

columns = st.columns(10)

for col, item in zip(columns, services):

    with col:

        st.markdown(
            f"""
            <div class="service-card">
                <div class="service-icon">{icon_svg(item[0], 34) if item[0] else "•••"}</div>
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

    if st.button("↻ New Chat"):

        st.session_state.messages = []
        st.rerun()

with c3:

    if st.button("◷ History"):

        st.info(
            f"Current chat में "
            f"{len(st.session_state.messages)} messages हैं।"
        )

# =========================================================
# POPULAR QUESTIONS
# =========================================================

st.markdown(
    f'<div class="section">{icon_svg("1f4a1", 28)} Popular Questions</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="popular">',
    unsafe_allow_html=True
)

p1, p2, p3, p4 = st.columns(4)

popular_question = None

with p1:
    if st.button("▣ Aadhaar Print"):
        popular_question = "Aadhaar print ka charge kitna hai?"

with p2:
    if st.button("▣ PAN Card"):
        popular_question = "PAN card banwane ka charge kitna hai aur kya documents lagenge?"

with p3:
    if st.button("▤ Certificate"):
        popular_question = "Income, caste ya residence certificate ka kaam ho jayega? Charge batao."

with p4:
    if st.button("✎ Online Form"):
        popular_question = "Online form bharne ka charge kitna hai?"

st.markdown(
    '</div>',
    unsafe_allow_html=True
)

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

        except Exception as e:

            # Customer ko technical/server details nahi dikhani hain.
            reply = (
                "मैं अभी थोड़ा व्यस्त हूँ। कृपया हमारे Owner Vicky Choudhary Ji से बात कर लीजिए और आवश्यक जानकारी ले लीजिए। "
                "Mobile No.: 8826066468. धन्यवाद, आपका दिन शुभ हो।"
            )

            st.markdown(
                f'''<div class="error-card">
                    {icon_svg("1f64f", 42)}
                    <div>
                        <div class="big">मैं अभी थोड़ा व्यस्त हूँ।</div>
                        <div class="small">कृपया हमारे Owner <b>Vicky Choudhary Ji</b> से बात कर लीजिए और आवश्यक जानकारी ले लीजिए।</div>
                        <div class="phone">☎ &nbsp;8826066468</div>
                        <div class="small">धन्यवाद • आपका दिन शुभ हो।</div>
                    </div>
                </div>''',
                unsafe_allow_html=True
            )

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
        &#128737;&#65039; Trusted Information For A Better Tomorrow
        <br><br>
        <b>CSC_HELPDESK_AI</b>
        • Digital Service Assistant
        <br>
        &#127470;&#127475; Digital India &nbsp; | &nbsp;
        Common Service Center &nbsp; | &nbsp;
        Jan Seva
        <br><br>
        &#9889; Fast &nbsp; | &nbsp;
        &#9881;&#65039; Simple &nbsp; | &nbsp;
        &#128737;&#65039; Reliable
    </div>
    """,
    unsafe_allow_html=True
)
