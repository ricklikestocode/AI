import streamlit as st
from groq import Groq
from gtts import gTTS
from fpdf import FPDF
from twilio.rest import Client
import datetime
import os

# === CONFIG ===
GROQ_API_KEY = "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"
MODEL = "llama3-70b-8192"
TWILIO_SID = "AC9fa1820b07d74e923f320ec1c7b65101"
TWILIO_AUTH = "57323d684cde0d16cff7aef800093a71"
TWILIO_NUMBER = "+17439027480"

client = Groq(api_key=GROQ_API_KEY)

# === FUNCTIONS ===
def generate_excuse(prompt, language):
    translation_prompt = f"Give a creative excuse for: {prompt}. Reply in {language}."
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": translation_prompt}],
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

def speak_excuse(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)
    tts.save("excuse.mp3")
    return "excuse.mp3"

def generate_pdf(excuse):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(0, 10, f"Excuse Document\n\nGenerated Excuse:\n\n{excuse}")
    filename = f"excuse_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

def send_sms(to_number, message):
    twilio_client = Client(TWILIO_SID, TWILIO_AUTH)
    msg = twilio_client.messages.create(
        body=message,
        from_=TWILIO_NUMBER,
        to=to_number
    )
    return msg.sid

# === STREAMLIT UI ===
st.set_page_config(page_title="Rutwik’s Official Excuse Generator AI")
st.title("🤖 Rutwik’s Official Excuse Generator AI")
st.markdown("Create **believable excuses**, read them aloud, generate fake documents, and even send them by **SMS**!")

prompt = st.text_input("👉 What do you need an excuse for?")
language = st.selectbox("🌐 Choose Language", ["English", "Hindi", "Telugu", "Spanish", "French"])
lang_code = {"English": "en", "Hindi": "hi", "Telugu": "te", "Spanish": "es", "French": "fr"}[language]

if st.button("Generate Excuse"):
    if prompt.strip():
        excuse = generate_excuse(prompt, language)
        st.success(excuse)

        # 🔊 Text-to-Speech
        audio_path = speak_excuse(excuse, lang_code)
        st.audio(audio_path)

        # 📄 PDF Download
        pdf_path = generate_pdf(excuse)
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Download Fake Proof PDF", f, file_name=pdf_path)

        # 📱 Optional SMS
        with st.expander("📱 Send via SMS"):
            phone = st.text_input("Enter phone number with country code")
            if st.button("Send SMS"):
                try:
                    sid = send_sms(phone, excuse)
                    st.success(f"✅ SMS sent (SID: {sid})")
                except Exception as e:
                    st.error(f"❌ Failed to send SMS: {e}")
    else:
        st.warning("Please enter a prompt.")
