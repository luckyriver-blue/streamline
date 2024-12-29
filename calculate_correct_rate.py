import os
import pandas as pd
from datetime import datetime

parent_directory = os.path.abspath(os.path.join('calculate_correct_rate.py', '..'))
ai_prediction_file = os.path.join(parent_directory, 'data', 'experiment_data', 'task_ai_prediction', 'result.csv')
human_result_file = os.path.join(parent_directory, 'data', 'experiment_data', 'task_human_result', 'result.csv')
result_file = os.path.join(parent_directory, 'data', 'analysis_data', 'correct_answer_rate.csv')

#ai_predictionデータを読み込み
with open(ai_prediction_file, 'r', encoding='utf-8') as ai_data:
  lines = ai_data.readlines()
  test_ai_data = list(map(int, lines[1].strip().split(',')[:15]))
  ai_data1 = test_ai_data[:5] #会話の履歴だけ条件
  ai_data2 = test_ai_data[5:10] #ビッグファイブデータだけ条件
  ai_data3 = test_ai_data[10:] #両方条件

#human_resultデータを読み込み
with open(human_result_file, 'r', encoding='utf-8') as human_data:
  lines = human_data.readlines()
  test_human_data = list(map(int, lines[0].strip().split(',')[:5]))

#AIの正答率を計算
correct_rate = []
def calculate_correct_rate(ai_data):
  correct_count = 0
  for i in range(len(ai_data)):
    if ai_data[i] == test_human_data[i]:
      correct_count += 1
  correct_rate.append(round(correct_count/len(test_ai_data)*100, 2))

calculate_correct_rate(ai_data1)
calculate_correct_rate(ai_data2)
calculate_correct_rate(ai_data3)

#結果リストをcsvファイルに出力
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
output_data = correct_rate + [timestamp]
pd.DataFrame([output_data]).to_csv(result_file, index=False, header=False, mode="a")   
print(f"Results saved to {result_file}.")