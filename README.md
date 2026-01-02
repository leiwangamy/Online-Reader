# 🗣️ Online Reader | 文本转语音工具

A web-based Text-to-Speech (TTS) app using Edge-TTS, allowing users to convert typed or uploaded text into natural-sounding speech with optional background music.

---

## 📁 Project Structure

- 📂 **static/** – Background music and output MP3  
- 📂 **templates/** – HTML templates (`index.html`)  
- 📂 **uploads/** – Uploaded user files  
- 📄 **main.py** – Flask app and audio processing logic  
- 📄 **requirements.txt** – Python package list  
- 📄 **README.md** – This file  


---

## 🛠️ Technologies Used

- Python + Flask  
- Edge-TTS (Microsoft Text-to-Speech)  
- HTML + CSS  
- JavaScript (live character counter)  
- Replit (deployment)  
- GitHub (version control)

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Local Development Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd "C:\Users\Lei\Documents\VS Code Projects\Online-Reader"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   **Windows (PowerShell):**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   **Windows (Command Prompt):**
   ```cmd
   venv\Scripts\activate.bat
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Access the website**
   - Open your browser and go to: http://localhost:8080

### Note
The virtual environment (`venv/`) is already included in `.gitignore` and won't be committed to version control.

---

## 🚀 How to Use

1. Type or paste your text (max 10,000 characters)  
2. (Optional) Upload a `.txt` or `.docx` file  
3. (Optional) Upload background music (`.mp3`, under 5MB)  
4. Set voice gender, speech speed, and music volume  
5. Click **Generate**  
6. Play or download the resulting `.mp3` audio

🔗 Live Demo: [online-reader-leiwangamy.replit.app](https://online-reader-leiwangamy.replit.app)

---

## ⚠️ Recommendations

- 📝 **Text input**: ≤ 10,000 characters (~5 minutes of speech)  
- 🎵 **Music file**: ≤ 5MB and under 5 minutes  
- ✅ Best viewed on desktop or mobile in Chrome/Edge

---

## 👤 Author

Built by **Lei Wang** with help from OpenAI ChatGPT.  
Created to practice Python, Flask, and practical web development with real audio generation tools.

---

## 📜 License

MIT License – Free to use, modify, and share.
