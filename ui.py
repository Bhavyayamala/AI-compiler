import streamlit as st
import requests

st.title("AI App Compiler")

user_input = st.text_area("Enter your app idea")

if st.button("Generate"):
    res = requests.post(
        "http://127.0.0.1:8000/generate",
        params={"user_input": user_input}
    )

    try:
        st.json(res.json())
    except:
        st.text(res.text)