# 📝 QuickSum AI: URL to Insights

**QuickSum AI** is a high-performance web application that transforms long-form web articles into concise, actionable bullet points. It solves information overload by allowing users to quickly grasp the core message of any webpage, with an optional "Deep Dive" feature to explore specific details on demand.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4136?style=for-the-badge&logo=Streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=google-gemini&logoColor=white)

## 🚀 Features

- **One-Click Summarization:** Paste a URL and receive a curated list of 5 high-level bullet points.
- **Smart Scraping:** Automatically extracts clean text from articles while ignoring ads, navigation bars, and footers.
- **"Deep Dive" Analysis:** Click on any bullet point to generate a detailed explanation of that specific concept using the full context of the article.
- **Fast & Cost-Effective:** Powered by Google Gemini 1.5 Flash for near-instant responses and high accuracy.
- **Responsive UI:** Built with Streamlit for a clean, modern, and mobile-friendly experience.

## 🛠️ Tech Stack

- **Frontend/Backend:** [Streamlit](https://streamlit.io/)
- **LLM:** [Google Gemini 1.5 Flash](https://ai.google.dev/)
- **Scraping Engine:** [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) & [Requests](https://requests.readthedocs.io/)
- **Environment Management:** `python-dotenv`

## ⚙️ Installation & Local Setup

Follow these steps to run the app on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/quicksum-ai.git
cd quicksum-ai
