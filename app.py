import streamlit as st
import sqlite3
import datetime
from groq import Groq
from gtts import gTTS
from fpdf import FPDF
from twilio.rest import Client
import os
import uuid

client = Groq(api_key="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")

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

def generate_excuse(prompt, lang="en"):
    chat_completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": f"You are a multilingual excuse generator AI. Respond only with creative, short, sharp, and believable excuses. No repetition. Respond in the user's language ({lang})."
            },
            {
                "role": "user",
                "content": f"Give a few creative excuses for: {prompt}"
            }
        ],
        temperature=1
    )
    return chat_completion.choices[0].message.content.strip()

def speak_excuse(excuse):
    audio = gTTS(text=excuse, lang="en")
    audio_path = f"excuse_{uuid.uuid4().hex}.mp3"
    audio.save(audio_path)
    return audio_path

def generate_pdf(excuse):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(0, 10, f"📄 OFFICIAL EXCUSE DOCUMENT\n\nExcuse:\n{excuse}")
    pdf_path = f"excuse_{uuid.uuid4().hex}.pdf"
    pdf.output(pdf_path)
    return pdf_path

def send_sms(excuse):
    twilio_sid = "AC9fa1820b07d74e923f320ec1c7b65101"
    twilio_auth = "5dfa97702492d2de2985293782814a0d"
    twilio_number = "+17439027480"
    to_number = st.text_input("📱 Enter phone number to send SMS", max_chars=15)

    if st.button("📤 Send SMS"):
        try:
            client = Client(twilio_sid, twilio_auth)
            client.messages.create(
                body=f"AI Excuse: {excuse}",
                from_=twilio_number,
                to=to_number
            )
            st.success("✅ SMS sent successfully!")
        except Exception as e:
            st.error(f"❌ Error sending SMS: {e}")

st.set_page_config(page_title="Rutwik's Official Excuse Generator AI", page_icon="😎", layout="centered")

st.markdown(
    """
    <style>
    body {
        background-color: #0d1117;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #9147ff;
        color: white;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image("86df66f1-0acc-43c6-a3ec-bfb48aa02cf8.png", width=100)
st.title("🤖 Rutwik’s Official Excuse Generator AI")

prompt = st.text_area("🌐 Enter your situation (in any language):", height=100)

if st.button("🎭 Generate Excuse"):
    if prompt.strip():
        excuse = generate_excuse(prompt)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO excuses (prompt, excuse, timestamp) VALUES (?, ?, ?)", (prompt, excuse, timestamp))
        conn.commit()

        st.subheader("🧠 Generated Excuse")
        st.success(excuse)

        st.audio(speak_excuse(excuse))
        pdf_path = generate_pdf(excuse)
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Download Fake Proof PDF", f, file_name="excuse.pdf")

        send_sms(excuse)
        st.balloons()
        st.info("✅ Process completed successfully. Please use this wisely.")
    else:
        st.warning("Please enter a valid situation.")

st.markdown("### 🕓 Excuse History")
cursor.execute("SELECT * FROM excuses ORDER BY timestamp DESC LIMIT 10")
history = cursor.fetchall()
for row in history:
    st.markdown(f"🕒 `{row[3]}`\n- ❓ Prompt: `{row[1]}`\n- 💬 Excuse: _\"{row[2]}\"_")

