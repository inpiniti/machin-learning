from flask_restx import Resource, Namespace
import config
import pandas as pd
import requests
import json

Naver = Namespace('naver', description='naver 증권사이트의 데이터를 조회합니다.')

@Naver.route('/popular')
class Popular(Resource):
    def get(self):
        return config.stockPredictResult

@Naver.route('/discussion')
class Discussion(Resource):
    def get(self):
        return config.discussionPredictResult

@Naver.route('/news')
class News(Resource):
    def get(self):
        return config.newsPredictResult
    
@Naver.route('crawlingFinancial/<string:symbolCode>')
@Naver.doc(params={'symbolCode': '업종코드를 입력해주세요. ex) 090355'})
class crawlingFinancial(Resource):
    def get(self, symbolCode):
        """종목코드를 기반으로 재무제표를 조회합니다."""
        
        URL = f"https://finance.naver.com/item/main.nhn?code={symbolCode}"
        r = requests.get(URL)
        df = pd.read_html(r.text)[3]
        df.set_index(df.columns[0],inplace=True)
        df.index.rename('주요재무정보', inplace=True)
        df.columns = df.columns.droplevel(2)
        #annual_date = pd.DataFrame(df).xs('최근 연간 실적',axis=1)
        quater_date = pd.DataFrame(df).xs('최근 분기 실적',axis=1)

        return json.loads(quater_date.to_json())