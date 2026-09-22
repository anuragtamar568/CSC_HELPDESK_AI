import os
import time
import streamlit as st
from google import genai

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CSC_HELPDESK_AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CUSTOM THEME
# =========================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(80, 120, 255, 0.18), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(170, 70, 255, 0.18), transparent 30%),
        linear-gradient(135deg, #f5f7ff 0%, #eef1ff 50%, #f8f3ff 100%);
}

/* Main container */
.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 6rem;
}

/* Header */
.ai-header {
    text-align: center;
    padding: 25px 20px;
    margin-bottom: 25px;
    border-radius: 25px;
    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.95),
        rgba(240,243,255,0.95)
    );
    border: 1px solid rgba(100,120,255,0.25);
    box-shadow:
        0 10px 35px rgba(65, 80, 180, 0.15),
        0 0 30px rgba(130, 80, 255, 0.08);
}

/* Logo */
.ai-logo {
    font-size: 55px;
    margin-bottom: 5px;
    filter: drop-shadow(0 0 12px rgba(80,100,255,0.45));
}

/* Main title */
.ai-title {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: 1px;
    background: linear-gradient(90deg, #315cff, #8b3dff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle */
.ai-subtitle {
    color: #5d6680;
    font-size: 15px;
    margin-top: 5px;
}

/* Online badge */
.online-badge {
    display: inline-block;
    margin-top: 12px;
    padding: 7px 16px;
    border-radius: 30px;
    background: rgba(55, 200, 120, 0.12);
    color: #16834c;
    border: 1px solid rgba(55, 200, 120, 0.3);
    font-size: 13px;
    font-weight: 600;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    border-radius: 18px;
    margin-bottom: 12px;
}

/* User message */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(
        135deg,
        rgba(75, 100, 255, 0.10),
        rgba(130, 75, 255, 0.08)
    );
    border: 1px solid rgba(80, 100, 255, 0.15);
}

/* Assistant message */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: rgba(255,255,255,0.85);
    border: 1px solid rgba(130, 100, 255, 0.15);
    box-shadow: 0 5px 20px rgba(70,80,160,0.07);
}

/* Chat input */
[data-testid="stChatInput"] {
    border-radius: 18px !important;
}

/* Input box */
[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.95) !important;
    border: 2px solid rgba(85,95,255,0.25) !important;
    border-radius: 18px !important;
    color: #20243a !important;
    font-size: 16px !important;
}

/* Input focus */
[data-testid="stChatInput"] textarea:focus {
    border: 2px solid #6c55ff !important;
    box-shadow:
        0 0 12px rgba(100,80,255,0.25) !important;
}

/* Buttons */
.stButton > button {
    border-radius: 14px;
    border: 1px solid rgba(90,90,255,0.25);
    background: linear-gradient(135deg, #5268ff, #884bff);
    color: white;
    font-weight: 600;
    box-shadow: 0 5px 15px rgba(90,80,220,0.20);
}

/* Footer */
.ai-footer {
    text-align: center;
    margin-top: 30px;
    color: #747b92;
    font-size: 12px;
}

/* Mobile */
@media (max-width: 600px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .ai-title {
        font-size: 26px;
    }

    .ai-logo {
        font-size: 45px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="ai-header">

    <div class="ai-logo">🤖</div>

    <div class="ai-title">
        CSC_HELPDESK_AI
    </div>

    <div class="ai-subtitle">
        Smart Assistant for CSC & Government Services
    </div>

    <div class="online-badge">
        🟢 AI Assistant Online
    </div>

</div>
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

You help users understand:

- Aadhaar
- PAN Card
- Ration Card
- PM Kisan
- Ayushman Card
- Income Certificate
- Caste Certificate
- Residence Certificate
- Birth Certificate
- Pension
- e-District services
- Government forms
- CSC services
- General digital service guidance

RULES:

1. Reply in Hindi when the user writes Hindi.
2. Reply in Hinglish when the user writes Hinglish.
3. Reply in English when the user writes English.
4. Keep answers simple and easy to understand.
5. Give step-by-step instructions when appropriate.
6. Do not invent government rules, fees, websites or deadlines.
7. If information may have changed, tell the user to verify it
   on the official government portal.
8. Never ask for passwords, OTPs, PINs or sensitive credentials.
9. Be polite and helpful.
10. Give a direct answer first for simple questions.
"""

# =========================================================
# CHAT MEMORY
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar="👤" if message["role"] == "user" else "🤖"
    ):
        st.markdown(message["content"])

# =========================================================
# USER INPUT
# =========================================================

user_message = st.chat_input(
    "अपना सवाल लिखें... जैसे: Aadhaar card kaise banega?"
)

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

            # -------------------------------------------------
            # RETRY SYSTEM
            # -------------------------------------------------

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

            # -------------------------------------------------
            # SHOW RESPONSE
            # -------------------------------------------------

            reply = response.text

            st.markdown(reply)

            # Save response
            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

        except Exception as e:

            error_text = str(e)

            if "503" in error_text:

                reply = """
⚠️ **Gemini server अभी busy है।**

कुछ सेकंड बाद अपना सवाल फिर से भेजें।
"""

            else:

                reply = f"""
⚠️ **AI Error**

`{error_text}`
"""

            st.markdown(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="ai-footer">
    CSC_HELPDESK_AI • Digital Service Assistant
</div>
""", unsafe_allow_html=True)
