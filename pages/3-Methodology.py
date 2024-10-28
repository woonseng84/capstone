import streamlit as st
from logics.query_handler import process_user_message

st.set_page_config(
    layout="centered",
    page_title="Methodology and Flow Charts"
)

st.title("Graduate Employment Survey Methodology")

# Write some text to the app
st.write("Welcome to my Graduate Employement Survey app! Below is the flow chart for the 2 pages:")

# Load and display an image
st.write("Flow for the Statistics Page:")
image_path = "./images/stats.png"  
st.image(image_path, caption="flowchart for the stats", use_column_width=True)


st.write("Flow for the Statistics Page:")
image_path2 = "./images/chat.png"  
st.image(image_path2, caption="flowchart for the chat", use_column_width=True)
