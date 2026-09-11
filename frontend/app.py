import streamlit as st
import requests
from pathlib import Path

st.set_page_config(page_title="AI HR Assistant", layout="wide")

st.title("AI HR Recruitment Assistant - Minimal UI")

model = st.text_input("Ollama model", value="qwen3:8b")
prompt = st.text_area("Prompt", value="Write a short candidate summary for John Doe based on resume...")

if st.button("Generate"):
    try:
        backend_url = st.text_input("Backend URL", value="http://127.0.0.1:8000")
        resp = requests.post(f"{backend_url}/generate", json={"prompt": prompt, "model": model})
        data = resp.json()
        if "output" in data:
            st.success("Generated")
            st.code(data["output"])
        else:
            st.error(data.get("error", "Unknown error"))
    except Exception as e:
        st.exception(e)
