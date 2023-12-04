from datetime import datetime
import ifinance
import pandas as pd

from flask import jsonify
from flask_restx import Resource, Namespace
from utils.db_utils import save_dart_to_db, get_dart_to_dataframe, select_db
from utils.db.error import save_error

from socket_events import sendMessage

Dart = Namespace('dart', description='dart')

# dart 조회하여 데이터를 수집합니다.
@Dart.route('/collect_data')
@Dart.doc()
class collect_data(Resource):
    def get(self):
        # 전역 변수를 함수 내에서 수정하려면 'global' 키워드를 사용해야 합니다.
        global sectorName, sectorCurrentIndex, sectorTotalCount, stockName, stockCurrentIndex, stockTotalCount, isCollecting

        # 수집중으로 변경
        isCollecting = True
        
        api_key = '9264c9a7d0da3f3ab83b509033a337722b5c329f'
        ifinance.set_api_key(api_key)

        darts = []
        dartdropnas = []
        successs = []

        """데이터를 수집합니다."""
        try:
            sectors = ifinance.get_sector_dataframe()
            sectorTotalCount = len(sectors)
        except Exception as e:
            save_error(f"collect_data > get_sector_dataframe", "", e)
            isCollecting = False
        for index, sector in sectors.iterrows():
            sectorCode = sector['sectorCode']
            
            sectorName = sector['sectorName']
            sectorCurrentIndex = index
            try:
                stocks = ifinance.get_stock_dataframe(sectorCode)
                stockTotalCount = len(stocks)
            except Exception as e:
                save_error(f"collect_data > get_stock_dataframe > {name}", sectorCode, e)
                isCollecting = False
            for jndex, stock in stocks.iterrows():
                name = stock['name']
                stockName = name
                stockCurrentIndex = jndex

                # sectorName, sectorCurrentIndex, sectorTotalCount, stockName, stockCurrentIndex, stockTotalCount
                # 데이터를 json 으로 보내서 프론트에서 처리하도록 변경
                sendMessage({
                    'sectorName': sectorName,
                    'sectorCurrentIndex': sectorCurrentIndex,
                    'sectorTotalCount': sectorTotalCount,
                    'stockName': stockName,
                    'stockCurrentIndex': stockCurrentIndex,
                    'stockTotalCount': stockTotalCount
                })

                symbolCode = stock['symbolCode']
                symbolCode = symbolCode[1:]
                code = stock['code']

                print(index, jndex)

                # 이미 저장되어 있으면 수집을 굳이 할필요는 없을거 같음
                # 조건문으로 분기처리                    
                if is_already_saved(symbolCode):
                    try:
                        dart = ifinance.get_financial_dataframe(symbolCode)
                    except Exception as e:
                        save_error(f"collect_data > get_financial_dataframe > {name}", symbolCode, e)
                        isCollecting = False

                    # dart nan 값 포함하는 행 제거하고,
                    if dart is not None:
                        dart = dart.dropna()
                    else:
                        darts.append(name)
                        print('dart is None', len(darts))
                        continue
                    # dart 가 비어 있으면 이후 작업을 하지 않음
                    if len(dart) == 0:
                        dartdropnas.append(name)
                        print('dart.dropna() is empty', len(dartdropnas))
                        continue

                    try:
                        krx = ifinance.get_monthly_stock_dataframe(code)
                    except Exception as e:
                        save_error(f"collect_data > get_monthly_stock_dataframe > {name}", code, e)
                        isCollecting = False
                    try:
                        dart_krx = ifinance.merge_financial_and_monthly_stock_dataframe(dart, krx)
                    except Exception as e:
                        save_error(f"collect_data > merge_financial_and_monthly_stock_dataframe > {name}", krx.to_string() + dart.to_string(), e)
                        isCollecting = False

                    # NaN 값을 포함하는 행을 삭제
                    dart_krx = dart_krx.dropna()
                    try:
                        save_dart_to_db(dart_krx)
                    except Exception as e:
                        save_error(f"collect_data > save_dart_to_db > {name}", dart_krx.to_string(), e)
                        isCollecting = False

                    successs.append(name)

        save_error(f"dart is None {len(darts)} {' '.join(map(str, darts))}," +
                   f"dart dropna is None {len(dartdropnas)} {' '.join(map(str, dartdropnas))}," +
                   f"successs {len(successs)} {' '.join(map(str, successs))},"  , '', '')
        # 수집 완료됨
        isCollecting = False
        return '데이터를 수집합니다.'

class getIsCollecting(Resource):
    def get(self):
        """데이터 수집중인지 확인합니다."""
        global isCollecting
        return isCollecting

@Dart.route('/get_data/<string:market>/<string:analysis_period>')
@Dart.doc(params={'market': '마켓 ex) KOSPI'})
@Dart.doc(params={'analysis_period': '기간 ex) 3'})
class get_data(Resource):
    def get(self, market, analysis_period):
        """저장된 데이터를 가져옵니다."""
        df = get_dart_to_dataframe(market, analysis_period, True)
    
        # Assuming `df` is your DataFrame
        return jsonify(df.to_dict(orient='records'))

# 이미 저장되어 있으면 수집을 굳이 할필요는 없을거 같음
# 조건문으로 분기처리 
def is_already_saved(symbolCode):
    # 조건문에 최근 년도와 월도 넣어서 비교해야 하는데,
    # year 은 올해 년도
    year = datetime.now().year
    # month 는 3의 배수로 가장 최근
    month = get_nearest_previous_multiple_of_three(datetime.now().month)

    sql = f"""
        SELECT * FROM `python-inpiniti`.dart
        WHERE isu_srt_cd = '{symbolCode}'
        AND year = '{year}'
        AND month = '{month}'
    """
    df = select_db(sql)
    if len(df) == 0:
        return True
    else:
        return False

# 현재 년도와 월을 기준으로 가장 최근의 년도와 월을 가져옵니다.
# 3의 배수로 가장 최근
def get_nearest_previous_multiple_of_three(month):
    return "{:02}".format(((month - 1) // 3) * 3)