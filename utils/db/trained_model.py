import mysql.connector
import json
from decimal import Decimal

# trained_model 테이블에서 데이터를 조회하여 dataframe 으로 반환
def get_trained_model_dataframe():
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
        SELECT id, `algorithm`, accuracy
        FROM `python-inpiniti`.trained_model;
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
    #df = pd.DataFrame(json_data)

    # 연결 종료
    cursor.close()
    conn.close()

    return json.dumps(json_data, default=decimal_default)

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError