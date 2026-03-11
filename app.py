import streamlit as st
from gtts import gTTS
from fpdf import FPDF
import qrcode
from PIL import Image
import pytesseract
from io import BytesIO

st.set_page_config(page_title="SmartConvert Pro", layout="wide")
st.title("🚀 SmartConvert Pro: All-in-One Digital Tool")

# --- SECTION 1: PHOTO SE TEXT NIKALNA (New Feature) ---
st.header("📸 Photo se Notes/PDF Banao")
uploaded_file = st.file_uploader("Wife ke Sociology notes ya kisi bhi page ki photo upload karo", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Photo', width=300)
    if st.button("Extract Text from Photo"):
        extracted_text = pytesseract.image_to_string(img)
        st.subheader("Extracted Text:")
        st.text_area("Yahan se copy karein:", extracted_text, height=150)

st.markdown("---")

# --- SECTION 2: MANUAL TEXT TO AUDIO/PDF/QR (Purane Features) ---
st.header("✍️ Text to Audio, PDF & QR")
user_input = st.text_area("Yahan apna content likho ya upar se copy karke paste karo:", placeholder="Kunal AI Studio Punjab...")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎙️ Audio (MP3)"):
        if user_input:
            tts = gTTS(text=user_input, lang='hi')
            tts.save("voice.mp3")
            st.audio("voice.mp3")

with col2:
    if st.button("📄 Document (PDF)"):
        if user_input:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=user_input.encode('latin-1', 'ignore').decode('latin-1'))
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            st.download_button("Download PDF", data=pdf_bytes, file_name="kunal_notes.pdf")

with col3:
    if st.button("🏁 QR Code"):
        if user_input:
            qr = qrcode.make(user_input)
            buf = BytesIO()
            qr.save(buf)
            st.image(buf)
            st.download_button("Download QR", data=buf.getvalue(), file_name="my_qr.png")

st.markdown("---")
st.write("🛠️ **Special for Firozpur Students:** Photo kheencho aur notes suno!")
