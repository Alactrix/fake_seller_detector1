# streamlit_app/app.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from features.features import calculate_score
import streamlit as st
from ml_model.predict_model import predict_fake_review
import streamlit as st
from features.features import calculate_score
from utils.reddit_scraper import get_latest_scam_domains


st.set_page_config(page_title="🛡️ Fake Seller Website Detector")
st.title("🛡️ Fake Seller Website Detector")
st.markdown("Enter a website URL to check if it might be a scam or fake.")

# ---- User Input ----
url = st.text_input("🌐 Website URL", placeholder="https://example.com")

if url:
    with st.spinner("Analyzing website..."):
        score, reasons = calculate_score(url)
    
    st.markdown("### 🧠 Website Score")
    st.metric("Trust Score", f"{score}/100")

    st.markdown("### 📌 Reasons")
    for reason in reasons:
        st.write(reason)

# ---- Reddit Scam Scanner Section ----
st.markdown("---")
st.markdown("## Reddit-Reported Scam Sites")
scam_sites = get_latest_scam_domains()

scam_sites = get_latest_scam_domains()

st.markdown("Here are the latest domains flagged by Reddit users as potential scams:")

for domain in scam_sites:
    full_url = f"https://{domain}" if not domain.startswith("http") else domain
    st.markdown(f"- 🔗 [{domain}]({full_url})")




