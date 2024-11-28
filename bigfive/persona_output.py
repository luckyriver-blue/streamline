import os
import openai
from config import openai_key
from human_description import description
import pandas as pd
from datetime import datetime

parent_directory = os.path.abspath(os.path.join('persona_output.py', '..'))
task_file = os.path.join(parent_directory, 'data', 'test_data', 'task.txt')
bigfive_file = os.path.join(parent_directory, 'data', 'test_data', 'bigfive.csv')
result_file = os.path.join(parent_directory, 'data', 'test_data', 'result.csv')

openai.api_key=openai_key

#タスク判断課題の文章を一文ずつリスト化
with open(task_file, 'r', encoding='utf-8') as task_data:
  lines = [s.rstrip() for s in task_data.readlines()]

#ビッグファイブのcsvファイルを読み取りLOW・MEDIUM・HIGHでリスト化
with open(bigfive_file, 'r', encoding='utf-8') as bigfive_data:
  bigfive_list = [float(i) for i in bigfive_data.readline().strip().split(',')]
#とりあえず5段階のデータで考える。とりあえずMEDIUMを2.5以上3.5未満として出す。
prompt_bigfive = []
for score in bigfive_list:
  if score >= 3.5:
    prompt_bigfive.append('HIGH')
  elif score >= 2.5:
    prompt_bigfive.append('MEDIUM')
  else:
    prompt_bigfive.append('LOW')


#判断タスクファイルから一行ずつ取り出して全て判断させる
result = []
for line in lines:     
  # プロンプトを基に出力させるようにする
  response = openai.chat.completions.create(
      model="gpt-4o",
      messages=[
        {
          "role": "system",
          "content": "For the following task, respond in a way that matches this BIG FIVE personality questionnaire:\n"
                     f"Extraversion: {prompt_bigfive[0]}, Agreeableness: {prompt_bigfive[1]}, Conscientiousness: {prompt_bigfive[2]}, Neuroticism: {prompt_bigfive[3]}, Openness: {prompt_bigfive[4]}\n\n"
                     "Additionally, respond in a way that mathces this description:\n"
                     f"{description}\n\n"
                     "Your response should be in accordance with the personality and description provided above."
        },
        {
          "role": "user",
          "content": "Please rate the following statement by selecting a number from 1 to 5, where:\n"
                     "1 = not applicable at all,\n"
                     "2 = not applicable,\n"
                     "3 = neutral,\n"
                     "4 = applicable,\n"
                     "5 = strongly applicable.\n\n"
                     f"Statement: {line}\n"
                     "Please ensure that your response is a number between 1 and 5."
        },
      ],
      max_tokens=1,
  )

  #結果をリストに保存
  result.append(response.choices[0].message.content)

#結果リストをcsvファイルに出力
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
output_data = result + [timestamp]
pd.DataFrame([output_data]).to_csv(result_file, index=False, header=False, mode="a")   
print(f"Results saved to {result_file}.")