import streamlit as st
import sqlite3
import datetime
from groq import Groq
from gtts import gTTS
from fpdf import FPDF
from twilio.rest import Client
import os

# Initialize Groq client
groq_api_key = "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"
client = Groq(api_key=groq_api_key)

# Initialize SQLite
conn = sqlite3.connect("history.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS excuses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt TEXT,
        excuse TEXT,
        timestamp TEXT
    )
""")
conn.commit()

# Title
st.set_page_config(page_title="Rutwik's Official Excuse Generator AI", layout="centered", initial_sidebar_state="collapsed")
st.title("😁 Rutwik's Official Excuse Generator AI")

# Input Prompt
st.markdown("### 🌐 Enter your situation (in any language):")
prompt = st.text_area(" ", placeholder="e.g., I skipped school today", height=120, label_visibility="collapsed")

# Main Generation Function
def generate_excuse(prompt):
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are an excuse generator. Give short, believable, creative excuses."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

# Save to history
def save_to_db(prompt, excuse):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO excuses (prompt, excuse, timestamp) VALUES (?, ?, ?)", (prompt, excuse, timestamp))
    conn.commit()

# PDF Generator
def generate_pdf_proof(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(0, 10, txt=f"Official Excuse Document:\n\n{text}")
    filename = "excuse_proof.pdf"
    pdf.output(filename)
    return filename

# SMS Sender
def send_sms(number, text):
    account_sid = "AC9fa1820b07d74e923f320ec1c7b65101"
    auth_token = "57323d684cde0d16cff7aef800093a71"
    twilio_number = "+17439027480"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Your excuse: {text}",
        from_=twilio_number,
        to=number
    )
    return message.sid

# Trigger generation
excuse = None
if st.button("🎯 Generate Excuse"):
    if prompt.strip():
        excuse = generate_excuse(prompt)
        save_to_db(prompt, excuse)
    else:
        st.warning("Please enter a situation!")

# Display results
if excuse:
    st.markdown("### 💬 Your AI-generated Excuse:")
    st.success(excuse)

    # PDF
    if st.button("📄 Generate Fake Proof PDF"):
        file = generate_pdf_proof(excuse)
        with open(file, "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name="excuse_proof.pdf")

    # gTTS
    if st.button("🔊 Speak the Excuse"):
        tts = gTTS(text=excuse, lang="en")
        tts.save("excuse.mp3")
        audio_file = open("excuse.mp3", "rb").read()
        st.audio(audio_file, format="audio/mp3")

    # SMS
    phone = st.text_input("📱 Enter phone number with country code:")
    if st.button("📤 Send Excuse via SMS"):
        if phone.strip():
            try:
                sid = send_sms(phone.strip(), excuse)
                st.success("Excuse sent via SMS!")
            except Exception as e:
                st.error(f"SMS Error: {e}")
        else:
            st.warning("Please enter a valid phone number.")

# Excuse History
st.markdown("### 🧾 Excuse History")
cursor.execute("SELECT * FROM excuses ORDER BY timestamp DESC LIMIT 10")
rows = cursor.fetchall()
for row in rows:
    st.markdown(f"🕒 **{row[3]}**")
    st.markdown(f"❓ **Prompt:** {row[1]}")
    st.markdown(f"💭 **Excuse:** {row[2]}")
    st.markdown("---")
