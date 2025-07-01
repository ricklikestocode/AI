import streamlit as st
from groq import Groq
from gtts import gTTS
from fpdf import FPDF
from twilio.rest import Client
import datetime
import os
import base64

client = Groq(api_key="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")
twilio_sid = "AC9fa1820b07d74e923f320ec1c7b65101"
twilio_token = "5dfa97702492d2de2985293782814a0d"
twilio_number = "+17439027480"

history = []

st.set_page_config(page_title="Rutwik's Official Excuse Generator AI", page_icon="🤖", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    body {
        background-color: #121212;
    }
    .stApp {
        background: linear-gradient(to bottom right, #1f1f1f, #2c2c2c);
        color: #ffffff;
    }
    .title-logo {
        display: flex;
        align-items: center;
    }
    .logo-text {
        font-size: 2.2em;
        font-weight: 700;
        margin-left: 10px;
    }
    .logo-box {
        background-color: #ff6347;
        color: white;
        font-weight: 800;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 1.4em;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-logo">
    <div class="logo-box">RS</div>
    <div class="logo-text">Rutwik's Official Excuse Generator AI</div>
</div>
""", unsafe_allow_html=True)

st.write("\n")
prompt = st.text_area("🌐 Enter your situation (in any language):", height=150)
lang = st.selectbox("🌍 Choose Language for Excuse Audio", ["English", "Hindi", "Telugu", "Tamil", "Spanish"], index=0)

if st.button("Generate Excuse") and prompt:
    with st.spinner("Thinking hard... 🤔"):
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are an expert excuse generator. Always give very creative, believable, short and funny excuses."},
                {"role": "user", "content": f"Give 1 creative excuse for: {prompt}"},
            ],
            temperature=0.9,
        )
        excuse = response.choices[0].message.content.strip()
        history.append((prompt, excuse, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        st.markdown(f"### 🎯 Your Excuse:\n> {excuse}")

        # PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.multi_cell(0, 10, excuse)
        filename = "excuse.pdf"
        pdf.output(filename)
        with open(filename, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<a href="data:application/pdf;base64,{b64}" download="excuse.pdf">📄 Download Fake Proof PDF</a>', unsafe_allow_html=True)

        # Audio
        audio = gTTS(text=excuse, lang=lang[:2].lower())
        audio.save("excuse.mp3")
        st.audio("excuse.mp3")

        # SMS
        try:
            recipient = st.text_input("📱 Enter recipient phone number (E.g. +91XXXXXXXXXX):")
            if st.button("📤 Send via SMS"):
                sms_client = Client(twilio_sid, twilio_token)
                sms_client.messages.create(
                    body=f"ExcuseBot: {excuse}",
                    from_=twilio_number,
                    to=recipient
                )
                st.success("✅ SMS sent successfully!")
        except Exception as e:
            st.warning(f"⚠️ SMS failed: {e}")

        st.success("🎉 Done! Please use the excuse responsibly.")

if history:
    st.markdown("## 📜 Excuse History")
    for item in reversed(history):
        st.markdown(f"**🕒 {item[2]}**")
        st.markdown(f"❓ Prompt: {item[0]}")
        st.markdown(f"💬 Excuse: \"{item[1]}\"")
