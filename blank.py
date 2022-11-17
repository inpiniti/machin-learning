# db 조회 후
# 파일이 만들어 져 있는지 먼저 체크 필요할듯..
# 데이터 별 조회 후
# 학습 후
# classifier 폴더에 저장
# blank_test 에서 저장된 것으로 테스트가 가능함.

import numpy as np
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TZ'] = 'Asia/Seoul'
import time
#time.tzset()
import psycopg2
#from sqlalchemy import create_engine

import pymysql
from sqlalchemy import create_engine, text
from datetime import timedelta, datetime, timezone

from sklearn.model_selection import cross_val_score

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier

import joblib

best_accuracy = 0 # 가장 좋은 알고리즘
best_model = None # 가장 좋은 모델
classifier_types = [ "KNN", "Gaussian Naive Bayes", "Decision Tree" ] # 알고리즘 리스트
#classifier_types = [ "Logistic Regression", "KNN", "Gaussian Naive Bayes", "Decision Tree", "Gradient Boost" ] # 알고리즘 리스트
date = None # 오늘 날짜
db_connection = None # db 연결 엔진?
conn = None # 실제 db 연결
df = None
X_train = None
X_test = None
y_train = None
y_test = None

def getKstTime():
  datetime_utc = datetime.utcnow()
  timezone_kst = timezone(timedelta(hours=9))
  datetime_kst = datetime_utc.astimezone(timezone_kst)
  return datetime_kst

# 학습된 파일이 있는지 확인
# def check_learned_file_exists(file_name):

# 현재 시간에서 한 시간 후의 시간 리턴
#ef after_one_hour(now):

# 특정 종목의 한 시간 후 데이터 리턴
#def stock_after_one_hour(stock):

# 예측하기
#def predict(data, type = "Logistic Regression"):

# db 연결
#def db_conn():

# 실제 로직 수행
#def business_logic():

# 실제 테이블 종류 알아오기
#def select():

# 학습된 파일이 있는지 확인
# in : 날짜
# out : true or false
def check_learned_file_exists(file_name):
  start = time.time()

  dir = './classifier'
  files = os.listdir(dir)
  
  #파일명 출력하기
  for file in files :
    if file.find(file_name) == 0:
      print(f'{file_name} file exists success : {timedelta(seconds=round(time.time() - start))}')
      return True

  print(f'{file_name} file exists fail : {timedelta(seconds=round(time.time() - start))}')
  return False

# 한시간 후
def after_one_hour(now):
    return now + timedelta(hours=1)

# 특정 종목 한 시간 후 데이터
def stock_after_one_hour(stock):
  condition = (df.stock == stock) # 조건식 작성
  df2 = df.loc[condition]
  df2.reset_index(drop=True, inplace=True)

  for idx, (createTime, current) in enumerate(zip(df2['createTime'], df2['current'])):
      condition3 = df2.createTime == after_one_hour(createTime)
      df3 = df2.loc[condition3]
      if df3.shape[0] != 0:
        df2 = df2.copy()
        df2.at[idx, 'test'] = df3.iloc[0]['current']

  df4 = df2.dropna(axis=0)

  return df4

# 예측하기
def replacement_verification(data, type = "Logistic Regression"):
  # 예측시 고려해야하는 데이터 a, b, changeRate
  # 그 외에 데이터는 제외 시킴
  columns = ["a", "b", "changeRate", "score"]
  df_x_data = data[columns]

  #if replacement_verificationtype == 1:
  df_y_data = data['hourlater']
  #else : 
  #  ycolumns = ["hourlater"]
  #  df_y_data = data[ycolumns]

  try:
    # 데이터 분할하기

    global X_train, X_test, y_train, y_test, best_accuracy, best_model

    X_train, X_test, y_train, y_test = train_test_split(df_x_data, df_y_data, 
                                                      test_size=0.2, random_state=11)

    print(f'\n==================== replacement_verification() ======================')
    print(f'predict : {date}')
    print(f'classifiers : {type}')
    print(f"time : {getKstTime().strftime('%Y-%m-%d %H:%M:%S')}")

    start = time.time()

    classifiers = {
        "Logistic Regression": LogisticRegression(random_state=0, solver="lbfgs", max_iter=10000),
        "KNN": KNeighborsClassifier(n_neighbors = 5, metric = "minkowski", p = 2),
        "Gaussian Naive Bayes": GaussianNB(),
        "Decision Tree": DecisionTreeClassifier(criterion = "entropy", random_state = 0),
        "Gradient Boost": GradientBoostingClassifier()
    }

    classifier = classifiers[type]

    # 교체 검증
    scores = cross_val_score(classifier, X_train, y_train, cv = 10)
    accuracy = np.mean(scores)
    min = np.min(scores)
    max = np.max(scores)

    if accuracy > best_accuracy:
              best_accuracy = accuracy
              best_model = (type, classifier)
    print(f"\nAccuracy: {accuracy}\nMin: {min}\nMax: {max}\n")
    print("Fitting on all data, predicting test data...\n")
    print('==========================================\n')

  except Exception as e:
    print(f'error : {e}')

def predict(predicttype = 1):
  print('\n==================== predict() ======================')
  start = time.time()

  global best_model

  print(f'best_model : {best_model}')

  type = best_model[0]
  classifier = best_model[1]

  # 학습
  classifier.fit(X_train, y_train)

  # 예측
  pred = classifier.predict(X_test)

  # 예측 정확도
  print('Prediction Accuracy : {0:.4f}'.format(accuracy_score(y_test,pred)))

  # 저장
  if predicttype == 1:
    joblib.dump(classifier, f'./classifier/{date}.pkl')
  else:
    joblib.dump(classifier, f'./classifier2/{date}.pkl')

  print(f'{type} {date} dump : {timedelta(seconds=round(time.time() - start))}')

  print('==========================================\n')

def db_conn():
  print('\n==================== db_conn() ======================')
  print('db conn...')

  start = time.time()

  global db_connection, conn

  # db 연결
  db_connection = create_engine('mysql+pymysql://root:!Wjd53850@113.131.152.55:3306/inpiniti')
  conn = db_connection.connect()

  print(f'db conn success : {timedelta(seconds=round(time.time() - start))}')
  print('==========================================\n')

def table_select():
  print('\n==================== table_select() ======================')
  print(f'table investing{date} selecting...')

  start = time.time()

  # sql 조회
  sql_cmd = f"SELECT * FROM inpiniti.investing{date} where tradeTime like '%:%';"
  db_test = pd.read_sql(sql=text(sql_cmd), con=conn)

  print(f'table select success : {timedelta(seconds=round(time.time() - start))}')

  print('==========================================\n')
  return db_test

# business logic
def business_logic(business_logictype = 1):
  db_test = table_select()

  print('\n==================== business_logic() ======================')

  global df, classifier_types, best_accuracy, best_model

  # pandas 생성
  df = pd.DataFrame(db_test)
  index = 0
  start = time.time()

  # 현재 날짜 찍어보기, 계산해야 되는 로우 찍어보기
  # 대략 시간 구하기
  print(f'current date : {date}')
  print(f'row cnt : {len(df.index)}')
  print(f'time taken : {timedelta(seconds=round(len(df.index)/1491))}')

  # 1시간 뒤의 값을 추가함
  for idx, (stock) in enumerate(df['stock'].unique()):
    if idx % 100 == 0:
      print(f'stock after 1 hour... : {str(idx).zfill(4)} / 1000 : {timedelta(seconds=round(time.time() - start))}')
    if index == 0:
      index = 1
      df2 = stock_after_one_hour(stock)
    #elif idx == 15:
    #  break
    else:
      df2 = pd.concat([df2, stock_after_one_hour(stock)])
  print(f'stock after 1 hour success : {timedelta(seconds=round(time.time() - start))}')
  print('==========================================\n')

  # 'test' 가 예측해야 되는 한 시간 뒤의 값인데 들어 있지 않은 경우도 존재하여 존재하지 않은 경우는 그냥 pass 하도록 if문을 넣어줌
  if 'test' in df2:
    # 한시간 뒤 비율 = 1보다 클수록 좋음
    #df2['hourlater'] = (round(df2['test']/df2['current'], 4) * 10000).astype(int) # 이게 예측해야 되는 값
    df2['hourlater'] = df2['test']/df2['current'] > 1
    df2['a'] = (round(df2['current']/df2['high'], 2) * 100).astype(int)
    df2['b'] = (round(df2['current']/df2['low'], 2) * 100).astype(int)

    # 2의 경우에는 얼마로 변할지를 예측함
    if business_logictype == 2:
      df2['hourlater'] = (round(df2['test']/df2['current'], 4) * 10000).astype(int) # 이게 예측해야 되는 값

    best_model = None
    best_accuracy = 0

    for classifier_type in classifier_types:
      replacement_verification(df2, classifier_type)

    predict(business_logictype)

# 실제 테이블 종류 알아오기
def select():
  db_conn()
  print('\n==================== select() ======================')
  print('Views : tables selecting...')

  start = time.time()

  # sql 조회
  sql_cmd = f'SELECT * FROM inpiniti.tables;'
  db_test = pd.read_sql(sql=sql_cmd, con=conn)

  print(f'table select success : {timedelta(seconds=round(time.time() - start))}')
  print('==========================================\n')

  # pandas 생성
  df = pd.DataFrame(db_test)

  return df

# 반복문 수행
def iter_loop(rating, fn):
  global date
  date = rating.strip('investing')
  fn()

def test():
  if not check_learned_file_exists(date):
    business_logic(2)
  else :
    print(f"'{date}' This day's learning has already been completed.")


def start_learning():
  print('\n==========================================')
  print('program start')
  print('==========================================\n')

  # 테이블 종류
  tables_df = select()

  print(tables_df)

  # 테이블 종류만큼 반복
  for idx, row in tables_df.iterrows():
    iter_loop(row['table_name'], test)


#conn=pymysql.connect(host='localhost',port=3306,user='inpiniti',password='!Wjd53850',db='mysql')
#sql="SELECT * FROM inpiniti.investing LIMIT 0,10"

#df = pd.read_sql(sql,conn)

# 데이터가 너무 많아, 데이터를 나누기 위한 sql
# create table if not exists investing20220509
# select *
#   from inpiniti.investing
# where createTime like '2022-05-09%';
#  
# delete from inpiniti.investing
#  where createTime like '2022-05-09%';