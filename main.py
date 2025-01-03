import streamlit as st
from config import firebase_credential
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from config import gpt
import datetime


# Firebase Admin SDKの初期化
if not firebase_admin._apps:
  cred = credentials.Certificate(firebase_credential)
  firebase_admin.initialize_app(cred)

# Firestoreのインスタンスを取得
db = firestore.client()


# セッションステートの初期化
if 'user_id' not in st.session_state:
  st.session_state['user_id'] = None
if 'messages' not in st.session_state:
  st.session_state["messages"] = [{"role": "AI", "content": "今日は何がありましたか？"}]
if 'count' not in st.session_state:
  st.session_state.count = 0


memory = ConversationBufferMemory()


#会話パート何日間行うか
talk_days = 1 
#5日間の会話パート
now = datetime.datetime.now()
#会話パート開始日
start_day = "2025-01-03" #仮
start_day_obj = datetime.datetime.strptime(start_day, "%Y-%m-%d")
#今日が会話パート何日目か計算
now_day = (now - start_day_obj).days + 1


#firebaseからuser_idを通してビッグファイブデータと会話データを取得
doc_ref = db.collection("users").document(st.session_state['user_id'])
doc = doc_ref.get()

data = doc.to_dict()
if data is None:
  prompt_bigfive = {}
  talk_day_data = {}
else:
  prompt_bigfive = data.get('bigfive', {})
  talk_day_data = data.get('messages', {}).get(f'day{now_day}', {}).get('messages', {})

# prompt_bigfiveの各値を変数として渡す
extraversion = prompt_bigfive.get("extraversion", "N/A")
agreeableness = prompt_bigfive.get("agreeableness", "N/A")
conscientiousness = prompt_bigfive.get("conscientiousness", "N/A")
neuroticism = prompt_bigfive.get("neuroticism", "N/A")
openness = prompt_bigfive.get("openness", "N/A")

# プロンプトテンプレートの設定
prompt_template = PromptTemplate(
  input_variables=["history", "input"],
  template=f"""
  ユーザーの性格：
  Extraversion: {extraversion}, 
  Agreeableness: {agreeableness}, 
  Conscientiousness: {conscientiousness}, 
  Neuroticism: {neuroticism}, 
  Openness: {openness}

  ユーザーの性格を参照して、ユーザーにとって最適な会話を心がけてください。
  ユーザーの性格のスコアには言及しないでください。
  300文字以内で回答してください。
  以下は会話の履歴です：\n{{history}}\n\nユーザーの入力：{{input}}
  """
)

conversation = ConversationChain(
  llm=gpt, 
  verbose=False, 
  prompt=prompt_template,
  memory=memory
)

#上記のプロンプトを用いて、ユーザーの入力に対する応答を取得する関数
def get_response(user_input):
  return conversation.predict(input=user_input)


#Firebaseから有効な参加者IDを取得する関数
def get_valid_ids():
  valid_ids = []
  users = db.collection('users').stream()

  for user in users:
    valid_ids.append(user.id)
  
  return valid_ids


# データの追加の関数
def add_data(collection_name, document_id, data):
  db.collection(collection_name).document(document_id).set(data, merge=True)


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
  st.stop()

     
#今日の日付が開始日よりも前の場合
if now < start_day_obj:
  #ビッグファイブのアンケートに回答してない場合は認証させてアンケートリンクを表示する
  if prompt_bigfive == {}:
    st.markdown(f'<a href="https://nagoyapsychology.qualtrics.com/jfe/form/SV_4N1LfAYkc9TrY8u?user_id={st.session_state["user_id"]}" target="_blank">こちら</a>をクリックしてアンケートに回答してください。', unsafe_allow_html=True)
  #ビッグファイブのアンケートに回答済みの場合
  else:
    st.write(f"会話パートは{start_day_obj.month}月{start_day_obj.day}日15時から開始できます。")
  st.stop()
#5日間の後の場合
elif now_day > talk_days:
  st.write(f"{talk_days}日間の会話パートは終了しました。")
  st.stop()
#今の時間が午後3時よりも前の場合
elif now.hour < 15:
  st.write("会話は本日の15時から開始できます。")
  st.stop()
else:
  st.title(f"会話{now_day}日目")


if st.session_state['user_id']:
  # 会話メッセージの履歴を表示
  if talk_day_data != {}:
    st.session_state["messages"] = talk_day_data
  for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  
  #会話が5ターンずつ終了した場合
  if talk_day_data != {} or st.session_state.count == 5:
    if talk_day_data == {}: #firebaseにデータが格納されていなかったら格納する
      add_data('users', st.session_state['user_id'], {"messages": {f"day{now_day}": {"messages": st.session_state["messages"]}}})
    if now_day < talk_days:
      st.markdown('本日の会話は終了です。')
    else:
      st.markdown(
        f'{talk_days}日間の会話パートは終了です。<br><a href="https://nagoyapsychology.qualtrics.com/jfe/form/SV_5b4FQikEOMWsjAO">こちら</a>をクリックしてアンケートに回答してください。', unsafe_allow_html=True
      )
    st.stop()

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