import streamlit as st
from main import get_response

st.title("プレゼミ　チャットボット")

# セッションステートの初期化
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if 'count' not in st.session_state:
    st.session_state.count = 0

# 過去の会話メッセージを表示
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.count >= 5:
    st.markdown('これで今回の会話は終了です。<a href="https://nagoyapsychology.qualtrics.com/jfe/form/SV_5cZeI9RbaCdozTU">こちら</a>をクリックしてアンケートに回答してください。', unsafe_allow_html=True)

#ユーザーの入力
user_input = st.chat_input(placeholder="ユーザーの入力")

if user_input: 
    with st.chat_message("Human"):
        st.markdown(user_input)
    st.session_state["messages"].append({"role": "Human", "content": user_input})
    with st.spinner("回答を入力中"):
        st.session_state["messages"].append({"role": "AI", "content": get_response(user_input)})
    st.session_state.count += 1
    st.rerun()