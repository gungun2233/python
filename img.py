import streamlit as st
import transformers
import torch
from diffusers import StableDiffusionPipeline
import io

@st.cache_resource
def load_model():
    try:
        # Use a smaller model that's more CPU-friendly
        model_id = "CompVis/stable-diffusion-v1-4"
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
        return pipe
    except Exception as e:
        st.error(f"Error loading the model: {str(e)}")
        return None

pipe = load_model()

if pipe is None:
    st.stop()

def generate_image(prompt, height, width, guidance_scale, num_inference_steps, seed):
    generator = torch.Generator().manual_seed(seed)
    try:
        image = pipe(
            prompt,
            height=height,
            width=width,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            generator=generator
        ).images[0]
        return image
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

def is_defense_related(prompt):
    defense_keywords = ['military', 'weapon', 'soldier', 'tank', 'aircraft', 'navy', 'army', 'defense', 'war', 'combat']
    return any(keyword in prompt.lower() for keyword in defense_keywords)

st.title("CPU-Friendly Defense-Focused Image Generator")

st.warning("Note: This application is running on CPU. Image generation may take several minutes.")

prompt = st.text_input("Enter your image prompt:")
height = st.slider("Image Height", min_value=256, max_value=512, value=384, step=64)
width = st.slider("Image Width", min_value=256, max_value=512, value=384, step=64)
guidance_scale = st.slider("Guidance Scale", min_value=1.0, max_value=20.0, value=7.5, step=0.1)
num_inference_steps = st.slider("Number of Inference Steps", min_value=10, max_value=50, value=30, step=1)
seed = st.number_input("Random Seed", min_value=0, max_value=2**32-1, value=0)

if st.button("Generate Image"):
    if prompt:
        with st.spinner("Generating image... This may take several minutes on a CPU."):
            if is_defense_related(prompt):
                enhanced_prompt = f"Defense-related image: {prompt}"
            else:
                enhanced_prompt = prompt
            
            image = generate_image(enhanced_prompt, height, width, guidance_scale, num_inference_steps, seed)
            
            if image:
                st.image(image, caption="Generated Image", use_column_width=True)
                
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                btn = st.download_button(
                    label="Download Image",
                    data=buf.getvalue(),
                    file_name="generated_image.png",
                    mime="image/png"
                )
    else:
        st.warning("Please enter a prompt before generating an image.")