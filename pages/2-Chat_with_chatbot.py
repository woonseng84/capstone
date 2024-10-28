import streamlit as st
from logics.query_handler import process_user_message

st.set_page_config(
    layout="centered",
    page_title="Grad Employment Survey Chatbot"
)

st.title("Graduate Employment Survey Chatbot")

form = st.form(key="form")
form.subheader("Prompt")

user_prompt = form.text_area("Enter your query here (e.g., Tell me about Bachelor of Medicine and Bachelor of Surgery)", height=200)

if form.form_submit_button("Submit"):
    st.toast(f"User Input Submitted - {user_prompt}")
    response = process_user_message(user_prompt)
    st.write(response)
    print(f"User input is {user_prompt}")

