import mysql.connector

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