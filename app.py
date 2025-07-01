import streamlit as st
from groq import Groq
from gtts import gTTS
from fpdf import FPDF
from twilio.rest import Client
import os
import datetime
import base64

GROQ_API_KEY = "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"
TWILIO_SID = "AC9fa1820b07d74e923f320ec1c7b65101"
TWILIO_AUTH = "5dfa97702492d2de2985293782814a0d"
TWILIO_FROM = "+17439027480"

client = Groq(api_key=GROQ_API_KEY)
twilio_client = Client(TWILIO_SID, TWILIO_AUTH)

st.set_page_config(page_title="Rutwik's Official Excuse Generator AI", page_icon="🤖", layout="centered")
st.markdown("## 🤖 Rutwik's Official Excuse Generator AI")
st.markdown("Create believable excuses, read them aloud, generate fake documents, and even send them by SMS!")

history = []

def generate_excuse(prompt, lang="en"):
    chat = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": f"Give a few creative, funny, and believable excuses for: {prompt}. Keep it in {lang}"}],
        temperature=0.9
    )
    return chat.choices[0].message.content.strip()

def speak(text, lang):
    tts = gTTS(text=text, lang=lang)
    tts.save("excuse.mp3")
    audio_file = open("excuse.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")

def generate_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    fake_title = "Doctor's Note" if "sick" in text.lower() else "Official Document"
    pdf.cell(200, 10, txt=fake_title, ln=1, align="C")
    pdf.multi_cell(0, 10, txt=f"This is to certify that:\n\n{text}\n\nRegards,\nDr. Smith\nVerified Signature", align="L")
    filename = f"excuse_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    with open(filename, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">📄 Download Proof PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

def send_sms(excuse, to_number):
    try:
        twilio_client.messages.create(body=excuse, from_=TWILIO_FROM, to=to_number)
        st.success("📩 Excuse sent via SMS!")
    except Exception as e:
        st.error(f"SMS failed: {e}")

with st.form("excuse_form"):
    prompt = st.text_area("🌐 Enter your situation (in any language):", height=150)
    language = st.selectbox("🌍 Choose Language", ["English", "Hindi", "Telugu", "Spanish", "French"])
    phone = st.text_input("📱 Send SMS to (optional, include country code):")
    submit = st.form_submit_button("Generate Excuse")

if submit:
    if prompt.strip() == "":
        st.error("Please enter a prompt.")
    else:
        lang_code = {"English": "en", "Hindi": "hi", "Telugu": "te", "Spanish": "es", "French": "fr"}[language]
        excuse = generate_excuse(prompt, lang=lang_code)
        st.markdown("### 💡 Excuse")
        st.write(excuse)
        speak(excuse, lang_code)
        generate_pdf(excuse)
        if phone.strip():
            send_sms(excuse, phone)
        history.append((prompt, excuse, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

if history:
    st.markdown("### 📝 Excuse History")
    for item in reversed(history):
        st.markdown(f"🕒 {item[2]}")
        st.markdown(f"❓ Prompt: {item[0]}")
        st.markdown(f"💬 Excuse: {item[1]}")
