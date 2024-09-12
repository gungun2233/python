import streamlit as st
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

# Set up the page
st.title("Text-to-Image Generator using Stable Diffusion")

# Load the model (only do this once to avoid reloading)
@st.cache_resource
def load_model():
    model_id = "CompVis/stable-diffusion-v1-4"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")  # Use GPU if available
    return pipe

# Get the prompt from the user
prompt = st.text_input("Enter a text prompt:", "A futuristic city skyline during sunset")

# Generate the image when the button is clicked
if st.button("Generate Image"):
    st.write("Generating the image...")

    # Load model
    pipe = load_model()

    # Generate image
    image = pipe(prompt).images[0]

    # Display the generated image
    st.image(image, caption="Generated Image", use_column_width=True)

    # Option to download the image
    image.save("generated_image.png")
    with open("generated_image.png", "rb") as file:
        btn = st.download_button(
            label="Download Image",
            data=file,
            file_name="generated_image.png",
            mime="image/png"
        )
