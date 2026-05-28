import streamlit as st
import pdfplumber
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.title("📑 Fact-Checking Web App")

# Step 1: Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    # Step 2: Extract Claims (numbers, years, percentages)
    claims = re.findall(r'\b\d{4}\b|\b\d+%|\b\d+\b', text)

    results = []
    for claim in claims:
        query = f"{claim}"
        url = f"https://www.bing.com/search?q={query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Simple check: does claim appear in search results?
        found = soup.get_text().lower().count(claim.lower()) > 0

        if found:
            status = "✅ Verified"
        else:
            status = "❌ False"

        results.append({"Claim": claim, "Status": status})

    # Step 3: Show Results
    st.subheader("Verification Results")
    df = pd.DataFrame(results)
    st.dataframe(df)
