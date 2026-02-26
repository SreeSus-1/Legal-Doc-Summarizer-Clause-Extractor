import streamlit as st
import requests

st.title("⚖️ Legal Document Analyzer")

text_input = st.text_area("Paste legal text here:", height=300)

API_URL = "http://127.0.0.1:8000/analyze/"  # safer than localhost on some setups

if st.button("Analyze"):
    if not text_input.strip():
        st.warning("Please paste some legal text first.")
        st.stop()

    with st.spinner("Analyzing..."):
        try:
            resp = requests.post(API_URL, json={"text": text_input}, timeout=180)
        except requests.RequestException as e:
            st.error(f"❌ Could not reach FastAPI at {API_URL}\n\n{e}")
            st.stop()

    st.write("Status code:", resp.status_code)

    if resp.status_code != 200:
        st.error("❌ Backend error (raw response):")
        st.code(resp.text)
        st.stop()

    try:
        results = resp.json()
    except ValueError:
        st.error("❌ Backend did not return JSON. Raw response:")
        st.code(resp.text)
        st.stop()

    st.subheader("📄 Document Summary")
    st.write(results.get("summary", ""))

    st.subheader("📌 Key Clauses")
    st.write(results.get("clauses", ""))

    st.subheader("🔍 Named Entities")
    st.write(results.get("entities", ""))