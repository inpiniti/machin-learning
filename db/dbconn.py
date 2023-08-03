from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import timedelta
from config import pysql, engine

import time
#time.tzset()

import pandas as pd

Base = declarative_base()
class history(Base):
    __tablename__ = "history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    host = Column(Text)
    url_path = Column(Text)
    result = Column(Text)

db_info = f"mysql+pymysql://{pysql['id']}:{pysql['pw']}@{pysql['host']}:{pysql['port']}/{pysql['db']}"
engine = create_engine(db_info)
engine = engine.connect()

# 실제 테이블 종류 알아오기
def select(_sql_cmd):
    print('\n==================== select() ======================')
    print('Views : tables selecting...');

    start = time.time()

    # sql 조회
    #sql_cmd = f'SELECT MAX(table_name) table_name FROM inpiniti.tables;'
    #db_test = pd.read_sql(sql=_sql_cmd, con=_conn)

    Session = sessionmaker()
    Session.configure(bind=engine)

    print(engine)

    session = Session()
    session.add(_sql_cmd)
    session.commit()
    session.close()

    print(f'table select success : {timedelta(seconds=round(time.time() - start))}');
    print('==========================================\n')

    # pandas 생성
    #df = pd.DataFrame(db_test)

    #return df