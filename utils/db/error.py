import datetime
from utils.db_utils import insert_db

# 에러 테이블 생성
# CREATE TABLE error (
#     id INT AUTO_INCREMENT,
#     func_name VARCHAR(255),
#     args TEXT,
#     reason TEXT,
#     time TIMESTAMP,
#     PRIMARY KEY (id)
# );

# 에러가 났을때, 에러가 발생한 함수, 인자값, 원인, 시간을 db에 저장하는 함수
def save_error(func_name, args, reason):
    # 현재 시간
    now = datetime.datetime.now()

    # reason 문자열에 '가 있으면 에러가 발생함
    if "'" in str(reason):
        reason = str(reason).replace("'", "")

    # sql문
    sql = f"""
        INSERT INTO error (func_name, args, reason, time)
        VALUES ('{func_name}', '{args}', '{reason}', '{now}')
    """

    print('sql', sql)

    insert_db(sql)
