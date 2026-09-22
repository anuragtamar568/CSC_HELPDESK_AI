import os
import streamlit as st
from google import genai

st.set_page_config(
    page_title="CSC_HELPDESK_AI",
    page_icon="🤖",
    layout="centered"
)

# Gemini API Key
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY is not configured.")
    st.stop()

client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
You are CSC_HELPDESK_AI, a helpful digital assistant for CSC and
Indian government service guidance.

Help users understand:
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

Rules:
1. Reply in Hindi when the user writes Hindi.
2. Reply in Hinglish when the user writes Hinglish.
3. Reply in English when the user writes English.
4. Keep answers simple and easy to understand.
5. Give step-by-step instructions when appropriate.
6. Do not invent government rules, fees, websites or deadlines.
7. If information may have changed, tell the user to verify it
   on the official government portal.
8. Never ask for passwords, OTPs, PINs or other sensitive credentials.
9. Be polite and helpful.
"""

st.title("🤖 CSC_HELPDESK_AI")
st.caption("CSC & Government Service AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_message = st.chat_input("अपना सवाल लिखें...")

if user_message:
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("user"):
        st.markdown(user_message)

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=user_message,
            config={
                "system_instruction": SYSTEM_PROMPT
            }
        )

        reply = response.text

    except Exception as e:
        reply = f"Error: {str(e)}"

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
