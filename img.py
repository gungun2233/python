import streamlit as st
import torch
from diffusers import FluxPipeline
from huggingface_hub import login

# Login with Hugging Face token
login(token="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")  # Replace with your token

# Title of the app
st.title("Generate AI Art using FluxPipeline")

# Model setup
st.write("Setting up the model...")
pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload()  # save VRAM by offloading the model to CPU if needed

# Input prompt from the user
prompt = st.text_input("Enter a prompt:", "A cat holding a sign that says hello world")

# Slider for other configurations
guidance_scale = st.slider("Guidance Scale:", min_value=1.0, max_value=10.0, value=3.5)
num_inference_steps = st.slider("Number of Inference Steps:", min_value=1, max_value=100, value=50)

# Generate the image when the button is clicked
if st.button("Generate Image"):
    st.write("Generating image...")

    # Generate the image
    image = pipe(
        prompt,
        height=1024,
        width=1024,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        max_sequence_length=512,
        generator=torch.Generator("cpu").manual_seed(0)
    ).images[0]

    # Save and display the image
    image.save("flux-dev.png")
    st.image(image, caption="Generated Image", use_column_width=True)

# Download button
with open("flux-dev.png", "rb") as file:
    btn = st.download_button(label="Download Image", data=file, file_name="flux-dev.png", mime="image/png")
