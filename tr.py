import streamlit as st
import googletrans
from googletrans import Translator

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-col.input-area, .output-area {
       or: #f0f2f6;
    }
    .full-width-element {
        width: 100vw;
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
    }
    .full-width-title {
        font-weight: bold;
        font-size: 48px;
        color: white;
        text-align: center;
        padding: 30px 0;
        background: linear-gradient(90deg, #1d2671, #c33764);
        border-radius: 15px;
        margin: 0;
    }
     padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .full-width-.stTextArea>div>div>.full-width-textarea {
        width: 100%;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        font-size: 18px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        margin-top: 20px;
        transition: 0.3s;
        width: auto;
        display: inline-block;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .stSelectbox {
        margin-top: 15px;
    }
    .button-container {
        display: flex;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Full-width title with gradient, bold text, and emoji
st.markdown('<div class="full-width-element"><div class="full-width-title">Army Public School Agra - Language Translator 🌐</div></div>', unsafe_allow_html=True)

translator = Translator()

# Input area for text
st.markdown('<div class="full-width-element"><div class="input-area">', unsafe_allow_html=True)
text_input = st.text_area("Enter the text you want to translate:", key="input_text", height=150)
st.markdown('</div></div>', unsafe_allow_html=True)

# Language selection dropdown
target_lang = st.selectbox("Select the target language:", list(googletrans.LANGUAGES.values()))

# Translate button
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button("Translate"):
    if text_input:
        translated_text = translator.translate(text_input, dest=target_lang)
        
        # Output area for translation result
        st.markdown('<div class="full-width-element"><div class="output-area">', unsafe_allow_html=True)
        st.subheader("Translated Text:")
        st.write(translated_text.text)
        st.markdown('</div></div>', unsafe_allow_html=True)
    else:
        st.warning("Please enter some text to translate.")
st.markdown('</div>', unsafe_allow_html=True)