import db.tables as tb
import pandas as pd
import blank

def 테이블조회():
    df = tb.select_tablse()
    print(df)

def 학습():
    blank.start_learning()

# 목표 금액을 위한 테스트 인데,
# start_learning의 수정이 필요할듯 싶음
학습()