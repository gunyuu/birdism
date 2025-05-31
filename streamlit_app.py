import streamlit as st
import google.generativeai as genai
import requests
import re

# Configure Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-flash")

# UI Setup
st.set_page_config(page_title="Birdsona Generator", page_icon="🐦")
st.title("🐦 Find what kind of bird are you in the next life!")
st.write("Describe your personality, habits, or mood — and discover which bird matches you!")

# Text input
user_input = st.text_area("Tell us about yourself:", placeholder="e.g., I'm curious, love the ocean, and enjoy peaceful mornings...")

def get_bird_image(bird_name):
    """Fetch bird image from Google Custom Search"""
    api_key = st.secrets["GOOGLE_API_KEY"]
    cse_id = st.secrets["GOOGLE_CSE_ID"]
    query = f"{bird_name} bird"

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cse_id,
        "q": query,
        "searchType": "image",
        "num": 1,
        "safe": "high"
    }

    try:
        response = requests.get(url, params=params)
        results = response.json()
        return results["items"][0]["link"] if "items" in results else None
    except Exception as e:
        return None

def extract_bird_name(text):
    """Extract bird name from Gemini response"""
    match = re.search(r"\*\*Your Birdsona: (.+?)\*\*", text)
    return match.group(1).strip() if match else None

if st.button("Reveal reincarnation") and user_input:
    with st.spinner("Consulting the birds..."):
        prompt = f"""You're an expert in matching birds with human personalities. A user wrote:

\"\"\"{user_input}\"\"\"

Based on this, reply with:
- The bird species that best matches (bold heading format)
- A short, fun description of why it fits
- One fun fact about that bird
Keep the tone light and creative. Format it like:
**Your Birdsona: [Bird Name]**
[Why it matches]
Fun Fact: [Interesting fact]"""

        response = model.generate_content(prompt)
        output = response.text
        st.markdown(output)

        bird_name = extract_bird_name(response.text)
        st.write("Bird Name:", bird_name)
        if bird_name:
            image_url = get_bird_image(bird_name)
            st.write("Search URL:", response.url)

            if image_url:
                st.image(image_url, caption=bird_name)
            else:
                st.warning("Couldn't fetch an image. Try another description!")
        else:
            st.warning("Couldn’t detect a bird name in the result.")
