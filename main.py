import os
import asyncio
from flask import Flask, render_template, request
from docx import Document
from pydub import AudioSegment
from pydub.effects import speedup
import edge_tts

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FILE = "static/output.mp3"
DEFAULT_MUSIC = "static/music/background.mp3"
MAX_LENGTH = 10000

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 语音映射，包括粤语语音（zh-HK）
VOICE_MAP = {
    "zh_female": "zh-CN-XiaoxiaoNeural",
    "zh_male": "zh-CN-YunxiNeural",
    "zh-hk_female": "zh-HK-HiuMaanNeural",   # 粤语女声
    "zh-hk_male": "zh-HK-WanLungNeural",     # 粤语男声
    "en_female": "en-US-AriaNeural",
    "en_male": "en-US-GuyNeural",
    "ja_female": "ja-JP-NanamiNeural",
    "ja_male": "ja-JP-KeitaNeural",
    "fr_female": "fr-FR-DeniseNeural",
    "fr_male": "fr-FR-HenriNeural"
}

def extract_text(filepath):
    if filepath.endswith(".txt"):
        try:
            with open(filepath, encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(filepath, encoding="gbk", errors="ignore") as f:
                    return f.read()
            except Exception as e:
                print(f"读取 txt 文件失败: {e}")
                return ""
    elif filepath.endswith(".docx"):
        try:
            doc = Document(filepath)
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        except Exception as e:
            print(f"读取 docx 文件失败: {e}")
            return ""
    return ""

async def generate_speech(text, voice_id, out_path, speed):
    communicate = edge_tts.Communicate(
        text,
        voice=voice_id,
        rate=f"{float(speed) * 100 - 100:+.0f}%"
    )
    await communicate.save(out_path)

def mix_music(voice_path, music_path, speed, include_music, volume_adjust):
    if include_music and os.path.exists(music_path):
        voice = AudioSegment.from_file(voice_path)
        music = AudioSegment.from_file(music_path)
        music = music - int(volume_adjust)
        try:
            if float(speed) != 1.0:
                music = speedup(music, playback_speed=float(speed))
        except Exception as e:
            print(f"背景音乐加速失败：{e}")
        music = music[:len(voice)]
        combined = music.overlay(voice)
        combined.export(voice_path, format="mp3")

@app.route("/", methods=["GET", "POST"])
def index():
    download_link = None

    # 清理旧文件
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))

    if request.method == "POST":
        text = request.form.get("typed_text", "").strip()
        voice_key = request.form.get("voice_gender", "zh_female")
        music_on = request.form.get("music") == "on"
        music_speed = request.form.get("speed", "1.0")
        voice_speed = request.form.get("voice_speed", "1.0")
        music_volume = request.form.get("music_volume", "15")
        music_upload = request.files.get("bgmusicfile")

        # 如果没填文本，尝试读取上传的文件
        if not text:
            file = request.files.get("textfile")
            if file and file.filename:
                ext = file.filename.rsplit(".", 1)[-1].lower()
                input_path = os.path.join(UPLOAD_FOLDER, f"input.{ext}")
                file.save(input_path)
                text = extract_text(input_path)

        if not text:
            return render_template("index.html", error="⚠️ 请提供文本或上传文件。Please provide text or upload a file.", download_link=None)

        if len(text) > MAX_LENGTH:
            return render_template("index.html", error="⚠️ 文本过长，请限制在 10,000 字以内。Text too long.", download_link=None)

        # 根据 voice_key 获取实际语音 ID
        voice_id = VOICE_MAP.get(voice_key, "zh-CN-XiaoxiaoNeural")

        # 背景音乐路径
        bg_music_path = DEFAULT_MUSIC
        if music_upload and music_upload.filename:
            custom_path = os.path.join(UPLOAD_FOLDER, "custom_music.mp3")
            music_upload.save(custom_path)
            bg_music_path = custom_path

        # 生成语音 + 混音
        asyncio.run(generate_speech(text, voice_id, OUTPUT_FILE, voice_speed))
        mix_music(OUTPUT_FILE, bg_music_path, music_speed, music_on, music_volume)

        download_link = OUTPUT_FILE

    return render_template("index.html", download_link=download_link)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
