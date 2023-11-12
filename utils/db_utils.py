import mysql.connector
import json
from decimal import Decimal

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
def fetch_data_by_latest_date(year, mktNm, name, sectorCode, symbolCode):
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
        SELECT *
        FROM financials 
        WHERE (year = %s OR %s IS NULL OR %s = '')
        AND (mktNm = %s OR %s IS NULL OR %s = '')
        AND (name LIKE %s OR %s IS NULL OR %s = '')
        AND (sectorCode = %s OR %s IS NULL OR %s = '')
        AND (symbolCode = %s OR %s IS NULL OR %s = '');
    """

    cursor.execute(select_query, (year, year, year, mktNm, mktNm, mktNm, name, name, name, sectorCode, sectorCode, sectorCode, symbolCode, symbolCode, symbolCode, ))

    # 쿼리 결과 읽기
    latest_date_data = cursor.fetchall()

    # 컬럼 이름 가져오기
    column_names = [desc[0] for desc in cursor.description]

    # JSON 형식으로 변환
    json_data = []
    for row in latest_date_data:
        json_data.append(dict(zip(column_names, row)))

    # 연결 종료
    cursor.close()
    conn.close()

    return json.dumps(json_data, default=decimal_default)

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError