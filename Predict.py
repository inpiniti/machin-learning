from tkinter.messagebox import NO
import joblib
import pandas as pd
import os
import time

from sqlalchemy import create_engine, text
from datetime import timedelta, datetime

class Predict:
    db_test = None
    conn = None
    true_cnt = 0
    false_cnt = 0
    all_cnt = 0
    files = None
    result = None

    # db 연결
    def db_conn(self):
        print('\n==================== db_conn() ======================')
        print('db conn...');

        start = time.time()

        # db 연결
        db_connection = create_engine('mysql+pymysql://root:!Wjd53850@113.131.152.55:3306/inpiniti')
        conn = db_connection.connect()

        print(f'db conn success : {timedelta(seconds=round(time.time() - start))}');
        print('==========================================\n')

        return conn

    # 실제 테이블 종류 알아오기
    def select(self):
        self.conn = self.db_conn()
        print('\n==================== select() ======================')
        print('Views : tables selecting...');

        start = time.time()

        # sql 조회
        sql_cmd = f'SELECT MAX(table_name) table_name FROM inpiniti.tables;'
        db_test = pd.read_sql(sql=sql_cmd, con=self.conn)

        print(f'table select success : {timedelta(seconds=round(time.time() - start))}');
        print('==========================================\n')

        # pandas 생성
        df = pd.DataFrame(db_test)

        return df

    # 예측하기
    def predict(self, file_name, df):
        #print('\n==================== predict() ======================')
        #print(f'file name : {file_name}')
        classifier = joblib.load(f'./classifier/{file_name}')
        #print(f'classifier : {classifier}')

        # "a", "b", "changeRate", "score"
        # 예측

        result = classifier.predict(df)
        if result[0]:
            self.true_cnt += 1
        else :
            self.false_cnt += 1
        #print('==========================================\n')

    # 파일 반복
    def check_learned_file_exists(self, fn, df):
        if self.all_cnt == 0:
            dir = './classifier'
            self.files = os.listdir(dir)
            self.all_cnt = len(self.files)

        #파일명 출력하기
        for file_name in self.files :
            fn(file_name, df)

    # 파일 반복 (거꾸로 5번)
    def check_learned_file_exists_reversed(self, fn, df):
        if self.all_cnt == 0:
            dir = './classifier'
            self.files = os.listdir(dir)
            all_cnt = len(self.files)

        #파일명 출력하기
        i = 0
        for file_name in reversed(self.files) :
            if i < 5:
                fn(file_name, df)
            i += 1

    def table_select(self, table_name, arr = []):
        print('\n==================== table_select() ======================')
        print(f'table {table_name} selecting...');

        start = time.time()
        today = datetime.today().strftime('%Y%m%d')
        #today = '20221014'

        sql_add = ""

        if len(arr) != 0:
            str = '\",\"'
            arr_str = str.join(arr)
            arr_str = arr_str.replace(",", str)
            sql_add = f'and stock in ("{arr_str}")'

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
                    substr(cast(TIMEDIFF(DATE_FORMAT(now(), '%H:%i:%s'), tradeTime) as char(9)), 1, 8) tradeTime,
                    score , 
                    stock 
                from inpiniti.investing{today}
                where createTime = ( select max(createTime) 
                                        from inpiniti.investing{today})
                ) a
        where tradeTime < '00:20:00'
        #where stock like ("%삼%")
        {sql_add}"""
        print(sql_cmd)
        db_test = pd.read_sql(sql=text(sql_cmd), con=self.conn)

        print(f'table select success : {timedelta(seconds=round(time.time() - start))}');

        print('==========================================\n')
        return db_test

    def start(self):
        # 테이블 종류
        row_1 = self.select()

        # 첫번째 테이블의 테이블 명
        table_1 = row_1.iloc[0]['table_name']

        # 테이블 가져 오기
        inpiniti_df = self.table_select(table_1)

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

        inpiniti_df["d"] = inpiniti_df[['a', 'b', 'changeRate', 'score']].apply(self.aa, axis = 1)
        print(f'table select success : {timedelta(seconds=round(time.time() - startdt))}');
        print('==========================================\n')

        self.result = inpiniti_df.sort_values(by=['d'], ascending=False)


        return self.result
        #return inpiniti_df.sort_values(by=['d'], ascending=False)

    def start2(self, arr):
        # 테이블 종류
        row_1 = self.select()

        # 첫번째 테이블의 테이블 명
        table_1 = row_1.iloc[0]['table_name']

        # 테이블 가져 오기
        inpiniti_df = self.table_select(table_1, arr)

        print('==================== inpiniti_df ====================')
        print(inpiniti_df)

        inpiniti_df['a'] = (round(inpiniti_df['current']/inpiniti_df['high'], 2) * 100).astype(int)
        inpiniti_df['b'] = (round(inpiniti_df['current']/inpiniti_df['low'], 2) * 100).astype(int)

        print('\n==================== inpiniti_df["d"] aa ======================')
        startdt = time.time()

        inpiniti_df["d"] = inpiniti_df[['a', 'b', 'changeRate', 'score']].apply(self.aa, axis = 1)
        print(f'table select success : {timedelta(seconds=round(time.time() - startdt))}');
        print('==========================================\n')

        return inpiniti_df.sort_values(by=['d'], ascending=False)

    # 예측 단축
    def aa(self, passenger):
        a, b, changeRate, score = passenger

        data = [{'a': a, 'b': b, 'changeRate': changeRate, 'score': score}]

        self.true_cnt = 0
        self.false_cnt = 0

        self.check_learned_file_exists(self.predict, pd.DataFrame(data))

        #print(pd.DataFrame(data))

        #print(f'true_cnt : {true_cnt}')
        #print(f'false_cnt : {false_cnt}')
        #print(f'all_cnt : {all_cnt}')

        #print(f'{round(true_cnt/all_cnt*100)}% - {true_cnt}/{all_cnt}')

        return f'{round(self.true_cnt/self.all_cnt*100)}'

    # 예측
    def bb(self, passenger):
        a, b, changeRate, score = passenger

        data = [{'a': a, 'b': b, 'changeRate': changeRate, 'score': score}]

        self.true_cnt = 0
        self.false_cnt = 0

        self.check_learned_file_exists_reversed(self.predict, pd.DataFrame(data))

        #print(pd.DataFrame(data))

        #print(f'true_cnt : {true_cnt}')
        #print(f'false_cnt : {false_cnt}')
        #print(f'all_cnt : {all_cnt}')

        #print(f'{round(true_cnt/all_cnt*100)}% - {true_cnt}/{all_cnt}')

        return f'{round(self.true_cnt/5*100)}'

    def getResult(self):
        return self.result