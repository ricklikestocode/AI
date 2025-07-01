import streamlit as st
import sqlite3
import datetime
from gtts import gTTS
from fpdf import FPDF
from twilio.rest import Client
from groq import Groq

# Twilio credentials
TWILIO_SID = "AC9fa1820b07d74e923f320ec1c7b65101"
TWILIO_AUTH = "5dfa97702492d2de2985293782814a0d"
TWILIO_NUMBER = "+17439027480"

client = Client()
groq_client = Groq(api_key="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")

conn = sqlite3.connect("history.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS excuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt TEXT,
    excuse TEXT,
    timestamp TEXT
)""")
conn.commit()

def generate_excuse(prompt, lang="en"):
    chat_completion = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a clever excuse generator. Generate funny or believable excuses based on the given prompt."},
            {"role": "user", "content": f"Give me a few creative excuses for: {prompt}"}
        ],
        temperature=0.9
    )
    return chat_completion.choices[0].message.content.strip()

def save_history(prompt, excuse):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO excuses (prompt, excuse, timestamp) VALUES (?, ?, ?)", (prompt, excuse, timestamp))
    conn.commit()

def generate_pdf(excuse):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(190, 10, excuse)
    filename = "excuse_proof.pdf"
    pdf.output(filename)
    return filename

def text_to_speech(excuse, lang='en'):
    tts = gTTS(text=excuse, lang=lang)
    tts.save("excuse.mp3")
    return "excuse.mp3"

def send_sms(excuse, to_number):
    try:
        message = client.messages.create(
            body=excuse,
            from_=TWILIO_NUMBER,
            to=to_number
        )
        return True
    except Exception:
        return False

st.set_page_config(page_title="Rutwik's Excuse Generator", page_icon="🤖", layout="centered")

st.markdown("<h1 style='text-align: center;'>🤖 Rutwik’s Official Excuse Generator AI</h1>", unsafe_allow_html=True)

prompt = st.text_area("🌐 Enter your situation (in any language):", height=100)
lang = st.selectbox("🌍 Choose Language for Speech:", ["English", "Hindi", "Telugu", "French", "German"])
lang_codes = {"English": "en", "Hindi": "hi", "Telugu": "te", "French": "fr", "German": "de"}

if st.button("Generate Excuse"):
    if prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:
        excuse = generate_excuse(prompt, lang_codes[lang])
        save_history(prompt, excuse)
        st.markdown(f"### 🧠 Generated Excuse:\n{excuse}")

        # Speech
        mp3_file = text_to_speech(excuse, lang_codes[lang])
        st.audio(mp3_file)

        # PDF
        pdf_path = generate_pdf(excuse)
        with open(pdf_path, "rb") as f:
            st.download_button("🧾 Download Fake Proof PDF", f, file_name="proof.pdf")

        # SMS
        send_sms_option = st.checkbox("📩 Send as SMS?")
        if send_sms_option:
            phone = st.text_input("Enter recipient phone number (with +countrycode):")
            if st.button("📤 Send SMS"):
                if send_sms(excuse, phone):
                    st.success("SMS sent successfully!")
                else:
                    st.error("Failed to send SMS.")

        st.success("✅ All systems completed. You can use this again anytime!")

st.markdown("---")
st.markdown("### 📜 Excuse History")
rows = cursor.execute("SELECT * FROM excuses ORDER BY id DESC LIMIT 5").fetchall()
for row in rows:
    st.markdown(f"🕒 {row[3]}\n- ❓ Prompt: {row[1]}\n- 💬 Excuse: {row[2]}")
