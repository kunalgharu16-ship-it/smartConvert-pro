import streamlit as st
from gtts import gTTS
from fpdf import FPDF
import qrcode
from PIL import Image
import pytesseract
import io
import base64

# Page Config
st.set_page_config(page_title="SmartConvert Pro", layout="wide")

st.title("🚀 SmartConvert Pro")
st.write("Photo, Text, Audio aur PDF Tool")

if 'final_text' not in st.session_state:
    st.session_state['final_text'] = ""

# --- SECTION 1: PHOTO TO TEXT ---
st.header("📸 Photo se Text")
uploaded_file = st.file_uploader("Photo upload karo", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, width=250)
    if st.button("Extract Text"):
        try:
            extracted = pytesseract.image_to_string(img)
            st.session_state['final_text'] = extracted
            st.success("Text mil gaya!")
        except Exception as e:
            st.error("Engine Error. 'packages.txt' check karein.")

st.markdown("---")

# --- SECTION 2: TOOLS ---
st.header("✍️ Audio, PDF & QR")
user_text = st.text_area("Content:", value=st.session_state['final_text'], height=150)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🎙️ Audio")
    if st.button("Generate Audio"):
        if user_text:
            try:
                tts = gTTS(text=user_text, lang='hi')
                audio_io = io.BytesIO()
                tts.write_to_fp(audio_io)
                audio_bytes = audio_io.getvalue()
                
                # --- MOBILE AUDIO FIX (Base64) ---
                b64 = base64.b64encode(audio_bytes).decode()
                md = f"""
                    <audio controls autoplay>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                    """
                st.markdown(md, unsafe_allow_html=True)
                
                st.download_button("📥 Download MP3", data=audio_bytes, file_name="audio.mp3")
            except:
                st.error("Audio failed.")

with col2:
    st.subheader("📄 PDF")
    if st.button("Make PDF"):
        if user_text:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=user_text.encode('latin-1', 'ignore').decode('latin-1'))
            st.download_button("📥 Download PDF", data=pdf.output(dest='S').encode('latin-1'), file_name="notes.pdf")

with col3:
    st.subheader("🏁 QR")
    if st.button("Make QR"):
        if user_text:
            qr = qrcode.make(user_text)
            qio = io.BytesIO()
            qr.save(qio)
            st.image(qio, width=150)

st.write("---")
st.caption("Kunal Gharu | Firozpur")
