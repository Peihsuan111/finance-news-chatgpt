# app.py
import streamlit as st
from rag_functiom import query_question

# Set page title and icon
st.set_page_config(
    page_title="AI Summarizer",
    page_icon=":speech_balloon:",
)

# Use CSS to style the button
st.markdown(
    """
    <style>
        div.stButton > button {
            width: 100%;
            text-align: left;
            justify-content: flex-start;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
# sidebar for different session(Data Summary & News Summary)
# with st.sidebar:
# openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
# "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
# "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
# "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

# create the app
st.title("📰 Welcome to Augmented GPT")
st.caption("🚀 根據提供的近期金融新聞及基金報告內容，請OpenAI LLM回覆問題")

# set initial message
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "歡迎問我近期不同市場的回顧及未來展望 👀"}
    ]

# render older messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

exapmle1 = "整理美國股市回顧及未來展望"
exapmle2 = "整理歐洲股市回顧及未來展望"
exapmle3 = "整理日本股市回顧及未來展望"
exapmle4 = "幫我整理新興亞洲股票市場回顧及未來展望。亞洲股票市場包含「中國、印度、東協、台灣、南韓」等等的亞洲國家。"
exapmle5 = "整理歐非中東股市回顧及未來展望"
exapmle6 = "整理拉丁美洲股市回顧及未來展望"
exapmle7 = "整理公債市場回顧及未來展望"
exapmle8 = "整理信用債市場回顧及未來展望"
exapmle9 = "整理外匯市場回顧及未來展望"

# button
if st.button(exapmle1):
    prompt = exapmle1
elif st.button(exapmle2):
    prompt = exapmle2
elif st.button(exapmle3):
    prompt = exapmle3
elif st.button(exapmle4):
    prompt = exapmle4
elif st.button(exapmle5):
    prompt = exapmle5
elif st.button(exapmle6):
    prompt = exapmle6
elif st.button(exapmle7):
    prompt = exapmle7
elif st.button(exapmle8):
    prompt = exapmle8
elif st.button(exapmle9):
    prompt = exapmle9
else:
    # render the chat input
    prompt = st.chat_input("Enter your message...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    # render the user's new message
    with st.chat_message("user"):
        st.markdown(prompt)


if st.session_state.messages[-1]["role"] != "assistant":
    # render the assistant's response
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            message_placeholder = st.empty()

            # if "messages" in st.session_state:
            #     chat_history = [
            #         m for m in st.session_state.messages[:-1]
            #     ]  # convert_message(m)
            #     print(chat_history)
            # else:
            #     chat_history = []

            response = query_question(prompt)
            full_response = f"{response.get('result')}"
            source_documents = f"{response.get('source_documents')}"
            # for response in custom_chain.stream(
            #     {"input": prompt, "chat_history": chat_history}
            # ):
            #     if "output" in response:
            #         full_response += response["output"]
            #     else:
            #         full_response += response.content

            #     message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        # add the full response to the message history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )


def get_chatbot_response(user_input):
    # Replace this with your actual chatbot logic
    # For simplicity, let's just echo the user's input
    return user_input


# def main():
#     st.title("ChatGPU Interface")

#     # User input text box
#     user_input = st.text_input("You:", key="user_input")

#     # Display user input
#     st.markdown(f"**User:** {user_input}")

#     # Simulate a response (you can replace this with a more sophisticated chatbot logic)
#     response = get_chatbot_response(user_input)

#     # Display the chatbot response
#     st.markdown(f"**ChatGPU:** {response}")

# if __name__ == "__main__":
#     main()
