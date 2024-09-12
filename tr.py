import streamlit as st
import googletrans
from googletrans import Translator

st.title("Language Translator")

translator = Translator()

text_input = st.text_input("Enter the text you want to translate:")

target_lang = st.selectbox("Select the target language:", list(googletrans.LANGUAGES.values()))

if st.button("Translate"):
    translated_text = translator.translate(text_input, dest=target_lang)
    st.text_area("Translated Text:", value=translated_text.text)