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
    """Fetches the text content from a URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'} # Helps prevent some blocks
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
            
        text = soup.get_text(separator=' ')
        clean_text = ' '.join(text.split())
        return clean_text[:15000] # Gemini can handle more, but 15k is plenty for a summary
    except Exception as e:
        return f"Error scraping site: {e}"

def get_ai_summary(text):
    """Generates bullet points from text using Gemini."""
    prompt = f"""
    Summarize the following web article into exactly 5 concise bullet points. 
    Focus on the most important facts and actions.
    \n\n{text}
    """
    response = model.generate_content(prompt)
    return response.text

def get_deep_dive(text, bullet_point):
    """Explains a specific bullet point in detail using Gemini."""
    prompt = f"""
    Context: {text[:10000]}
    
    Task: Provide a 'Deep Dive' explanation for this specific point: "{bullet_point}"
    Explain why this matters and provide any extra detail found in the context.
    Keep it informative but concise.
    """
    response = model.generate_content(prompt)
    return response.text

# --- UI Layout ---

st.set_page_config(page_title="QuickSum Gemini", page_icon="✨")
st.title("✨ QuickSum Gemini")
st.subheader("Paste a URL to get a summarized bulleted list.")

url_input = st.text_input("Enter URL here:", placeholder="https://example.com")

if st.button("Summarize"):
    if url_input:
        with st.spinner("Scraping and analyzing..."):
            raw_text = scrape_website(url_input)
            
            if "Error" in raw_text:
                st.error(raw_text)
            else:
                summary_raw = get_ai_summary(raw_text)
                
                # Split the summary into lines/bullets
                bullets = [b.strip("- ").strip("* ").strip() for b in summary_raw.split('\n') if b.strip()]
                
                st.success("Summary Complete!")
                st.markdown("---")
                
                # Display Bullets with Deep Dive
                for i, bullet in enumerate(bullets):
                    st.write(f"**{i+1}. {bullet}**")
                    
                    # Using an expander for the "Deep Dive" feel
                    with st.expander(f"🔍 Deep Dive Point {i+1}"):
                        if st.button(f"Analyze this point", key=f"btn_{i}"):
                            with st.spinner("Deep diving..."):
                                deep_dive = get_deep_dive(raw_text, bullet)
                                st.info(deep_dive)
    else:
        st.warning("Please enter a URL first.")
