from tkinter.messagebox import NO
import joblib
import pandas as pd
import os
import time

import schedule

from sqlalchemy import create_engine, text
from datetime import timedelta, datetime

db_test = None

conn = None

true_cnt = 0
false_cnt = 0
all_cnt = 0
files = None

result = None

# db 연결
def db_conn():
  print('\n==================== db_conn() ======================')
  print('db conn...');

  start = time.time()

  # db 연결
  db_connection = create_engine('mysql+pymysql://inpiniti:!Wjd53850@localhost:3306/inpiniti')
  conn = db_connection.connect()

  print(f'db conn success : {timedelta(seconds=round(time.time() - start))}');
  print('==========================================\n')

  return conn

# 실제 테이블 종류 알아오기
def select():
  global conn

  conn = db_conn()
  print('\n==================== select() ======================')
  print('Views : tables selecting...');

  start = time.time()

  # sql 조회
  sql_cmd = f'SELECT MAX(table_name) table_name FROM inpiniti.tables;'
  db_test = pd.read_sql(sql=sql_cmd, con=conn)

  print(f'table select success : {timedelta(seconds=round(time.time() - start))}');
  print('==========================================\n')

  # pandas 생성
  df = pd.DataFrame(db_test)

  return df

# 예측하기
def predict(file_name, df):
    #print('\n==================== predict() ======================')
    #print(f'file name : {file_name}')
    classifier = joblib.load(f'./classifier/{file_name}')
    #print(f'classifier : {classifier}')

    # "a", "b", "changeRate", "score"
    # 예측

    global true_cnt, false_cnt

    result = classifier.predict(df)
    if result[0]:
        true_cnt += 1
    else :
        false_cnt += 1
    #print('==========================================\n')

# 파일 반복
def check_learned_file_exists(fn, df):
  global all_cnt, files
  if all_cnt == 0:
    dir = './classifier'
    files = os.listdir(dir)
    all_cnt = len(files)

  #파일명 출력하기
  for file_name in files :
    fn(file_name, df)

# 파일 반복 (거꾸로 5번)
def check_learned_file_exists_reversed(fn, df):
  global all_cnt, files
  if all_cnt == 0:
    dir = './classifier'
    files = os.listdir(dir)
    all_cnt = len(files)

  #파일명 출력하기
  i = 0
  for file_name in reversed(files) :
    if i < 5:
      fn(file_name, df)
    i += 1

def table_select(table_name):
  print('\n==================== table_select() ======================')
  print(f'table {table_name} selecting...');

  global conn

  start = time.time()

  today = datetime.today().strftime('%Y%m%d')
  #today = '20221014'

  # sql 조회
  sql_cmd = f"""
  select *
  from ( select 
            cast(createTime as char(19)) createTime, 
            `current` , 
            high , 
            low , 
            changePrice , 
            changeRate , 
            tradingVolume , 
            cast(TIMEDIFF(DATE_FORMAT(now(), '%H:%i:%s'), tradeTime) as char(8)) tradeTime, 
            score , 
            stock 
          from inpiniti.investing{today}
          where createTime = ( select max(createTime) 
                                from inpiniti.investing{today})
        ) a
  where tradeTime < '00:20:00'"""
  print(sql_cmd)
  db_test = pd.read_sql(sql=text(sql_cmd), con=conn)

  print(f'table select success : {timedelta(seconds=round(time.time() - start))}');

  print('==========================================\n')
  return db_test

def start():
    # 테이블 종류
    row_1 = select()

    # 첫번째 테이블의 테이블 명
    table_1 = row_1.iloc[0]['table_name']

    # 테이블 가져 오기
    inpiniti_df = table_select(table_1)

    print('==================== inpiniti_df ====================')
    print(inpiniti_df)

    inpiniti_df['a'] = (round(inpiniti_df['current']/inpiniti_df['high'], 2) * 100).astype(int)
    inpiniti_df['b'] = (round(inpiniti_df['current']/inpiniti_df['low'], 2) * 100).astype(int)

    ##columns = ["a", "b", "changeRate", "score"]
    #print('\n==================== inpiniti_df["c"] bb ======================')
    #startdt = time.time()
    #inpiniti_df["c"] = inpiniti_df[['a', 'b', 'changeRate', 'score']].apply(bb, axis = 1)
    #print(f'table select success : {timedelta(seconds=round(time.time() - startdt))}');
    #print('==========================================\n')
    #print(inpiniti_df['c'].sort_values(ascending=False))

    #print(inpiniti_df.sort_values(by=['c'], ascending=False))

    #is_100 = inpiniti_df['c'] == '100%'
    #is_80 = inpiniti_df['c'] == '80%'
    #predict10 = inpiniti_df[is_100 | is_80]

    #print(predict10)

    print('\n==================== inpiniti_df["d"] aa ======================')
    startdt = time.time()

    inpiniti_df["d"] = inpiniti_df[['a', 'b', 'changeRate', 'score']].apply(aa, axis = 1)
    print(f'table select success : {timedelta(seconds=round(time.time() - startdt))}');
    print('==========================================\n')

    global result
    result = inpiniti_df.sort_values(by=['d'], ascending=False)

    start()
    #return inpiniti_df.sort_values(by=['d'], ascending=False)

# 예측 단축
def aa(passenger):
  a, b, changeRate, score = passenger

  global true_cnt, false_cnt

  data = [{'a': a, 'b': b, 'changeRate': changeRate, 'score': score}]

  true_cnt = 0
  false_cnt = 0

  check_learned_file_exists(predict, pd.DataFrame(data))

  #print(pd.DataFrame(data))

  #print(f'true_cnt : {true_cnt}')
  #print(f'false_cnt : {false_cnt}')
  #print(f'all_cnt : {all_cnt}')

  #print(f'{round(true_cnt/all_cnt*100)}% - {true_cnt}/{all_cnt}')

  return f'{round(true_cnt/all_cnt*100)}'

# 예측
def bb(passenger):
  a, b, changeRate, score = passenger

  global true_cnt, false_cnt

  data = [{'a': a, 'b': b, 'changeRate': changeRate, 'score': score}]

  true_cnt = 0
  false_cnt = 0

  check_learned_file_exists_reversed(predict, pd.DataFrame(data))

  #print(pd.DataFrame(data))

  #print(f'true_cnt : {true_cnt}')
  #print(f'false_cnt : {false_cnt}')
  #print(f'all_cnt : {all_cnt}')

  #print(f'{round(true_cnt/all_cnt*100)}% - {true_cnt}/{all_cnt}')

  return f'{round(true_cnt/5*100)}'

def getResult():
  global result

  return result
#start()