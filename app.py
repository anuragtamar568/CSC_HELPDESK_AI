import os
import time
import streamlit as st
from google import genai

st.set_page_config(
    page_title="CSC_HELPDESK_AI",
    page_icon="🤖",
    layout="centered"
)

# =========================
# THEME
# =========================

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(70,120,255,0.18), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(170,70,255,0.18), transparent 30%),
        linear-gradient(135deg, #f3f6ff 0%, #eef0ff 50%, #f8f1ff 100%);
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 5rem;
}

.ai-header {
    text-align: center;
    padding: 28px 20px;
    margin-bottom: 25px;
    border-radius: 25px;
    background: linear-gradient(135deg, #ffffff, #f1f3ff);
    border: 1px solid rgba(90,100,255,0.25);
    box-shadow: 0 10px 35px rgba(70,80,180,0.15);
}

.ai-logo {
    font-size: 55px;
    margin-bottom: 8px;
}

.ai-title {
    font-size: 34px;
    font-weight: 800;
    background: linear-gradient(90deg, #315cff, #8b3dff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.ai-subtitle {
    color: #606a85;
    font-size: 15px;
    margin-top: 6px;
}

.online-badge {
    display: inline-block;
    margin-top: 12px;
    padding: 7px 16px;
    border-radius: 30px;
    background: #e9fff2;
    color: #16834c;
    border: 1px solid #a9e8c4;
    font-size: 13px;
    font-weight: 600;
}

[data-testid="stChatMessage"] {
    border-radius: 18px;
    margin-bottom: 12px;
}

[data-testid="stChatInput"] textarea {
    background: white !important;
    border: 2px solid rgba(90,90,255,0.25) !important;
    border-radius: 18px !important;
    font-size: 16px !important;
}

[data-testid="stChatInput"] textarea:focus {
    border: 2px solid #6c55ff !important;
    box-shadow: 0 0 15px rgba(100,80,255,0.25) !important;
}

.ai-footer {
    text-align: center;
    margin-top: 30px;
    color: #747b92;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.markdown("""
<div class="ai-header">
<div class="ai-logo">🤖</div>
<div class="ai-title">CSC_HELPDESK_AI</div>
<div class="ai-subtitle">Smart Assistant for CSC & Government Services</div>
<div class="online-badge">🟢 AI Assistant Online</div>
</div>
""", unsafe_allow_html=True)

# =========================
# GEMINI API
# =========================

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY is not configured.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# =========================
# AI INSTRUCTIONS
# =========================

SYSTEM_PROMPT = """
You are CSC_HELPDESK_AI, a helpful digital assistant for CSC
and Indian government service guidance.

You help users with:
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
- e-District
- Government forms
- CSC services

Rules:
1. Reply in Hindi when user writes Hindi.
2. Reply in Hinglish when user writes Hinglish.
3. Reply in English when user writes English.
4. Keep answers simple.
5. Give step-by-step instructions.
6. Do not invent government rules, fees or deadlines.
7. Tell users to verify changing information on official portals.
8. Never ask for OTP, PIN, password or sensitive credentials.
9. Be polite and helpful.
"""

# =========================
# CHAT MEMORY
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# SHOW CHAT
# =========================

for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# =========================
# INPUT
# =========================

user_message = st.chat_input(
    "अपना सवाल लिखें... जैसे: Aadhaar card kaise banega?"
)

# =========================
# AI ANSWER
# =========================

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
                reply = "⚠️ Gemini server अभी busy है। कुछ सेकंड बाद फिर कोशिश करें।"
            else:
                reply = f"⚠️ Error: {str(e)}"

            st.markdown(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

# =========================
# FOOTER
# =========================

st.markdown("""
<div class="ai-footer">
CSC_HELPDESK_AI • Digital Service Assistant
</div>
""", unsafe_allow_html=True)
