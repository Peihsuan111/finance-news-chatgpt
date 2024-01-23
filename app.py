import streamlit as st

# Set page title and icon
st.set_page_config(
    page_title="ChatGPT Input Template",
    page_icon=":speech_balloon:",
)

# Add a title
st.title("ChatGPT Input Template")

# Add a text input for user input
user_input = st.text_input("You:", "Hello, ChatGPT!")

# Add a button to submit the input
if st.button("Submit"):
    # Perform any processing here
    st.success("Input submitted: {}".format(user_input))
