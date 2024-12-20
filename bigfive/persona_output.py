import os
import openai
from config import openai_key
from human_description import description
import pandas as pd
from datetime import datetime
from bigfive.read_bigfive import prompt_bigfive 

parent_directory = os.path.abspath(os.path.join('persona_output.py', '..'))
task_file = os.path.join(parent_directory, 'data', 'test_data', 'task.txt')
result_file = os.path.join(parent_directory, 'data', 'experiment_data', 'task_ai_prediction', 'result.csv')

openai.api_key=openai_key

#タスク判断課題の文章を一文ずつリスト化
with open(task_file, 'r', encoding='utf-8') as task_data:
  lines = [s.rstrip() for s in task_data.readlines()]


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