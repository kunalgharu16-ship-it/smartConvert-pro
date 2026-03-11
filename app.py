import streamlit as st
from gtts import gTTS
from fpdf import FPDF
import qrcode
from PIL import Image
import pytesseract
import io
import base64
from googletrans import Translator

# Page Setup for Global Reach
st.set_page_config(page_title="SmartConvert Global | Free AI Tool", layout="wide")
translator = Translator()

st.title("🌍 SmartConvert Global: All-in-One AI Utility")
st.write("Convert, Translate, and Generate — Free for Everyone, Everywhere.")

# --- LANGUAGE SELECTOR FOR GLOBAL USERS ---
st.sidebar.header("🌐 Select Language")
lang_opt = st.sidebar.selectbox("Choose your language", ["English", "Hindi", "Punjabi", "Spanish", "French", "Arabic", "German"])
lang_codes = {"English": "en", "Hindi": "hi", "Punjabi": "pa", "Spanish": "es", "French": "fr", "Arabic": "ar", "German": "de"}
target_lang = lang_codes[lang_opt]

if 'final_text' not in st.session_state:
    st.session_state['final_text'] = ""

# --- SECTION 1: PHOTO TO TEXT (OCR) ---
st.header("📸 Image to Text (OCR)")
uploaded_file = st.file_uploader("Upload any document image", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, width=250)
    if st.button("Extract & Translate"):
        try:
            extracted = pytesseract.image_to_string(img)
            # Global Translation Logic
            translated = translator.translate(extracted, dest=target_lang).text
            st.session_state['final_text'] = translated
            st.success(f"Success! Translated to {lang_opt}")
        except:
            st.error("Engine busy. Please ensure 'packages.txt' is active.")

st.markdown("---")

# --- SECTION 2: MULTI-TOOLS ---
st.header("🛠️ Digital Tools Hub")
user_text = st.text_area("Your Content:", value=st.session_state['final_text'], height=150)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🎙️ Audio (Global Voice)")
    if st.button("Generate MP3"):
        if user_text:
            tts = gTTS(text=user_text, lang=target_lang)
            audio_io = io.BytesIO()
            tts.write_to_fp(audio_io)
            b64 = base64.b64encode(audio_io.getvalue()).decode()
            st.markdown(f'<audio controls><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
            st.download_button("📥 Download Audio", data=audio_io.getvalue(), file_name="global_audio.mp3")

with col2:
    st.subheader("📄 Smart PDF")
    if st.button("Create PDF"):
        if user_text:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=user_text.encode('latin-1', 'ignore').decode('latin-1'))
            st.download_button("📥 Download PDF", data=pdf.output(dest='S').encode('latin-1'), file_name="smart_notes.pdf")

with col3:
    st.subheader("🏁 QR Master")
    if st.button("Create QR"):
        if user_text:
            qr = qrcode.make(user_text)
            q_io = io.BytesIO()
            qr.save(q_io)
            st.image(q_io, width=150)

# --- EARNINGS & AD-SENSE COMPLIANCE ---
st.markdown("---")
col_f1, col_f2 = st.columns(2)
with col_f1:
    if st.button("⚖️ Privacy Policy"):
        st.info("We do not store your data. All conversions happen in real-time.")
with col_f2:
    if st.button("📩 Contact Support"):
        st.info("Email: kunalgharu16@gmail.com")

st.caption("© 2026 SmartConvert Global | Fast. Free. Secure.")
