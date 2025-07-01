import streamlit as st
import os
import tempfile
from groq import Groq
from gtts import gTTS
from fpdf import FPDF
from twilio.rest import Client

st.set_page_config(page_title="Rutwik’s Official Excuse Generator AI", page_icon="🤖")

client = Groq(api_key="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")

TWILIO_SID = "AC9fa1820b07d74e923f320ec1c7b65101"
TWILIO_AUTH = "5dfa97702492d2de2985293782814a0d"
TWILIO_NUM = "+17439027480"

def generate_excuse(prompt, lang="en"):
    messages = [
        {"role": "system", "content": "You generate short, creative, and believable excuses. Respond in the selected language."},
        {"role": "user", "content": f"Give a creative and believable excuse for: {prompt}"}
    ]
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

def speak_text(text, lang='en'):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts = gTTS(text=text, lang=lang)
        tts.save(fp.name)
        return fp.name

def generate_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Official Excuse Document", ln=True, align="C")
    pdf.multi_cell(0, 10, txt=text)
    pdf_path = os.path.join(tempfile.gettempdir(), "excuse_proof.pdf")
    pdf.output(pdf_path)
    return pdf_path

def send_sms(to_number, message):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH)
        sms = client.messages.create(
            body=message,
            from_=TWILIO_NUM,
            to=to_number
        )
        return True, f"✅ SMS sent! SID: {sms.sid}"
    except Exception as e:
        return False, f"❌ SMS failed: {e}"

st.title("🤖 Rutwik’s Official Excuse Generator AI")
st.markdown("Create believable excuses, read them aloud, generate fake documents, and even send them by SMS!")

with st.form("excuse_form"):
    prompt = st.text_input("👉 What do you need an excuse for?")
    lang = st.selectbox("🌐 Choose Language", ["English", "Hindi", "Telugu", "Spanish", "French"])
    phone_number = st.text_input("📲 Optional: Enter phone number to send excuse via SMS")
    submitted = st.form_submit_button("🎯 Generate Excuse")

if submitted and prompt:
    lang_code = {
        "English": "en", "Hindi": "hi", "Telugu": "te", "Spanish": "es", "French": "fr"
    }[lang]

    excuse = generate_excuse(prompt, lang_code)
    st.markdown("### ✨ Your Excuse:")
    st.write(excuse)

    audio_file = speak_text(excuse, lang=lang_code)
    st.audio(audio_file, format="audio/mp3")

    pdf_path = generate_pdf(excuse)
    with open(pdf_path, "rb") as f:
        st.download_button("📄 Download Fake PDF", f, file_name="excuse_proof.pdf")

    if phone_number:
        success, msg = send_sms(phone_number, excuse)
        st.success(msg) if success else st.error(msg)

    st.success("🎉 Done! You can use the app again anytime.")
