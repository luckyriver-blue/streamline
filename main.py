from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from config import gpt

memory = ConversationBufferMemory()

# プロンプトテンプレートの設定
prompt_template = PromptTemplate(
    input_variables=["history", "input"],
    template="以下は会話の履歴です：\n{history}\n\nユーザーの入力：{input}"
)


conversation = ConversationChain(
    llm=gpt, 
    verbose=True, 
    prompt=prompt_template,
    memory=memory
)

#ユーザーの入力に対する応答を取得する関数
def get_response(user_input):
    return conversation.predict(input=user_input)