from flask_restx import Resource, Namespace
import pandas as pd
import requests
import json

Naver = Namespace('naver', description='naver 증권사이트의 데이터를 조회합니다.')
    
@Naver.route('/crawling/Financial/<string:symbolCode>')
@Naver.doc(
    params={'symbolCode': '업종코드를 입력해주세요. ex) 090355'},
    responses={
        "year": '연도월',
        "sales": '매출액',
        "operatingProfit": '영업이익',
        "netIncome": '당기순이익',
        "operatingProfitRatio": '영업이익률',
        "netProfitRatio": '순이익률',
    }
)
class crawlingFinancial(Resource):
    def get(self, symbolCode):
        """종목코드를 기반으로 재무제표를 조회합니다."""
        try:
            URL = f"https://finance.naver.com/item/main.nhn?code={symbolCode[1:]}"
            r = requests.get(URL)
            df = pd.read_html(r.text)[3]
            df.set_index(df.columns[0],inplace=True)
            df.index.rename('주요재무정보', inplace=True)
            df.columns = df.columns.droplevel(2)
            annual_date = pd.DataFrame(df).xs('최근 연간 실적',axis=1)
            quater_date = pd.DataFrame(df).xs('최근 분기 실적',axis=1)

            # 영업이익률과 순이익률을 하나의 리스트로 합치기
            data_list = []
            for year in quater_date.iloc[3].index :
                data_dict = {
                    'year': year, 
                    'sales' : quater_date[year]['매출액'],
                    'operatingProfit' : quater_date[year]['영업이익'],
                    'netIncome' : quater_date[year]['당기순이익'],
                    'operatingProfitRatio': quater_date[year]['영업이익률'], 
                    'netProfitRatio': quater_date[year]['순이익률'],
                }
                data_list.append(data_dict)

            # JSON 형식으로 변환
            json_str = json.dumps(data_list)

            # JSON 형식으로 변환
            json_data = json.loads(json_str)

            return json_data
        except Exception as e:
            print(f"Error occurred: {e}")
            return None        