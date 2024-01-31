# app.py
import streamlit as st
import requests

# from opencc import OpenCC

# cc = OpenCC("s2tw")

api = "http://0.0.0.0:8000/summary"
headers = {"accept": "text/event-stream"}


def main():
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
                container = st.empty()

                # response = query_question(prompt)
                url = f"http://127.0.0.1:8000/summary/?query={prompt}"
                full_response = ""
                with requests.get(url, stream=True) as r:
                    for line in r.iter_lines(decode_unicode=True):
                        # print(line)
                        full_response += "\n"
                        full_response += line
                        container.markdown(full_response)
                        # add the full response to the message history
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
                # st.   write(line)


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

if __name__ == "__main__":
    main()
