import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO

# =========================
# CẤU HÌNH
# =========================
st.set_page_config(
    page_title="Dịch Nhanh",
    page_icon="🌐",
    layout="centered"
)

# =========================
# CSS - GIAO DIỆN
# =========================
st.markdown("""
<style>
    .stApp {
        background: #f7f8fa;
    }

    .title {
        text-align: center;
        font-size: 32px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #777;
        margin-bottom: 25px;
    }

    .card {
        background: white;
        padding: 22px;
        border-radius: 22px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.07);
        margin-bottom: 18px;
    }

    .lang {
        text-align: center;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .result {
        background: #f1f3f5;
        padding: 20px;
        border-radius: 18px;
        font-size: 22px;
        min-height: 90px;
    }

    .mic-text {
        text-align: center;
        color: #777;
        margin-top: 5px;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 15px;
        height: 48px;
        font-size: 17px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# 4 CHẾ ĐỘ DỊCH
# =========================
MODES = {
    "🇻🇳 Việt → 🇬🇧 Anh": {
        "source": "vi",
        "target": "en",
        "source_name": "Tiếng Việt",
        "target_name": "English",
        "speech": "vi-VN",
        "tts": "en"
    },

    "🇻🇳 Việt → 🇨🇳 Trung": {
        "source": "vi",
        "target": "zh-CN",
        "source_name": "Tiếng Việt",
        "target_name": "中文",
        "speech": "vi-VN",
        "tts": "zh-CN"
    },

    "🇨🇳 Trung → 🇻🇳 Việt": {
        "source": "zh-CN",
        "target": "vi",
        "source_name": "中文",
        "target_name": "Tiếng Việt",
        "speech": "zh-CN",
        "tts": "vi"
    },

    "🇬🇧 Anh → 🇻🇳 Việt": {
        "source": "en",
        "target": "vi",
        "source_name": "English",
        "target_name": "Tiếng Việt",
        "speech": "en-US",
        "tts": "vi"
    }
}

# =========================
# HÀM NHẬN DẠNG GIỌNG NÓI
# =========================
def speech_to_text(audio_bytes, language):
    recognizer = sr.Recognizer()

    try:
        audio_file = BytesIO(audio_bytes)

        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(
            audio,
            language=language
        )

        return text

    except sr.UnknownValueError:
        return "❌ Không nghe rõ giọng nói."

    except sr.RequestError:
        return "❌ Không thể kết nối dịch vụ nhận dạng giọng nói."

    except Exception as e:
        return f"❌ Lỗi: {e}"


# =========================
# DỊCH
# =========================
def translate_text(text, source, target):
    try:
        translator = GoogleTranslator(
            source=source,
            target=target
        )

        return translator.translate(text)

    except Exception as e:
        return f"❌ Không thể dịch: {e}"


# =========================
# TEXT → GIỌNG NÓI
# =========================
def text_to_speech(text, language):
    try:
        audio = BytesIO()

        tts = gTTS(
            text=text,
            lang=language
        )

        tts.write_to_fp(audio)
        audio.seek(0)

        return audio

    except Exception:
        return None


# =========================
# GIAO DIỆN
# =========================

st.markdown(
    '<div class="title">🌐 DỊCH NHANH</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Nói → Dịch → Nghe</div>',
    unsafe_allow_html=True
)

# Chọn chế độ
mode = st.selectbox(
    "Chọn ngôn ngữ",
    list(MODES.keys())
)

config = MODES[mode]

# Ngôn ngữ
st.markdown(
    f"""
    <div class="card">
        <div class="lang">
            {config["source_name"]} &nbsp; → &nbsp; {config["target_name"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# MIC
# =========================

st.markdown(
    '<div class="mic-text">🎙️ Nhấn nút bên dưới và nói</div>',
    unsafe_allow_html=True
)

audio = st.audio_input(
    "🎙️ Nhấn để nói",
    sample_rate=16000
)

# =========================
# XỬ LÝ
# =========================

if audio:

    audio_bytes = audio.getvalue()

    with st.spinner("🎧 Đang nghe..."):

        original_text = speech_to_text(
            audio_bytes,
            config["speech"]
        )

    # Câu người dùng nói
    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown("### 🗣️ Bạn nói")

    st.markdown(
        f'<div class="result">{original_text}</div>',
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Nếu nhận dạng thành công
    if not original_text.startswith("❌"):

        with st.spinner("🌐 Đang dịch..."):

            translated = translate_text(
                original_text,
                config["source"],
                config["target"]
            )

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown("### 🔊 Bản dịch")

        st.markdown(
            f'<div class="result">{translated}</div>',
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # =========================
        # ĐỌC BẢN DỊCH
        # =========================

        if not translated.startswith("❌"):

            with st.spinner("🔊 Đang tạo giọng nói..."):

                speech_audio = text_to_speech(
                    translated,
                    config["tts"]
                )

            if speech_audio:

                st.audio(
                    speech_audio,
                    format="audio/mp3"
                )

                st.caption("🔊 Nhấn Play để nghe bản dịch")