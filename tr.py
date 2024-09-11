import streamlit as st
from googletrans import Translator

# Set page configuration
st.set_page_config(page_title="Army Public School Agra Translator", page_icon="🌐", layout="wide")

# Apply Google Fonts and Custom CSS for design
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        body { background-color: #f0f4f8; font-family: 'Poppins', sans-serif; }
        .title { font-family: 'Georgia', serif; color: #3498db; text-align: center; margin-bottom: 20px; font-size: 48px; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
        .school-name { font-size: 36px; color: #2ecc71; padding: 20px; border: 6px solid #3498db; border-radius: 15px; display: inline-block; margin: 0 auto; text-align: center; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); }
        .introduction { color: #34495e; font-size: 20px; text-align: center; margin-bottom: 20px; }
        .section-title { color: #3498db; font-size: 28px; margin-top: 20px; text-align: center; }
        .translation-area { margin-top: 20px; border: 1px solid #ccc; border-radius: 8px; padding: 20px; background-color: #ffffff; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .stButton > button { background-color: #3498db; color: white; border-radius: 5px; padding: 10px 20px; border: none; cursor: pointer; font-size: 16px; transition: background-color 0.3s; display: inline-block; }
        .stButton > button:hover { background-color: #2980b9; }
    </style>
    """, unsafe_allow_html=True)

# Page title with school name in a bordered and styled design
st.markdown("<h1 class='title'>🌐 Army Public School Agra Translator</h1>", unsafe_allow_html=True)
st.markdown("<div class='school-name'>Army Public School Agra</div>", unsafe_allow_html=True)

# Translator object
translator = Translator()

# Language options
languages = {
    'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de', 'Hindi': 'hi',
    'Chinese': 'zh-cn', 'Arabic': 'ar', 'Russian': 'ru', 'Japanese': 'ja', 'Korean': 'ko'
}

# User input section
st.markdown("<h2 class='section-title'>Enter Text to Translate</h2>", unsafe_allow_html=True)
input_text = st.text_area("Your text:", height=150)

st.markdown("<h2 class='section-title'>Select Target Language</h2>", unsafe_allow_html=True)
target_lang = st.selectbox("Choose language", list(languages.keys()))

# Translate button
if st.button("Translate"):
    if input_text.strip() != "":
        translated_text = translator.translate(input_text, dest=languages[target_lang])
        st.markdown(f"<div class='translation-area'><strong>Translated Text:</strong><br>{translated_text.text}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter text to translate.")

# Footer section
st.markdown("<p class='introduction'>This translation tool is created by Army Public School, Agra.</p>", unsafe_allow_html=True)
