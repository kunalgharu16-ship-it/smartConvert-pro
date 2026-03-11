import streamlit as st
from gtts import gTTS
from fpdf import FPDF
import qrcode
from PIL import Image
import pytesseract
import io

# Page Title & Layout
st.set_page_config(page_title="SmartConvert Pro | Kunal Studio", layout="wide")

st.title("🚀 SmartConvert Pro")
st.write("Convert Photos to Text, PDF, Audio, and QR Codes instantly.")

# --- SECTION 1: PHOTO TO TEXT ---
st.header("📸 Step 1: Photo se Text Nikalo")
uploaded_file = st.file_uploader("Sociology notes ya koi bhi photo upload karo", type=['jpg', 'jpeg', 'png'])

# Session state to store text across interactions
if 'final_text' not in st.session_state:
    st.session_state['final_text'] = ""

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, width=300, caption="Aapki Photo")
    
    if st.button("Extract Text from Photo"):
        with st.spinner("AI photo padh raha hai..."):
            try:
                extracted = pytesseract.image_to_string(img)
                if extracted.strip():
                    st.session_state['final_text'] = extracted
                    st.success("Text mil gaya! Neeche dekhiye.")
                else:
                    st.warning("Photo saaf nahi hai ya text nahi mila.")
            except Exception as e:
                st.error(f"Error: {e}. Make sure 'packages.txt' is added.")

st.markdown("---")

# --- SECTION 2: TEXT MANIPULATION ---
st.header("✍️ Step 2: Audio, PDF ya QR Banao")
# Input box jisme extracted text apne aap aa jayega
user_text = st.text_area("Yahan apna text edit karein:", value=st.session_state['final_text'], height=200)

col1, col2, col3 = st.columns(3)

# --- AUDIO SECTION ---
with col1:
    st.subheader("🎙️ Audio")
    if st.button("Generate Audio"):
        if user_text:
            try:
                tts = gTTS(text=user_text, lang='hi')
                audio_io = io.BytesIO()
                tts.write_to_fp(audio_io)
                audio_bytes = audio_io.getvalue()
                
                st.audio(audio_bytes, format='audio/mp3')
                st.download_button("📥 Download MP3", data=audio_bytes, file_name="kunal_audio.mp3")
            except Exception as e:
                st.error("Audio nahi ban paya.")
        else:
            st.info("Pehle text likho!")

# --- PDF SECTION ---
with col2:
    st.subheader("📄 PDF")
    if st.button("Generate PDF"):
        if user_text:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            # Encoding fix for special characters
            pdf.multi_cell(0, 10, txt=user_text.encode('latin-1', 'ignore').decode('latin-1'))
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            st.download_button("📥 Download PDF", data=pdf_bytes, file_name="notes.pdf")
        else:
            st.info("Pehle text likho!")

# --- QR SECTION ---
with col3:
    st.subheader("🏁 QR Code")
    if st.button("Generate QR"):
        if user_text:
            qr = qrcode.make(user_text)
            qr_io = io.BytesIO()
            qr.save(qr_io)
            st.image(qr_io, width=200)
            st.download_button("📥 Download QR", data=qr_io.getvalue(), file_name="my_qr.png")
        else:
            st.info("Pehle text likho!")

st.markdown("---")
st.caption("Developed by Kunal Gharu | Firozpur, Punjab")
