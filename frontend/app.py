# app.py
import streamlit as st
import requests
import yaml
import os, sys

LOCAL_TEST = sys.argv[1]

LOCAL_TEST = False if LOCAL_TEST == "False" else LOCAL_TEST

api = "http://0.0.0.0:8000"
if not LOCAL_TEST:
    api = os.getenv("BACKEND_API")

print(f"get backend api: {api}")

# header token
with open("token.yaml", "r") as token_yaml:
    try:
        token = yaml.safe_load(token_yaml)
    except yaml.YAMLError as exc:
        print(exc)

header_token = token["header_token"]

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
# sidebar for different session
with st.sidebar:
    password_key = st.text_input("Password", key="sara_password_key", type="password")
    st.markdown(
        """
        :red[👆 Please contact author Sara to get] :rainbow[Password]."""
    )
    "[View the source code](https://github.com/Peihsuan111/finance-news-chatgpt)"

# create the app
st.title("📰 Welcome to Augmented GPT")
st.caption(
    "🚀 根據提供的近期金融新聞及基金報告內容，請OpenAI LLM回覆問題(資料源日期:2023年10,11月)"
)

# set initial message
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "歡迎問我2023年10,11月發生的金融時事👀"}
    ]

# render older messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def main():
    # add example question box
    button_placeholder = st.empty()
    example1 = "美國總統做了哪些事？並使用條列式呈現。"

    prompt = st.chat_input("Enter your message...")
    if len(st.session_state.messages) == 1:
        if button_placeholder.button("例如: " + example1):
            prompt = example1
            button_placeholder.empty()

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
                url = f"{api}/chat"
                full_response = ""
                with requests.get(
                    url,
                    stream=True,
                    json={
                        "text": prompt,
                    },
                    params={"x_token": header_token},
                    headers={"Authorization": f"Bearer {password_key}"},
                ) as r:
                    for line in r.iter_content(decode_unicode=True):
                        full_response += line
                        container.markdown(full_response)
                # add the full response to the message history
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )


if __name__ == "__main__":
    main()
