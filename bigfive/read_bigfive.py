import os
import pandas as pd

parent_directory = os.path.abspath(os.path.join('read_bigfive.py', '..'))
bigfive_directory = os.path.join(parent_directory, 'data', 'experiment_data', 'bigfive_data')
bigfive_file_list = os.listdir(bigfive_directory)

id = 1 #仮
bigfive_csv = os.path.join(bigfive_directory, bigfive_file_list[id-1])


#ビッグファイブのcsvファイルを読み取りLOW・MEDIUM・HIGHでリスト化
qualtrics_data = pd.read_csv(bigfive_csv, header=None)
#最後の10項目の数字の羅列(ビッグファイブの結果）だけ取得
answer = qualtrics_data.iloc[-1, -11:-1]
answer_list = answer.astype(int).tolist()

#ビッグファイブのMEDIUMの範囲を平均 ± 標準偏差として定義する。
#外向性は7.83±2.97、協調性は9.48±2.16、勤勉性は6.14±2.41、神経症傾向は9.21±2.48、開放性は8.03±2.48
medium_range = [[4.86, 10.8], [7.32, 11.64], [3.73, 8.55], [6.73, 11.69], [5.55, 10.51]]

#ビッグファイブをHIGH,MEDIUM,LOWに評価
def score_bigfive(data):
  bigfive_list = []
  #計算方法は、参考になった論文のマニュアルから
  for i in range(5):
    #外向性、協調性、勤勉性、神経症傾向、開放性の順に入れる
    bigfive_list.append(data[i]+data[i+5]) 
  
  prompt_bigfive = []
  for i in range(5):
    if bigfive_list[i] > medium_range[i][1]:
      prompt_bigfive.append('HIGH')
    elif bigfive_list[i] >= medium_range[i][0]:
      prompt_bigfive.append('MEDIUM')
    else:
      prompt_bigfive.append('LOW')

  return prompt_bigfive


prompt_bigfive = score_bigfive(answer_list)