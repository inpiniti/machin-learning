import mysql.connector

def save_financials_to_db(financial):
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
        INSERT INTO financials (
            year, sales, operatingProfit, netIncome, operatingProfitRatio,
            netProfitRatio, code, symbolCode, name, 
            sectorCode, sectorName
        ) VALUES (
            %(year)s, %(sales)s, %(operatingProfit)s, %(netIncome)s, %(operatingProfitRatio)s,
            %(netProfitRatio)s, %(code)s, %(symbolCode)s, %(name)s, 
            %(sectorCode)s, %(sectorName)s
        )
    """

    # 데이터 삽입
    #for financial in financials:
    cursor.execute(insert_query, financial)

    # 변경사항 저장
    conn.commit()

    # 연결 종료
    cursor.close()
    conn.close()