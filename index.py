import streamlit as st
from main import get_response
from config import firebase_credential
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Firebase Admin SDKの初期化
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credential)
    firebase_admin.initialize_app(cred)

# Firestoreのインスタンスを取得
db = firestore.client()

# データの追加
def add_data(collection_name, document_id, data):
    db.collection(collection_name).document(document_id).set(data)


st.title("プレゼミ　チャットボット")

# セッションステートの初期化
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "AI", "content": "今日は何がありましたか？"}]
if 'count' not in st.session_state:
    st.session_state.count = 0

# 過去の会話メッセージを表示
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.count >= 5:
    add_data('users', 'user1', {"messages": st.session_state["messages"]})
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