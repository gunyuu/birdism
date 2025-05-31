import streamlit as st
import google.generativeai as genai

# Load API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Set up model
model = genai.GenerativeModel("models/gemini-1.5-flash")

st.set_page_config(page_title="Birdsona Generator", page_icon="🐦")
st.title("🐦 Find Your Birdsona!")
st.write("Describe your personality, habits, or mood—and discover which bird matches you!")

# User input
user_input = st.text_area("Tell us about yourself:", placeholder="e.g., I'm an introvert who loves the night, quiet forests, and deep thinking...")

if st.button("Reveal My Birdsona") and user_input:
    with st.spinner("Consulting the flock..."):
        prompt = f"""You're an expert in matching birds with human personalities. A user wrote the following description about themselves:

\"\"\"{user_input}\"\"\"

Based on this, tell them:
- The name of a bird species that fits
- A short fun description of why it matches
- One fun fact about that bird
- Keep the tone light, warm, and creative
Format like:
**Your Birdsona: [Bird Name]**
[Description]
Fun Fact: [fact]"""

        response = model.generate_content(prompt)
        st.markdown(response.text)

        st.markdown("---")
        st.button("Try Again")

