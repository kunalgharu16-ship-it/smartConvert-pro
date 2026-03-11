import streamlit as st
from gtts import gTTS
from fpdf import FPDF
import qrcode
from PIL import Image
import pytesseract
from io import BytesIO
import time

# Page Layout & Style
st.set_page_config(page_title="SmartConvert Pro | AI Tools", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("💰 SmartConvert Pro: Your Digital Earnings Hub")
st.write("Convert Photos, Text, and Audio instantly.")

# --- SECTION 1: PHOTO TO TEXT (The Money Maker) ---
with st.expander("📸 Photo to Text / PDF Converter", expanded=True):
    uploaded_file = st.file_uploader("Upload Image (Notes, Books, Bills)", type=['jpg', 'jpeg', 'png'])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, width=250)
        if st.button("Start Extraction"):
            with st.spinner('AI is reading the image... Please wait.'):
                time.sleep(2) # User ko rokne ke liye (For future Ads)
                text = pytesseract.image_to_string(img)
                st.session_state['extracted'] = text
                st.success("Extraction Complete!")
                st.text_area("Result:", text, height=150)

st.markdown("---")

# --- SECTION 2: UTILITY TOOLS ---
col1, col2 = st.columns(2)

with col1:
    st.header("🎙️ Text to Audio")
    txt_input = st.text_area("Enter text for Audio:", key="audio_in")
    if st.button("Generate MP3"):
        if txt_input:
            tts = gTTS(text=txt_input, lang='hi')
            tts.save("voice.mp3")
            st.audio("voice.mp3")

with col2:
    st.header("🏁 QR Generator")
    qr_input = st.text_input("Enter URL or Text for QR:", key="qr_in")
    if st.button("Generate QR"):
        if qr_input:
            qr = qrcode.make(qr_input)
            buf = BytesIO()
            qr.save(buf)
            st.image(buf, width=200)

# --- FOOTER (Trust Building) ---
st.markdown("---")
st.markdown("<p style='text-align: center;'>© 2026 SmartConvert Pro | For Support: kunalgharu16@gmail.com</p>", unsafe_allow_html=True)
