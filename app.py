import streamlit as st
from gtts import gTTS
from fpdf import FPDF
import qrcode
from PIL import Image
import pytesseract
import io

st.set_page_config(page_title="SmartConvert Pro", layout="wide")
st.title("🚀 SmartConvert Pro")

# --- PHOTO TO TEXT SECTION ---
st.header("📸 Photo to Text")
uploaded_file = st.file_uploader("Photo upload karo", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, width=250)
    if st.button("Extract Text"):
        try:
            # Check if tesseract is installed
            text = pytesseract.image_to_string(img)
            if text.strip():
                st.session_state['last_text'] = text
                st.success("Text mil gaya!")
                st.text_area("Extracted:", text, height=150)
            else:
                st.warning("Photo mein koi text nahi mila. Clear photo try karein.")
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Pehla kaam: GitHub pe 'packages.txt' banayein aur usme 'tesseract-ocr' likhein.")

st.markdown("---")

# --- TEXT TO AUDIO/PDF/QR ---
st.header("✍️ Audio, PDF & QR")
# Agar upar se text nikla hai toh wo apne aap yahan aa jaye
default_text = st.session_state.get('last_text', "")
user_input = st.text_area("Yahan text likhein:", value=default_text)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎙️ Audio"):
        if user_input:
            with st.spinner("Processing Audio..."):
                tts = gTTS(text=user_input, lang='hi')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                st.audio(fp, format='audio/mp3')
        else:
            st.warning("Pehle kuch likho!")

with col2:
    if st.button("📄 PDF"):
        if user_input:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=user_input.encode('latin-1', 'ignore').decode('latin-1'))
            st.download_button("Download PDF", data=pdf.output(dest='S').encode('latin-1'), file_name="notes.pdf")

with col3:
    if st.button("🏁 QR Code"):
        if user_input:
            qr = qrcode.make(user_input)
            buf = io.BytesIO()
            qr.save(buf)
            st.image(buf)

st.write("---")
st.caption("Developed by Kunal | Firozpur")
