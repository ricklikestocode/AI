import os
import datetime
import sqlite3
from groq import Groq
from gtts import gTTS
from fpdf import FPDF
from twilio.rest import Client

# ==== CONFIGURATION ====
GROQ_API_KEY = "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"
GROQ_MODEL = "llama3-8b-8192"

TWILIO_SID = "AC9fa1820b07d74e923f320ec1c7b65101"
TWILIO_AUTH ="57323d684cde0d16cff7aef800093a71"
TWILIO_FROM = "+17439027480"  # Your Twilio phone number
TO_PHONE = "+917207431844"  # Replace with recipient number

FONT_PATH = "fonts/DejaVuSans.ttf"

# ==== INIT ====
client = Groq(api_key=GROQ_API_KEY)

# Create history DB
conn = sqlite3.connect("history.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input TEXT,
        excuse TEXT,
        timestamp TEXT
    )
""")
conn.commit()

# ==== CORE FUNCTIONS ====
def generate_excuse(prompt, lang="en"):
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "Generate a believable, short excuse. Avoid code or poetry."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

def speak_excuse(text, lang="en"):
    tts = gTTS(text, lang=lang)
    tts.save("excuse.mp3")
    os.system("start excuse.mp3" if os.name == 'nt' else "mpg123 excuse.mp3")

def generate_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.set_font("DejaVu", "", 14)
    pdf.multi_cell(0, 10, f"📝 Excuse Proof\n\n{text}")
    filename = f"excuse_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

def send_sms(text):
    try:
        twilio = Client(TWILIO_SID, TWILIO_AUTH)
        message = twilio.messages.create(
            body=text,
            from_=TWILIO_FROM,
            to=TO_PHONE
        )
        print("✅ SMS sent:", message.sid)
    except Exception as e:
        print("❌ SMS failed:", e)

def log_history(prompt, excuse):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO history (input, excuse, timestamp) VALUES (?, ?, ?)", (prompt, excuse, timestamp))
    conn.commit()

# ==== MAIN CHAT ====
def main():
    print("📘 Welcome to Rutwik's Official Excuse Generator AI")
    print("👉 What do you need an excuse for?")
    prompt = input("> ")

    print("🌐 Choose language (e.g., en, hi, te, fr): ")
    lang = input("> ").strip() or "en"

    print("⏳ Generating...")
    excuse = generate_excuse(prompt, lang)

    print("\n🧠 Excuse Generated:")
    print(f"👉 {excuse}")

    speak_excuse(excuse, lang)
    pdf_path = generate_pdf(excuse)
    print(f"📄 Proof PDF saved as: {pdf_path}")

    send_sms(excuse)
    log_history(prompt, excuse)

if __name__ == "__main__":
    main()
