import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

# Gemini API Key
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
You are CSC_HELPDESK_AI, a helpful digital assistant for CSC and
Indian government service guidance.

Your job is to help users understand:
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

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "assistant": "CSC_HELPDESK_AI"
    })


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({
                "error": "Message is required"
            }), 400

        user_message = data["message"].strip()

        if not user_message:
            return jsonify({
                "error": "Message cannot be empty"
            }), 400

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=user_message,
            config={
                "system_instruction": SYSTEM_PROMPT
            }
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
