import streamlit as st
from gtts import gTTS
from fpdf import FPDF
import pytesseract
from PIL import Image
import io

st.set_page_config(page_title="SmartConvert Pro", layout="wide")
st.title("🚀 SmartConvert Pro: Image to PDF & Audio")

# Naya Feature: Image to Text/PDF
st.header("📸 Photo se Text/PDF Banao")
uploaded_file = st.file_uploader("Sociology notes ya kisi bhi page ki photo upload karo", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Photo', width=300)
    
    if st.button("Extract Text from Photo"):
        # Photo se text nikalna
        extracted_text = pytesseract.image_to_string(image)
        st.text_area("Nikala gaya Text:", extracted_text, height=200)
        
        # Option 1: PDF Banana
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=extracted_text.encode('latin-1', 'ignore').decode('latin-1'))
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button("📥 Download as PDF", data=pdf_output, file_name="kunal_notes.pdf")
        
        # Option 2: Audio Banana
        if st.button("🎙️ Is Text ki Audio Suno"):
            tts = gTTS(text=extracted_text, lang='hi')
            tts.save("extracted.mp3")
            st.audio("extracted.mp3")

st.markdown("---")
st.write("🛠️ **Special for Students:** Photo kheencho aur notes taiyar!")
