from datetime import datetime
import ifinance
import pandas as pd

from flask import jsonify
from flask_restx import Resource, Namespace
from utils.db_utils import save_dart_to_db, get_dart_to_dataframe, select_db
from utils.db.error import save_error

Dart = Namespace('dart', description='dart')

# dart 조회하여 데이터를 수집합니다.
@Dart.route('/collect_data')
@Dart.doc()
class collect_data(Resource):
    def get(self):
        api_key = '9264c9a7d0da3f3ab83b509033a337722b5c329f'
        ifinance.set_api_key(api_key)

        darts = []
        dartdropnas = []
        successs = []

        """데이터를 수집합니다."""
        try:
            sectors = ifinance.get_sector_dataframe()
        except Exception as e:
            save_error(f"collect_data > get_sector_dataframe", "", e)
        for index, sector in sectors.iterrows():
            sectorCode = sector['sectorCode']
            try:
                stocks = ifinance.get_stock_dataframe(sectorCode)
            except Exception as e:
                save_error(f"collect_data > get_stock_dataframe > {name}", sectorCode, e)
            for jndex, stock in stocks.iterrows():
                name = stock['name']
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
                    try:
                        dart_krx = ifinance.merge_financial_and_monthly_stock_dataframe(dart, krx)
                    except Exception as e:
                        save_error(f"collect_data > merge_financial_and_monthly_stock_dataframe > {name}", krx.to_string() + dart.to_string(), e)

                    # NaN 값을 포함하는 행을 삭제
                    dart_krx = dart_krx.dropna()
                    try:
                        save_dart_to_db(dart_krx)
                    except Exception as e:
                        save_error(f"collect_data > save_dart_to_db > {name}", dart_krx.to_string(), e)

                    successs.append(name)

        save_error(f"dart is None {len(darts)} {' '.join(map(str, darts))}," +
                   f"dart dropna is None {len(dartdropnas)} {' '.join(map(str, dartdropnas))}," +
                   f"successs {len(successs)} {' '.join(map(str, successs))},"  , '', '')
        return '데이터를 수집합니다.'
    
@Dart.route('/get_data/<string:market>/<string:analysis_period>')
@Dart.doc(params={'market': '마켓 ex) KOSPI'})
@Dart.doc(params={'analysis_period': '기간 ex) 3'})
class get_data(Resource):
    def get(self, market, analysis_period):
        """저장된 데이터를 가져옵니다."""
        df = get_dart_to_dataframe(market, analysis_period)
    
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