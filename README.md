🤖 Rutwik's Official Excuse Generator AI
This is a terminal + Streamlit-powered AI excuse generator using Groq's API and LLaMA 3 model. It generates clever and believable excuses based on user prompts — in multiple languages — and logs all history locally.

✨ Features
💡 Prompt-first UI — waits for user input before generating

🌐 Multilingual Support — detects and handles inputs in various languages (placeholder ready for future translation)

🧠 LLaMA 3 via Groq API — fast and lightweight inference

📜 Local History Logging — saves all prompts and generated excuses in history.db

🖥️ Terminal Mode — lightweight CLI version

🌍 Streamlit Web App — user-friendly GUI with scrollable excuse history

📁 No heavy model download — everything runs via API (no training needed)

🚀 How to Run
🔧 1. Clone the Repo
bash
Copy
Edit
git clone https://github.com/ricklikestocode/excusegeneratorai.git
cd excusegeneratorai
🛠️ 2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
🔑 3. Add Groq API Key
Replace this line in app.py with your own Groq API key:

python
Copy
Edit
api_key = "gsk_xxx..."  # your Groq key here
💻 4. To Run in Terminal
bash
Copy
Edit
python app.py
🌐 5. To Run Streamlit App
bash
Copy
Edit
streamlit run app.py
🧾 History Logging
All interactions are logged in a local SQLite file:

sql
Copy
Edit
📁 history.db
  └── user_input
  └── generated_excuse
  └── timestamp
You can view or export it using any SQLite viewer or CLI.

📌 Future Ideas
🔄 Built-in language translation

📥 Download history as CSV

🎨 Better UI/UX styling

🔐 User authentication for shared access

📃 License
MIT License. Created with ❤️ by Rutwik

