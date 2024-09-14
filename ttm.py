import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator

# Initialize recognizer
recognizer = sr.Recognizer()

# Custom CSS for title, subtitle, and output box
st.markdown("""
    <style>
        .title {
            text-align: center;
            background-color: red;
            padding: 20px;
            border-radius: 10px;
            color: #FFD700;  /* Dark Yellow color */
            font-size: 50px;
            font-weight: bold;
        }
        .subtitle {
            text-align: center;
            font-size: 28px;
            color: #333;
            margin-bottom: 20px;
            font-weight: bold;
            border-bottom: 3px solid #333;
            padding-bottom: 10px;
        }
        .output-box {
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #ccc;
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# Title and subtitle
st.markdown("<div class='title'>ARMY PUBLIC SCHOOL AGRA</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Speech Translation App</div>", unsafe_allow_html=True)

# Instructions
st.write("Click 'Start Listening' and speak to the microphone. The app will transcribe and translate your speech in real-time.")

# Define Indian languages (with full names and their language codes)
languages = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Punjabi": "pa"
}

# Group the language selectors in one row using columns
col1, col2 = st.columns(2)

with col1:
    source_language_name = st.selectbox("Choose the language you're speaking", list(languages.keys()))
    source_language = languages[source_language_name]

with col2:
    target_language_name = st.selectbox("Choose the language you want to translate to", list(languages.keys()))
    target_language = languages[target_language_name]

# Button to start the live speech translation
if st.button("Start Listening"):
    with sr.Microphone() as source:
        st.write("Listening... Please speak.")
        recognizer.adjust_for_ambient_noise(source)  # Adjust microphone sensitivity
        try:
            # Listen to the speech
            audio = recognizer.listen(source)

            # Recognize and transcribe the speech
            st.write("Transcribing...")
            spoken_text = recognizer.recognize_google(audio, language=source_language)
            
            # Display transcription in a styled box
            st.markdown(f"<div class='output-box'><strong>Transcription:</strong> {spoken_text}</div>", unsafe_allow_html=True)

            # Translate the transcription using deep_translator
            st.write("Translating...")
            translated_text = GoogleTranslator(source=source_language, target=target_language).translate(spoken_text)
            
            # Display translation in a styled box
            st.markdown(f"<div class='output-box'><strong>Translation ({target_language_name}):</strong> {translated_text}</div>", unsafe_allow_html=True)

        except sr.UnknownValueError:
            st.write("Sorry, I couldn't understand the audio.")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
