import os
import pandas as pd
from datetime import datetime
from bigfive.read_bigfive import prompt_bigfive 

parent_directory = os.path.abspath(os.path.join('calculate_correct_rate.py', '..'))
ai_prediction_file = os.path.join(parent_directory, 'data', 'experiment_data', 'task_ai_prediction', 'result.csv')
human_result_file = os.path.join(parent_directory, 'data', 'experiment_data', 'task_human_result', 'result.csv')
result_file = os.path.join(parent_directory, 'data', 'analysis_data', 'correct_answer_rate.csv')

#ai_predictionデータを読み込み
with open(ai_prediction_file, 'r', encoding='utf-8') as ai_data:
  lines = ai_data.readlines()
  test_ai_data = list(map(int, lines[1].strip().split(',')[:5]))

#human_resultデータを読み込み
with open(human_result_file, 'r', encoding='utf-8') as human_data:
  lines = human_data.readlines()
  test_human_data = list(map(int, lines[0].strip().split(',')[:5]))
print(test_ai_data, test_human_data)

#AIの正答率を計算
correct_count = 0

for i in range(len(test_ai_data)):
  if test_ai_data[i] == test_human_data[i]:
    correct_count += 1

correct_rate = correct_count/len(test_ai_data)*100

#結果リストをcsvファイルに出力
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
output_data = [correct_rate, timestamp]
pd.DataFrame([output_data]).to_csv(result_file, index=False, header=False, mode="a")   
print(f"Results saved to {result_file}.")