import pickle
import mysql.connector
import json
from decimal import Decimal

import pandas as pd

# 페이지 번호를 기반으로 LIMIT와 OFFSET을 계산하여 반환
def calculate_limit_offset(page):
    limit = 100
    offset = (page - 1) * limit
    return limit, offset

def save_dart_to_db(df):
    # MySQL 연결 정보
    config = {
        'user': 'root',
        'password': '!Wjd53850',
        'host': '110.46.192.54',
        'database': 'python-inpiniti'
    }

    # MySQL 연결
    conn = mysql.connector.connect(**config)

    # 커서 생성
    cursor = conn.cursor()

    # 데이터 삽입 쿼리
    insert_query = """
        INSERT INTO dart (
            `year`, 
            `month`, 
            isu_abbrv, 
            isu_srt_cd, 
            mkt_nm, 
            sales, 
            sales_change_3, 
            sales_change_6, 
            sales_change_9, 
            sales_change_12, 
            operating_profit, 
            operating_profit_change_3, 
            operating_profit_change_6, 
            operating_profit_change_9, 
            operating_profit_change_12, 
            net_profit, 
            net_profit_change_3, 
            net_profit_change_6, 
            net_profit_change_9, 
            net_profit_change_12, 
            mmend_clsprc, 
            mmend_clsprc_change_3, 
            mmend_clsprc_change_6, 
            mmend_clsprc_change_9, 
            mmend_clsprc_change_12, 
            next_mmend_clsprc_change
        ) VALUES (
            %(year)s, 
            %(month)s, 
            %(isu_abbrv)s, 
            %(isu_srt_cd)s, 
            %(mkt_nm)s, 
            %(sales)s, 
            %(sales_change_3)s, 
            %(sales_change_6)s, 
            %(sales_change_9)s, 
            %(sales_change_12)s, 
            %(operating_profit)s, 
            %(operating_profit_change_3)s, 
            %(operating_profit_change_6)s, 
            %(operating_profit_change_9)s, 
            %(operating_profit_change_12)s, 
            %(net_profit)s, 
            %(net_profit_change_3)s, 
            %(net_profit_change_6)s, 
            %(net_profit_change_9)s, 
            %(net_profit_change_12)s, 
            %(mmend_clsprc)s, 
            %(mmend_clsprc_change_3)s, 
            %(mmend_clsprc_change_6)s, 
            %(mmend_clsprc_change_9)s, 
            %(mmend_clsprc_change_12)s, 
            %(next_mmend_clsprc_change)s
        );
    """

    print("Number of placeholders in insert_query:", insert_query.count("%"))
    print("Number of columns in df:", len(df.columns))

    data = df.to_dict('records')
    cursor.executemany(insert_query, data)

    # 변경사항 저장
    conn.commit()

    # 연결 종료
    cursor.close()
    conn.close()

def get_dart_to_dataframe():

    # 학습을 위해 `year`, `month`, isu_abbrv, isu_srt_cd, mkt_nm, sales 이 필드는 뺌
    # 'mmend_clsprc', 'net_profit' 'operating_profit' 이 3개 필드도
    query = """
    SELECT sales_change_3, sales_change_6, sales_change_9, sales_change_12, 
    operating_profit_change_3, operating_profit_change_6, operating_profit_change_9, operating_profit_change_12, 
    net_profit_change_3, net_profit_change_6, net_profit_change_9, net_profit_change_12, 
    mmend_clsprc_change_3, mmend_clsprc_change_6, mmend_clsprc_change_9, mmend_clsprc_change_12, 
    next_mmend_clsprc_change
    FROM `python-inpiniti`.dart;
    """

    return select_db(query)

def save_financials_to_db(financial):

    #print('save_financials_to_db start')

    # MySQL 연결 정보
    config = {
        'user': 'root',
        'password': '!Wjd53850',
        'host': '110.46.192.54',
        'database': 'python-inpiniti'
    }

    # MySQL 연결
    conn = mysql.connector.connect(**config)

    #print('mysql connected')

    # 커서 생성
    cursor = conn.cursor()

    # 데이터 삽입 쿼리
    insert_query = """
        INSERT INTO financials (
            year, sales, operatingProfit, netIncome, operatingProfitRatio,
            netProfitRatio, prevSales, prevOperatingProfit, prevNetIncome, prevOperatingProfitRatio,
            prevNetProfitRatio, salesChange, operatingProfitChange, netIncomeChange, operatingProfitRatioChange,
            netProfitRatioChange, trdDd, isuAbbrv, isuSrtCd, mktNm, mmendClsprc, hgstClsprc, lwstClsprc,
            isuStd, isuKurt, coskew, isuBeta, isuAmibud, isuZeros, mmAccTrdvol, avgAccTrdvol,
            mmAccTrdval, avgAccTrdval, nextmmendclsprc, mmendclsprcchange, code, symbolCode, name, sectorCode,
            sectorName
        ) VALUES (
            %(year)s, %(sales)s, %(operatingprofit)s, %(netincome)s, %(operatingprofitratio)s,
            %(netprofitratio)s, %(prevsales)s, %(prevoperatingprofit)s, %(prevnetincome)s, %(prevoperatingprofitratio)s,
            %(prevnetprofitratio)s, %(saleschange)s, %(operatingprofitchange)s, %(netincomechange)s, %(operatingprofitratiochange)s,
            %(netprofitratiochange)s, %(trdDd)s, %(isuAbbrv)s, %(isuSrtCd)s, %(mktNm)s, %(mmendClsprc)s, %(hgstClsprc)s,
            %(lwstClsprc)s, %(isuStd)s, %(isuKurt)s, %(coskew)s, %(isuBeta)s, %(isuAmibud)s, %(isuZeros)s,
            %(mmAccTrdvol)s, %(avgAccTrdvol)s, %(mmAccTrdval)s, %(avgAccTrdval)s, %(nextmmendclsprc)s, %(mmendclsprcchange)s,
            %(code)s, %(symbolCode)s, %(name)s, %(sectorCode)s, %(sectorName)s
        )        
    """

    #print('insert_query created')

    #print(financial)

    # 숫자데이터에 쉼표 제거
    for key, value in financial.items():
        if isinstance(value, str) and ',' in value:
            financial[key] = str(value.replace(',', ''))

    # 이상한 값  제거
    if financial['coskew'] == '-':
        financial['coskew'] = 0

    if not financial.get('nextmmendclsprc'):
        financial['nextmmendclsprc'] = 0

    if not financial.get('prevsales'):
        financial['prevsales'] = 0

    if not financial.get('prevoperatingprofit'):
        financial['prevoperatingprofit'] = 0
    if financial.get('prevoperatingprofit') is None:
        financial['prevoperatingprofit'] = 0

    if not financial.get('mmendclsprcchange'):
        financial['mmendclsprcchange'] = 0
    if financial.get('mmendclsprcchange') is None:
        financial['mmendclsprcchange'] = 0

    if not financial.get('prevnetincome'):
        financial['prevnetincome'] = 0
    if financial.get('prevnetincome') is None:
        financial['prevnetincome'] = 0
    
    if not financial.get('prevoperatingprofitratio'):
        financial['prevoperatingprofitratio'] = 0
    if financial.get('prevoperatingprofitratio') is None:
        financial['prevoperatingprofitratio'] = 0

    if not financial.get('prevnetprofitratio'):
        financial['prevnetprofitratio'] = 0
    if financial.get('prevnetprofitratio') is None:
        financial['prevnetprofitratio'] = 0

    if not financial.get('saleschange'):
        financial['saleschange'] = 0
    if financial.get('saleschange') is None:
        financial['saleschange'] = 0

    if not financial.get('operatingprofitchange'):
        financial['operatingprofitchange'] = 0
    if financial.get('operatingprofitchange') is None:
        financial['operatingprofitchange'] = 0
        
    # 데이터 삽입
    #for financial in financials:
    query_with_values = insert_query % financial
    #print('---------------------')
    #print(query_with_values)
    #print('---------------------')
    cursor.execute(insert_query, financial)

    #print('insert_query executed')

    # 변경사항 저장
    conn.commit()

    # 연결 종료
    cursor.close()
    conn.close()

def get_latest_date_from_financials():
    # MySQL 연결 정보
    config = {
        'user': 'root',
        'password': '!Wjd53850',
        'host': '110.46.192.54',
        'database': 'python-inpiniti'
    }

    # MySQL 연결
    conn = mysql.connector.connect(**config)

    #print('mysql connected')

    # 커서 생성
    cursor = conn.cursor()

    # 데이터 삽입 쿼리
    select_query = """
        SELECT MAX(year) FROM financials;
    """

    cursor.execute(select_query)

    # 쿼리 결과 읽기
    latest_date = cursor.fetchone()[0]

    # 변경사항 저장
    conn.commit()

    # 연결 종료
    cursor.close()
    conn.close()

    return latest_date

# 날짜로 데이터를 조회 year
# mktNm
# name like
# sectorCode
# stock (symbolCode)
# page
def fetch_data_by_latest_date(year, mktNm, name, sectorCode, symbolCode, page):
    # MySQL 연결 정보
    config = {
        'user': 'root',
        'password': '!Wjd53850',
        'host': '110.46.192.54',
        'database': 'python-inpiniti'
    }

    # MySQL 연결
    conn = mysql.connector.connect(**config)

    # 커서 생성
    cursor = conn.cursor()

    # LIMIT와 OFFSET을 사용하여 페이징 처리를 합니다.
    limit, offset = calculate_limit_offset(page)

    # 데이터 삽입 쿼리
    select_query = """
        SELECT *
        FROM financials 
        WHERE (year = %s OR %s IS NULL OR %s = '')
        AND (mktNm = %s OR %s IS NULL OR %s = '')
        AND (name LIKE CONCAT('%', %s, '%') OR %s IS NULL OR %s = '')
        AND (sectorCode = %s OR %s IS NULL OR %s = '')
        AND (symbolCode = %s OR %s IS NULL OR %s = '')
        LIMIT %s OFFSET %s;
    """

    cursor.execute(select_query, (year, year, year, mktNm, mktNm, mktNm, name, name, name, sectorCode, sectorCode, sectorCode, symbolCode, symbolCode, symbolCode, limit, offset))

    # 쿼리 결과 읽기
    latest_date_data = cursor.fetchall()

    # 컬럼 이름 가져오기
    column_names = [desc[0] for desc in cursor.description]

    # JSON 형식으로 변환
    json_data = {'data_list': []}
    for row in latest_date_data:
        json_data['data_list'].append(dict(zip(column_names, row)))

    # 전체 페이지 수도 조회
    select_query = """
        SELECT COUNT(*)
        FROM financials 
        WHERE (year = %s OR %s IS NULL OR %s = '')
        AND (mktNm = %s OR %s IS NULL OR %s = '')
        AND (name LIKE CONCAT('%', %s, '%') OR %s IS NULL OR %s = '')
        AND (sectorCode = %s OR %s IS NULL OR %s = '')
        AND (symbolCode = %s OR %s IS NULL OR %s = '');
    """

    cursor.execute(select_query, (year, year, year, mktNm, mktNm, mktNm, name, name, name, sectorCode, sectorCode, sectorCode, symbolCode, symbolCode, symbolCode))

    # 쿼리 결과 읽기
    total_count = cursor.fetchone()[0]

    # json_data 에 total_count 추가
    json_data['total_count'] = total_count

    # 연결 종료
    cursor.close()
    conn.close()

    return json.dumps(json_data, default=decimal_default)

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError


# financials 테이블에서 데이터를 조회하여 dataframe 으로 반환
def get_financials_dataframe():
    # MySQL 연결 정보
    config = {
        'user': 'root',
        'password': '!Wjd53850',
        'host': '110.46.192.54',
        'database': 'python-inpiniti'
    }

    # MySQL 연결
    conn = mysql.connector.connect(**config)

    # 커서 생성
    cursor = conn.cursor()

    # 데이터 삽입 쿼리
    select_query = """
        select 
            saleschange, #: string; // 매출 변동
            operatingprofitchange, #: string; // 영업이익 변동
            netincomechange, #: string; // 순이익 변동
            operatingprofitratiochange, #: string; // 영업이익률 변동
            netprofitratiochange, #: string; // 순이익률 변동
            mmendclsprcchange #: string; // 월말 종가 변동
        from financials f 
        where nextmmendclsprc != 0;
    """

    cursor.execute(select_query)

    # 쿼리 결과 읽기
    latest_date_data = cursor.fetchall()

    # 컬럼 이름 가져오기
    column_names = [desc[0] for desc in cursor.description]

    # JSON 형식으로 변환
    json_data = []
    for row in latest_date_data:
        json_data.append(dict(zip(column_names, row)))

    # DataFrame 객체로 변환
    df = pd.DataFrame(json_data)

    # 연결 종료
    cursor.close()
    conn.close()

    return df

# 학습한 모델 저장
# CREATE TABLE trained_model (
#    id INT AUTO_INCREMENT PRIMARY KEY,
#    model BLOB,
#    algorithm VARCHAR(255),
#    accuracy FLOAT
#);
def save_trained_model(model, algorithm, accuracy):
    # 모델 직렬화 및 바이트 배열로 변환
    serialized_model = pickle.dumps(model)

    # MySQL 연결 정보
    config = {
        'user': 'root',
        'password': '!Wjd53850',
        'host': '110.46.192.54',
        'database': 'python-inpiniti'
    }

    # MySQL 데이터베이스에 연결
    conn = mysql.connector.connect(**config)

    # 커서 생성
    cursor = conn.cursor()

    # trained_model 테이블에 모델 저장 (테이블이 이미 존재한다고 가정)
    query = f"INSERT INTO trained_model (model, algorithm, accuracy) VALUES (%s, %s, %s)"
    cursor.execute(query, (serialized_model, algorithm, accuracy,))

    # 변경사항 커밋
    conn.commit()

    # 연결 종료
    conn.close()

def predict_with_saved_model(data, model_id):
    # MySQL 연결 정보
    config = {
        'user': 'root',
        'password': '!Wjd53850',
        'host': '110.46.192.54',
        'database': 'python-inpiniti'
    }

    # MySQL 데이터베이스에 연결
    conn = mysql.connector.connect(**config)

    # 커서 생성
    cursor = conn.cursor()

    # trained_model 테이블에서 모델 검색 (테이블이 이미 존재한다고 가정)
    query = f"SELECT model FROM trained_model WHERE id = %s"
    cursor.execute(query, (model_id,))

    # 검색된 모델을 Python 객체로 역직렬화
    model_data = cursor.fetchone()[0]

    model = pickle.loads(model_data)

    # 연결 종료
    conn.close()

    # 모델을 사용하여 새로운 데이터에 대한 예측 수행
    prediction = model.predict(data)

    return prediction

def select_db(query):
    # MySQL 연결 정보
    config = {
        'user': 'root',
        'password': '!Wjd53850',
        'host': '110.46.192.54',
        'database': 'python-inpiniti'
    }

    # MySQL 연결
    conn = mysql.connector.connect(**config)

    # 커서 생성
    #cursor = conn.cursor()

    # 데이터 삽입 쿼리
    #cursor.execute(query)

    # Assuming `conn` is your database connection
    df = pd.read_sql_query(query, conn)

    # 쿼리 결과 읽기
    #latest_date_data = cursor.fetchall()

    # 컬럼 이름 가져오기
    #column_names = [desc[0] for desc in cursor.description]

    # JSON 형식으로 변환
    #json_data = []
    #for row in latest_date_data:
    #    json_data.append(dict(zip(column_names, row)))

    # DataFrame 객체로 변환
    #df = pd.DataFrame(json_data)


    # 변경사항 저장
    conn.commit()

    # 연결 종료
    #cursor.close()
    conn.close()

    return df

# db에 insert 하는 함수
def insert_db(query):
    # MySQL 연결 정보
    config = {
        'user': 'root',
        'password': '!Wjd53850',
        'host': '110.46.192.54',
        'database': 'python-inpiniti'
    }

    # MySQL 연결
    conn = mysql.connector.connect(**config)

    # 커서 생성
    cursor = conn.cursor()

    # 데이터 삽입 쿼리
    cursor.execute(query)

    # 변경사항 커밋
    conn.commit()

    # 연결 종료
    cursor.close()
    conn.close()