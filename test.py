import streamlit as st

# セッションステートの初期化
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# チャットメッセージの表示
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# テキストエリアでユーザーからの入力を受け取る
user_input = st.text_area("あなたのメッセージを入力してください:", height=50)

# カスタム送信ボタン
if st.button("送信"):
    if user_input:
        # メッセージをセッションに追加して表示
        st.session_state["messages"].append({"role": "user", "content": user_input})
        # 表示する例（仮のレスポンス）
        st.session_state["messages"].append({"role": "assistant", "content": "こちらが応答です。"})

