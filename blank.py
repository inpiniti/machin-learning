import pandas as pd
#import psycopg2.extras
#from sqlalchemy import create_engine

import pymysql
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

#conn = psycopg2.connect(host='192.168.55.115', user='aistudy', password='aistudy', dbname='2022_aistudy', port=30432)

#engine = create_engine('postgresql://aistudy:aistudy@192.168.55.115:30432/2022_aistudy')
#conn2 = engine.connect()

#db_test = pd.read_sql_table('titanic', conn2)

#pd.DataFrame(db_test)

# 한시간 후
def after_one_hour(now):
    return now + timedelta(hours=1)

# 특정 종목 한 시간 후 데이터
def stock_after_one_hour(stock):
  condition = (df.stock == stock) # 조건식 작성
  df2 = df.loc[condition]
  df2.reset_index(drop=True, inplace=True)

  print(df2)

  for idx, (createTime, current) in enumerate(zip(df2['createTime'], df2['current'])):
      condition3 = df2.createTime == after_one_hour(createTime)
      df3 = df2.loc[condition3]
      if df3.shape[0] != 0:
        df2.at[idx, 'test'] = df3.iloc[0]['current']

  print(df2.dropna(axis=0))

db_connection = create_engine('mysql+pymysql://inpiniti:!Wjd53850@mysql-5.mysql.database.azure.com:3306/mysql')
conn = db_connection.connect()
db_test = pd.read_sql(text("""
SELECT *
  FROM inpiniti.investing20220510;
"""), conn)
df = pd.DataFrame(db_test)

# 유일값
for stock in df['stock'].unique():
  stock_after_one_hour(stock)

#conn=pymysql.connect(host='mysql-5.mysql.database.azure.com',port=3306,user='inpiniti',password='!Wjd53850',db='mysql')
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