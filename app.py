import streamlit as st
import google.generativeai as genai
import requests  # Changed from openai
from apikey import google_gemini_api_key, stability_api_key  # Get new key from stability.ai
from streamlit_carousel import carousel



# Configure APIs
genai.configure(api_key=google_gemini_api_key)
STABILITY_API_HOST = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

# Gemini model
model = genai.GenerativeModel(model_name="gemini-2.5-flash-preview-04-17")

# Streamlit UI
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .blog-header {font-size: 2.5em; font-weight: bold; color: #639bff;}
    .blog-section {background: #fff; border-radius: 12px; box-shadow: 0 2px 12px #eee; padding: 2em; margin-bottom: 2em;}
    </style>
""", unsafe_allow_html=True)
# Add this CSS after your existing styles
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #639bff10 0%, #FDF6F0 50%, #ffd6e710 100%);
        position: relative;
        overflow: hidden;
    }
    
    /* Animated floating elements */
    .main::before {
        content: "";
        position: absolute;
        width: 400px;
        height: 400px;
        background: #639bff10;
        border-radius: 50%;
        top: -100px;
        left: -100px;
        animation: float 20s infinite;
    }
    
    .main::after {
        content: "";
        position: absolute;
        width: 300px;
        height: 300px;
        background: #ffd6e720;
        clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
        bottom: -150px;
        right: -150px;
        animation: float 25s infinite;
    }
    
    @keyframes float {
        0% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(20px, 20px) rotate(180deg); }
        100% { transform: translate(0, 0) rotate(360deg); }
    }
    
    /* Improved blog section styling */
    .blog-section {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 2.5rem;
        margin-bottom: 2rem;
        transition: transform 0.3s ease;
    }
    
    .blog-section:hover {
        transform: translateY(-5px);
    }
    
    /* Custom spinner styling */
    .stSpinner > div {
        border-color: #639bff !important;
        border-right-color: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="blog-header">📝 Welcome to ANIBLOGS</div>', unsafe_allow_html=True)
st.markdown('<div class="blog-section">Your AI-powered blog content will appear here.</div>', unsafe_allow_html=True)



# st.markdown('<div class="blog-header">📝 Welcome to ANIBLOGS</div>', unsafe_allow_html=True)
# st.markdown('<div class="blog-section">Your AI-powered blog content will appear here.</div>', unsafe_allow_html=True)

# st.title("📝 Welcome to ANIBLOGS: Your Smart AI Blogging Assistant 🚀")
# st.subheader("✍️ Blog like a beast, powered by AI feast — ANIBLOGS is here to unleash your inner writer!")

# 🖼️ Image generation using Stable Diffusion SD3
def generate_images(prompt, n_images=1):
    images = []
    try:
        response = requests.post(
            f"{STABILITY_API_HOST}",
            headers={
                "authorization": f"Bearer {stability_api_key}",
                "accept": "image/*"
            },
            files={"none": ''},
            data={
                "prompt": prompt,
                "output_format": "jpeg",
                "model": "sd3-turbo",
                "size": "1024x1024",
            }
        )
        
        if response.status_code == 200:
            images.append(response.content)
        else:
            st.error(f"Image generation failed: {response.text}")
    except Exception as e:
        st.error(f"API Error: {str(e)}")
    return images

# Sidebar input (unchanged)
with st.sidebar:
    st.title("Input your Blog Details")
    blog_title = st.text_input("Blog Title")
    keywords = st.text_input("Keywords (comma-separated)")
    num_words = st.slider("Number of words", 250, 1000, step=100)
    num_images = st.number_input("Number of images", min_value=1, max_value=1, step=1)
    submit_button = st.button("Generate your blog here")

# Main logic (updated image handling)
if submit_button and blog_title and keywords:
    with st.spinner("Generating your blog..."):
        prompt = f"""
        You are ANIBLOGS, a witty, smart, and creative AI-powered blogging assistant.
        Write a blog post titled "{blog_title}" using the following keywords: {keywords}.
        The blog should be around {num_words} words, with a clear, human-like, SEO-friendly tone.
        Include a strong introduction, structured sections, and a catchy conclusion.
        """
        response = model.generate_content(prompt)
        st.markdown("## ✨ Here is your Blog")
        st.write(response.text)

    with st.spinner("Generating relevant images..."):
        image_prompt = (
            f"Professional blog header image for article titled '{blog_title}'. "
            f"Visual elements representing: {keywords}. "
            "Modern minimalist style, warm colors, high quality, 4K resolution."
        )
        image_data = generate_images(image_prompt, num_images)
        
        st.markdown(f"{blog_title}")
        for img_bytes in image_data:
            st.image(img_bytes, use_container_width=True)
