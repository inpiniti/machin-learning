from flask_restx import Resource, Namespace
import ifinance
from utils.db_utils import save_dart_to_db
import pandas as pd

Dart = Namespace('dart', description='dart')

@Dart.route('/collect_data')
@Dart.doc()
class collect_data(Resource):
    def get(self):
        api_key = '9264c9a7d0da3f3ab83b509033a337722b5c329f'
        ifinance.set_api_key(api_key)

        """데이터를 수집합니다."""
        sectors = ifinance.get_sector_dataframe()
        for _, sector in sectors.iterrows():
            sectorCode = sector['sectorCode']
            stocks = ifinance.get_stock_dataframe(sectorCode)
            for _, stock in stocks.iterrows():
                name = stock['name']
                symbolCode = stock['symbolCode']
                symbolCode = symbolCode[1:]
                code = stock['code']
                try:
                    dart = ifinance.get_financial_dataframe(symbolCode)
                    krx = ifinance.get_monthly_stock_dataframe(code)
                    dart_krx = ifinance.merge_financial_and_monthly_stock_dataframe(dart, krx)

                    # NaN 값을 포함하는 행을 삭제
                    dart_krx = dart_krx.dropna()

                    print(dart_krx)

                    save_dart_to_db(dart_krx)
                except Exception as e:
                    print(f"{name : } An error occurred: {e}")
        return '데이터를 수집합니다.'