import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Configuration
load_dotenv()
# Replace with your Gemini API Key or set it in a .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("API Key not found! Please set GOOGLE_API_KEY in your .env file or Streamlit Secrets.")
    st.stop()
    
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model (Gemini 1.5 Flash is best for speed/cost)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- Helper Functions ---

def scrape_website(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
        text = soup.get_text(separator=' ')
        clean_text = ' '.join(text.split())
        return clean_text[:15000]
    except Exception as e:
        return f"Error scraping site: {e}"

def get_ai_summary(text):
    prompt = f"Summarize the following web article into exactly 5 concise bullet points. Focus on the most important facts and actions.\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

def get_deep_dive(text, bullet_point):
    prompt = f"Context: {text[:10000]}\n\nTask: Provide a 'Deep Dive' explanation for this specific point: \"{bullet_point}\" Explain why this matters and provide any extra detail found in the context."
    response = model.generate_content(prompt)
    return response.text

# --- UI Layout ---

st.set_page_config(page_title="QuickSum Gemini", page_icon="✨")
st.title("✨ QuickSum Gemini")
st.subheader("Paste a URL to get a summarized bulleted list.")

url_input = st.text_input("Enter URL here:", placeholder="https://example.com")

# Initialize Session State
# This creates "memory" variables that persist across reruns
if "summary" not in st.session_state:
    st.session_state.summary = None
if "raw_text" not in st.session_state:
    st.session_state.raw_text = None

if st.button("Summarize"):
    if url_input:
        with st.spinner("Scraping and analyzing..."):
            raw = scrape_website(url_input)
            if "Error" in raw:
                st.error(raw)
            else:
                # Save results to session_state (The Memory)
                st.session_state.raw_text = raw
                st.session_state.summary = get_ai_summary(raw)
    else:
        st.warning("Please enter a URL first.")

# --- Display Logic ---
# This section now runs every time the script reruns
if st.session_state.summary:
    st.success("Summary Complete!")
    st.markdown("---")
    
    # Split the summary from memory into bullet points
    bullets = [b.strip("- ").strip("* ").strip() for b in st.session_state.summary.split('\n') if b.strip()]
    
    for i, bullet in enumerate(bullets):
        st.write(f"**{i+1}. {bullet}**")
        
        # Use a unique key for each button so Streamlit doesn't get confused
        if st.button(f"🔍 Deep Dive Point {i+1}", key=f"btn_{i}"):
            with st.spinner("Deep diving..."):
                deep_dive = get_deep_dive(st.session_state.raw_text, bullet)
                st.info(deep_dive)
