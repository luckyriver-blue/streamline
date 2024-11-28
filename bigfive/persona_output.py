import os
import openai
from config import openai_key
import pandas as pd

parent_directory = os.path.abspath(os.path.join('persona_output.py', '..'))
task_file = os.path.join(parent_directory, 'data', 'test_data', 'task.txt')
bigfive_file = os.path.join(parent_directory, 'data', 'test_data', 'bigfive.csv')

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
for line in lines:     
  print(line)

  # プロンプトを基に出力させるようにする
  response = openai.chat.completions.create(
      model="gpt-4o",
      messages=[
        {
          "role": "system",
          "content": "For the following task, respond in a way that matches this BIG FIVE personality questionnaire:\n"
                     f"Extraversion: {prompt_bigfive[0]}, Agreeableness: {prompt_bigfive[1]}, Conscientiousness: {prompt_bigfive[2]}, Neuroticism: {prompt_bigfive[3]}, Openness: {prompt_bigfive[4]}\n"
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

  #結果をcsvファイルに出力
  print(response.choices[0].message.content)