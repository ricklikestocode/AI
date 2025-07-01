import os
import datetime
from gtts import gTTS
from fpdf import FPDF
from twilio.rest import Client
import requests

# Set your Groq API key
GROQ_API_KEY = "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"

# Twilio credentials (replace with your own)
TWILIO_SID = "AC9fa1820b07d74e923f320ec1c7b65101"
TWILIO_AUTH_TOKEN = "57323d684cde0d16cff7aef800093a71"
TWILIO_FROM_NUMBER = "+17439027480"
TO_PHONE_NUMBER = "+917207431844"

def generate_excuse(prompt):
    response = requests.post(
        url="https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "user", "content": f"Give a sharp, clever, and believable excuse for: {prompt}"}
            ],
            "temperature": 0.7
        }
    )
    return response.json()['choices'][0]['message']['content'].strip()

def speak_excuse(excuse):
    tts = gTTS(text=excuse)
    tts.save("excuse.mp3")
    os.system("start excuse.mp3" if os.name == "nt" else "mpg321 excuse.mp3")

def generate_pdf(prompt, excuse):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Excuse Document", ln=1, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Prompt: {prompt}\n\nExcuse: {excuse}")
    filename = f"excuse_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

def send_sms(excuse):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=excuse,
        from_=TWILIO_FROM_NUMBER,
        to=TO_PHONE_NUMBER
    )
    return message.sid

def main():
    print("\n🎤 Rutwik's Official Excuse Generator AI")
    prompt = input("\n👉 What do you need an excuse for?\n> ")
    excuse = generate_excuse(prompt)
    print(f"\n🤖 Excuse: {excuse}\n")

    speak_excuse(excuse)
    pdf_file = generate_pdf(prompt, excuse)
    print(f"📄 PDF Proof Generated: {pdf_file}")

    try:
        sid = send_sms(excuse)
        print(f"📲 SMS sent (SID: {sid})")
    except Exception as e:
        print(f"⚠️ SMS Error: {e}")

if __name__ == "__main__":
    main()
