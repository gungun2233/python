import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator

# Initialize recognizer
recognizer = sr.Recognizer()

# Streamlit app title
st.title("Live Speech Translation App - Indian Languages")

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

# Display dropdown for selecting the language you're speaking
source_language_name = st.selectbox("Choose the language you're speaking", list(languages.keys()))
source_language = languages[source_language_name]

# Display dropdown for selecting the language you want to translate to
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
            st.write(f"Transcription: {spoken_text}")

            # Translate the transcription using deep_translator
            st.write("Translating...")
            translated_text = GoogleTranslator(source=source_language, target=target_language).translate(spoken_text)
            st.write(f"Translation ({target_language_name}): {translated_text}")

        except sr.UnknownValueError:
            st.write("Sorry, I couldn't understand the audio.")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
