import streamlit as st
import keras_cv
from PIL import Image
import numpy as np

# Set page config
st.set_page_config(page_title="Army Public School Agra Image Generator", layout="wide")

# Custom CSS for title styling
st.markdown("""
    <style>
    .title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        color: #1E3A8A;
        padding: 20px;
        border: 5px solid #4B5563;
        border-radius: 15px;
        background: linear-gradient(45deg, #E5E7EB, #F3F4F6);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Display the styled title
st.markdown('<p class="title">Army Public School Agra</p>', unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    # Reduce the image resolution to speed up generation
    return keras_cv.models.StableDiffusion(img_width=128, img_height=128)  # Reduced to 128x128

model = load_model()

# User input
prompt = st.text_input("Enter your image prompt:", "A beautiful landscape with mountains and a lake")

if st.button("Generate Image"):
    with st.spinner("Generating image... This may take a few seconds."):
        # Generate the image
        images = model.text_to_image(prompt, batch_size=1)
        image = Image.fromarray((images[0] * 255).astype(np.uint8))
    
    st.image(image, caption="Generated Image", use_column_width=True)

st.markdown("---")
st.markdown("Created with ❤️ for Army Public School Agra")
