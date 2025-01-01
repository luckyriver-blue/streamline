import streamlit as st
from chat_ai import get_response
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

#Firebaseから有効な参加者IDを取得する関数
def  get_valid_ids():
  valid_ids = []
  users = db.collection('users').stream()

  for user in users:
    valid_ids.append(user.id)
  
  return valid_ids

# データの追加の関数
def add_data(collection_name, document_id, data):
  db.collection(collection_name).document(document_id).set(data)

# セッションステートの初期化
if 'user_id' not in st.session_state:
  st.session_state['user_id'] = None
if 'messages' not in st.session_state:
  st.session_state["messages"] = [{"role": "AI", "content": "今日は何がありましたか？"}]
if 'count' not in st.session_state:
  st.session_state.count = 0

#クエリパラメータからuser_idを取得（あれば）
query_params = st.query_params
if "user_id" in query_params:
  st.session_state["user_id"] = query_params.get('user_id', [None])[0]


#ログイン（実験参加者のid認証）
valid_ids = get_valid_ids()
if not st.session_state['user_id']:
  user_id = st.text_input("IDを半角で入力してエンターを押してください")
  if user_id:
    if user_id in valid_ids:
      st.session_state['user_id'] = user_id
      st.rerun()
    else:
      st.error("IDが間違っています")

if st.session_state['user_id']:
  # 会話メッセージの履歴を表示
  for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if st.session_state.count == 5:
    add_data('users', st.session_state['user_id'], {"messages": st.session_state["messages"]})
    st.markdown('これで本日の会話は終了です。')

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