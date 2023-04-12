from sqlalchemy import create_engine
from datetime import timedelta

import time
#time.tzset()

import pandas as pd

# db 연결
def db_conn():
    print('\n==================== db_conn() ======================')
    print('db conn...');

    start = time.time()

    # db 연결
    db_connection = create_engine('mysql+pymysql://root:!Wjd53850@113.131.145.133:3306/inpiniti')
    conn = db_connection.connect()

    print(f'db conn success : {timedelta(seconds=round(time.time() - start))}');
    print('==========================================\n')

    return conn

# 실제 테이블 종류 알아오기
def select(conn, sql_cmd):
    print('\n==================== select() ======================')
    print('Views : tables selecting...');

    start = time.time()

    # sql 조회
    #sql_cmd = f'SELECT MAX(table_name) table_name FROM inpiniti.tables;'
    db_test = pd.read_sql(sql=sql_cmd, con=conn)

    print(f'table select success : {timedelta(seconds=round(time.time() - start))}');
    print('==========================================\n')

    # pandas 생성
    df = pd.DataFrame(db_test)

    return df