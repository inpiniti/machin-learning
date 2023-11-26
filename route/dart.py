import ifinance
import pandas as pd

from flask import jsonify
from flask_restx import Resource, Namespace
from utils.db_utils import save_dart_to_db, get_dart_to_dataframe
from utils.db.error import save_error

Dart = Namespace('dart', description='dart')

# dart 조회하여 데이터를 수집합니다.
@Dart.route('/collect_data')
@Dart.doc()
class collect_data(Resource):
    def get(self):
        api_key = '9264c9a7d0da3f3ab83b509033a337722b5c329f'
        ifinance.set_api_key(api_key)

        """데이터를 수집합니다."""
        try:
            sectors = ifinance.get_sector_dataframe()
        except Exception as e:
            save_error(f"collect_data > get_sector_dataframe", "", e)
        for _, sector in sectors.iterrows():
            sectorCode = sector['sectorCode']
            try:
                stocks = ifinance.get_stock_dataframe(sectorCode)
            except Exception as e:
                save_error(f"collect_data > get_stock_dataframe > {name}", sectorCode, e)
            for _, stock in stocks.iterrows():
                name = stock['name']
                symbolCode = stock['symbolCode']
                symbolCode = symbolCode[1:]
                code = stock['code']
                try:
                    dart = ifinance.get_financial_dataframe(symbolCode)
                except Exception as e:
                    save_error(f"collect_data > get_financial_dataframe > {name}", symbolCode, e)
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
                
        return '데이터를 수집합니다.'
    
@Dart.route('/get_data')
@Dart.doc()
class get_data(Resource):
    def get(self):
        """저장된 데이터를 가져옵니다."""
        df = get_dart_to_dataframe()
    
        # Assuming `df` is your DataFrame
        return jsonify(df.to_dict(orient='records'))