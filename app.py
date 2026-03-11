import streamlit as st
from gtts import gTTS
from fpdf import FPDF
import qrcode
from io import BytesIO

st.set_page_config(page_title="SmartConvert Pro", layout="wide")
st.title("💰 SmartConvert Pro: All-in-One Digital Tool")

# Sidebar for Earning Info
st.sidebar.header("User Dashboard")
st.sidebar.success("Account Status: Active")
st.sidebar.write("Today's Users: 1 (Kunal)")

# Main Input
user_input = st.text_area("Yahan apna content dalo (Hindi/English/Punjabi):", placeholder="Example: Aaj ki taja khabar...")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎙️ Audio (MP3)"):
        tts = gTTS(text=user_input, lang='hi')
        tts.save("voice.mp3")
        st.audio("voice.mp3")

with col2:
    if st.button("📄 Document (PDF)"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=user_input)
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("Download PDF", data=pdf_bytes, file_name="kunal_notes.pdf")

with col3:
    if st.button("🏁 QR Code"):
        qr = qrcode.make(user_input)
        buf = BytesIO()
        qr.save(buf)
        st.image(buf)
        st.download_button("Download QR", data=buf.getvalue(), file_name="my_qr.png")

st.markdown("---")
st.write("📢 **Ad Space:** Your ad could be here! Contact: kunalgharu16@gmail.com")
