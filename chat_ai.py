from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from config import gpt
from bigfive.read_bigfive import prompt_bigfive 

memory = ConversationBufferMemory()

# prompt_bigfiveの各値を変数として渡す
extraversion = prompt_bigfive[0]
agreeableness = prompt_bigfive[1]
conscientiousness = prompt_bigfive[2]
neuroticism = prompt_bigfive[3]
openness = prompt_bigfive[4]

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

#ユーザーの入力に対する応答を取得する関数
def get_response(user_input):
  return conversation.predict(input=user_input)