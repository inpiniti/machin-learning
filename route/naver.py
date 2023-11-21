from flask_restx import Resource, Namespace
import pandas as pd
import requests
import json
import math
from route.krx import currentPrices
from datetime import datetime, timedelta

from utils.merge_json import add_next_quarter_data, merge_json_data, merge_quarterly_data

Naver = Namespace('naver', description='naver 증권사이트의 데이터를 조회합니다.')
    
@Naver.route('/crawling/Financial/<string:symbolCode>')
@Naver.doc(
    params={'symbolCode': '업종코드를 입력해주세요. ex) A090355'},
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
                sales = quater_date[year]['매출액']
                operating_profit = quater_date[year]['영업이익']
                net_income = quater_date[year]['당기순이익']
                operating_profit_ratio= quater_date[year]['영업이익률']
                net_profit_ratio= quater_date[year]['순이익률']
                
                # NaN 값을 가진 데이터를 제외하고 data_list에 추가합니다.
                if all(map(lambda x: not math.isnan(x), [sales, operating_profit, net_income, operating_profit_ratio, net_profit_ratio])):
                    data_dict = {
                        'year': year, 
                        'sales': sales,
                        'operatingProfit': operating_profit,
                        'netIncome': net_income,
                        'operatingProfitRatio': operating_profit_ratio, 
                        'netProfitRatio': net_profit_ratio,
                    }
                    data_list.append(data_dict)

            # JSON 문자로 변환
            json_str = json.dumps(data_list)

            # JSON 형식으로 변환
            json_data = json.loads(json_str)

            # 이전 분기 데이터를 합칩니다.
            json_data = merge_quarterly_data(json_data)

            return json_data
        except Exception as e:
            URL = f"https://finance.naver.com/item/main.nhn?code={symbolCode[1:]}"
            print(f"Error occurred: (naver.crawlingFinancial) {e}")
            print(f"URL: {URL}")
            return None

# naver financial 데이터와 krx의 currentPrice 데이터를 합치기
@Naver.route('/financial/currentPrice/<string:symbolCode>/<string:isuCd>')
@Naver.doc(params={'symbolCode': '업종코드를 입력해주세요. ex) A090355'})
@Naver.doc(params={'isuCd': '종목 코드 ex) KR7005930003'})
class financialCurrentPrice(Resource):
    def get(self, symbolCode, isuCd):
        """종목코드를 기반으로 재무제표를 조회합니다."""

        # 2년 전 날짜를 계산합니다.
        two_years_ago = datetime.now() - timedelta(days=2*365)
        two_years_ago_str = two_years_ago.strftime('%Y%m')

        # 오늘 날짜를 계산합니다.
        today = datetime.now()
        today_str = today.strftime('%Y%m')

        # 검색 기간을 설정합니다.
        strtYymm = two_years_ago_str
        endYymm = today_str

        try:
            # 재무재표 조회
            financials = crawlingFinancial().get(symbolCode)
            # krx 의 월별 종목의 주식의 현재 시세를 조회
            currentPrice = currentPrices().get(isuCd, strtYymm, endYymm)
            
            merged_data = merge_json_data(financials, currentPrice)
            # 다음 분기의 MMEND_CLSPRC 필드를 추가
            merged_data = add_next_quarter_data(merged_data)

            for data in merged_data:
                new_data = {}
                for key, value in data.items():
                    new_key = key.title().replace('_', '')
                    new_data[new_key[0].lower() + new_key[1:]] = value
                data.clear()
                data.update(new_data)

            return merged_data
        except Exception as e:
            print(f"Error occurred: (naver.financialCurrentPrice) {e}")
            return None