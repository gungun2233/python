import streamlit as st
import googletrans
from googletrans import Translator
from gtts import gTTS
import os

# Set up the translator
translator = Translator()

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
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
    .input-area, .output-area {
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        width: 100%;
    }
    .stTextArea>div>div>textarea {
        width: 100%;
        border-radius: 10px;
        padding: 10px;
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
    .key-features {
        color: #1d2671;
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .feature-item {
        color: #007bff;
        font-size: 20px;
        font-weight: bold;
        padding: 10px 0;
    }
    .feature-description {
        color: #333;
        font-size: 16px;
        padding: 5px 0;
        margin-left: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Full-width title with gradient, bold text, and emoji
st.markdown('<div class="full-width-element"><div class="full-width-title"> Army Public School Agra - Language Translator 🌐 </div></div>', unsafe_allow_html=True)

# Input area for text
st.markdown('<div class="full-width-element"><div class="input-area">', unsafe_allow_html=True)
text_input = st.text_area("Enter the text you want to translate:", key="input_text", height=150)
st.markdown('</div></div>', unsafe_allow_html=True)

# Language Detection Feature
detected_lang = None
if text_input:
    detected_lang = translator.detect(text_input).lang
    st.write(f"Detected language: {googletrans.LANGUAGES[detected_lang]}")

# Multi-Language Translation Feature
selected_langs = st.multiselect("Select multiple target languages:", list(googletrans.LANGUAGES.values()))

# Reverse mapping from full language names to language codes
lang_name_to_code = {v: k for k, v in googletrans.LANGUAGES.items()}

# Initialize session state for translation storage
if 'last_translated_text' not in st.session_state:
    st.session_state['last_translated_text'] = None

# Translation button
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button("Translate"):
    if text_input:
        all_translations = []  # To store all translations
        for lang in selected_langs:
            # Get the language code from the selected language name
            lang_code = lang_name_to_code.get(lang)
            if lang_code:
                translated = translator.translate(text_input, dest=lang_code)
                st.session_state['last_translated_text'] = translated.text  # Store the last translation in session state
                all_translations.append(translated.text)  # Save translations to list
                st.markdown('<div class="full-width-element"><div class="output-area">', unsafe_allow_html=True)
                st.subheader(f"Translated Text ({lang}):")
                st.write(translated.text)
                st.markdown('</div></div>', unsafe_allow_html=True)
    else:
        st.warning("Please enter some text to translate.")
st.markdown('</div>', unsafe_allow_html=True)

# Text-to-Speech (TTS) Feature
if st.session_state['last_translated_text']:  # Only enable TTS if text has been translated
    if st.button("Play Translated Text"):
        # Use the stored translation for TTS
        tts = gTTS(st.session_state['last_translated_text'], lang=detected_lang)
        tts.save("translated_speech.mp3")
        st.audio("translated_speech.mp3")
else:
    st.warning("Please translate the text first before playing it.")

# Key Features Section with Colors
st.markdown("""
<div class="key-features">🌟 Key Features of the Translator 🌟</div>

<div class="feature-item">1. **Language Detection**:</div>
<div class="feature-description">Automatically detects the input language for a smoother translation process.</div>

<div class="feature-item">2. **Multi-Language Translation**:</div>
<div class="feature-description">Translate text into multiple languages simultaneously with ease.</div>

<div class="feature-item">3. **Text-to-Speech (TTS)**:</div>
<div class="feature-description">Converts the translated text into speech, making the tool interactive and engaging.</div>

<div class="feature-item">4. **Custom UI Design**:</div>
<div class="feature-description">Sleek and responsive interface with a gradient title bar and full-width elements for a modern look.</div>

<div class="feature-item">5. **Detects and Shows Language Code**:</div>
<div class="feature-description">Detects the language of input text and shows the detected language before translation.</div>
""", unsafe_allow_html=True)
