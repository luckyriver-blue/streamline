import streamlit as st

# セッション状態を初期化
if "messages" not in st.session_state:
    st.session_state["messages"] = []
js = '''
<script>
    var body = parent.document.querySelector('.st-emotion-cache-1wmy9hl');
    body.scrollTop = body.scrollHeight;
    console.log(body.scrollHeight);
</script>
'''



input_style = f"""
<style>
  .footer {{
    position: fixed;
    bottom: 0;
    width: 100%;
    background-color: #ffffff;
    padding: 5rem;
  }}
  .stTextArea {{
    position: fixed;
    bottom: 4rem;
  }}
  .stButton {{
    position: fixed;
    bottom: 1rem;
    left: calc(105px + 64%);
  }}
</style>
"""
st.markdown(input_style, unsafe_allow_html=True)

# チャット履歴の表示
st.title("チャット履歴")
for message in st.session_state["messages"]:
    st.write(message)
st.components.v1.html(js, height=0)


# ユーザーのメッセージ送信
def send_message():
    user_message = st.session_state["user_input"]
    if user_message:
        st.session_state["messages"].append(user_message)
        st.session_state["user_input"] = ""  # 入力欄をクリア



# 固定されたフッター
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.text_area(
  "メッセージを入力してください", 
  key="user_input", 
  placeholder="メッセージを入力してください",
)
st.button("送信", on_click=send_message)
