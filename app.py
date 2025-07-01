from groq import Groq
from gtts import gTTS
from fpdf import FPDF
from twilio.rest import Client
import re
import os
import streamlit as st

groq_api_key = "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"
twilio_sid = "AC9fa1820b07d74e923f320ec1c7b65101"
twilio_token = "57323d684cde0d16cff7aef800093a71"
twilio_number = "+17439027480"

client = Groq(api_key=groq_api_key)

def generate_excuse(prompt, lang="en"):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You're a helpful AI that gives creative excuses."},
            {"role": "user", "content": f"Give me a few creative excuses for: {prompt}"}
        ],
        model="llama3-8b-8192",
        temperature=0.9
    )
    return chat_completion.choices[0].message.content.strip()

def speak_text(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    tts.save("excuse.mp3")
    os.system("start excuse.mp3" if os.name == "nt" else "mpg123 excuse.mp3")

def generate_pdf(text, filename="excuse_proof.pdf"):
    safe_text = re.sub(r'[^\x00-\x7F]+', '', text)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, safe_text)
    pdf.output(filename)
    return filename

def send_sms(body, to_number):
    client = Client(twilio_sid, twilio_token)
    message = client.messages.create(
        body=body,
        from_=twilio_number,
        to=to_number
    )
    return message.sid

st.set_page_config(page_title="Rutwik’s Official Excuse Generator AI")
st.title("🤖 Rutwik’s Official Excuse Generator AI")
st.write("Create believable excuses, read them aloud, generate fake documents, and even send them by SMS!")

prompt = st.text_input("👉 What do you need an excuse for?")
language = st.selectbox("🌐 Choose Language", ["English", "Hindi", "Telugu"])
speak = st.checkbox("🔊 Read Aloud")
make_pdf = st.checkbox("🧾 Generate Fake Proof PDF")
send = st.checkbox("📨 Send via SMS")

if st.button("Generate Excuse") and prompt:
    lang_map = {"English": "en", "Hindi": "hi", "Telugu": "te"}
    lang_code = lang_map.get(language, "en")
    excuse = generate_excuse(prompt, lang=lang_code)
    st.markdown(f"### 🤯 Your Excuse:\n{excuse}")
    
    if speak:
        speak_text(excuse, lang=lang_code)
    if make_pdf:
        pdf_path = generate_pdf(excuse)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download Fake Proof", f, file_name="excuse_proof.pdf")
    if send:
        to_number = st.text_input("📱 Enter recipient phone number (e.g., +91...)")
        if to_number and st.button("Send SMS"):
            sid = send_sms(excuse, to_number)
            st.success(f"Sent via Twilio. SID: {sid}")
