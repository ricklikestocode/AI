import streamlit as st
from groq import Groq
from gtts import gTTS
from fpdf import FPDF
from twilio.rest import Client
import os
import datetime
import tempfile

client = Groq(api_key="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")

st.set_page_config(
    page_title="Rutwik’s Official Excuse Generator AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🤖 Rutwik’s Official Excuse Generator AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>Create believable excuses, read them aloud, generate fake documents, and even send them by SMS!</p>",
    unsafe_allow_html=True
)

prompt = st.text_input("👉 What do you need an excuse for?")
lang = st.selectbox("🌐 Choose Language", ["English", "Hindi", "Telugu", "French", "Spanish"])

if prompt:
    with st.spinner("Generating excuse..."):
        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"Reply with 3 creative and believable excuses in {lang}."},
                {"role": "user", "content": f"{prompt}"}
            ]
        )
        excuse = chat_completion.choices[0].message.content.strip()
        st.success("Here are your excuses:")
        st.write(excuse)

        # --- Text to Speech ---
        tts = gTTS(excuse, lang='en')
        mp3_fp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(mp3_fp.name)
        st.audio(mp3_fp.name)

        # --- PDF Generator ---
        def generate_pdf(text):
            clean_text = text.encode("latin-1", "ignore").decode("latin-1")
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            pdf.multi_cell(190, 10, clean_text)
            pdf.output("proof.pdf")
            return "proof.pdf"

        pdf_path = generate_pdf(excuse)
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Download Proof PDF", f, file_name="proof.pdf")

        # --- Twilio SMS Sender ---
        def send_sms(excuse_text):
            try:
                twilio_sid = "AC9fa1820b07d74e923f320ec1c7b65101"
                twilio_auth = "5dfa97702492d2de2985293782814a0d"
                from_number = "+17439027480"

                to_number = st.text_input("📱 Enter your phone number (with +country code):", key="sms_input")

                if to_number and st.button("📩 Send SMS"):
                    client = Client(twilio_sid, twilio_auth)
                    client.messages.create(body=excuse_text, from_=from_number, to=to_number)
                    st.success("SMS sent successfully!")
            except Exception as e:
                st.error(f"SMS failed: {e}")

        send_sms(excuse)

        st.info("✅ Done! Feel free to use the app again anytime.")
