from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_text_generation_model():
    return pipeline("text-generation", model="gpt2", framework="pt")  # Force PyTorch

text_generator = load_text_generation_model()

st.title("Text Generation with GPT-2")

# Input from user
input_text = st.text_input("Enter a prompt:")

# Generate text when the button is clicked
if st.button("Generate"):
    if input_text:
        generated_text = text_generator(input_text, max_length=100, num_return_sequences=1)
        st.write(generated_text[0]['generated_text'])
    else:
        st.write("Please enter some text to generate.")
