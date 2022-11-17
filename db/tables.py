import db.dbconn as conn

# 테이블 조회
def select_tablse():
    df = conn.select(
        conn.db_conn(),
        f'select * from tables;'
    )

    return df