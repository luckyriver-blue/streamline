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

#ビッグファイブをHIGH,MEDIUM,LOWに評価
def score_bigfive(data, medium_range=(7, 9)):
  bigfive_list = []
  #計算方法は、参考になった論文のマニュアルから
  for i in range(5):
    #外向性、協調性、勤勉性、神経症傾向、開放性の順に入れる
    bigfive_list.append(data[i]+data[i+5]) 
  
  #とりあえずMEDIUMを7以上9以下として出す。
  prompt_bigfive = []
  for score in bigfive_list:
    if score > medium_range[1]:
      prompt_bigfive.append('HIGH')
    elif score >= medium_range[0]:
      prompt_bigfive.append('MEDIUM')
    else:
      prompt_bigfive.append('LOW')

  return prompt_bigfive


prompt_bigfive = score_bigfive(answer_list)