from flask import request, render_template, Blueprint
from flask_restx import Resource, Namespace

import requests

Daum = Namespace('daum', description='daum 증권사이트의 데이터를 조회합니다.')
daum_host = 'https://finance.daum.net'
headers = {
    'Referer': 'https://finance.daum.net/domestic/sectors',
    'User-Agent': 'PostmanRuntime/7.32.3'
}

@Daum.route('crawlingIndustries/<string:market>')
@Daum.doc(params={'market': 'KOSPI 또는 KOSDAQ 을 입력해주세요.'})
class crawlingIndustries(Resource):
    def get(self, market):
        """크롤링을 하여 업종리스트를 조회합니다."""

        # Query Params
        includedStockLimit = '2'
        page = '1'
        perPage = '40'
        fieldName = 'changeRate'
        order = 'desc'
        #market = 'KOSPI' # or KOSDAQ
        change = 'RISE'
        includeStocks = 'true'
        pagination = 'true'

        daum_url = '/api/sectors/'
        
        query_params = {
            'includedStockLimit' : includedStockLimit,
            'page' : page,
            'perPage' : perPage,
            'fieldName' : fieldName,
            'order' : order,
            'market' : market,
            'change' : change,
            'includeStocks' : includeStocks,
            'pagination' : pagination
        }

        url = (
            daum_host + 
            daum_url
        )
        
        response = requests.get(
            url, 
            json=query_params, 
            headers=headers)
        
        list = []
        for i in response.json()["data"]:
            list.append({
                'symbolCode': i['symbolCode'],
                'code': i['code'],
                'sectorCode': i['sectorCode'],
                'sectorName': i['sectorName'],
                'date': i['date'],
                'market': i['market'],
                'change': i['change'],
                'changePrice': i['changePrice'],
                'changeRate': i['changeRate'],
                'tradePrice': i['tradePrice'],
                'prevClosingPrice': i['prevClosingPrice'],
                'accTradeVolume': i['accTradeVolume'],
                'accTradePrice': i['accTradePrice'],
            })
        
        return list

@Daum.route('crawlingStocks/<string:symbolCode>')
@Daum.doc(params={'symbolCode': '업종코드를 입력해주세요. ex) KRD020020149'})
class crawlingStocks(Resource):
    def get(self, symbolCode):
        """업종코드를 기반으로 종목을 조회합니다."""

        # Query Params
        page = '1'
        perPage = '30'
        fieldName = 'changeRate'
        order = 'desc'
        pagination = 'true'

        daum_url = '/api/sectors/' + symbolCode + '/includedStocks'

        query_params = {
            'symbolCode' : symbolCode,
            'page' : page,
            'perPage' : perPage,
            'fieldName' : fieldName,
            'order' : order,
            'pagination' : pagination
        }

        url = (
            daum_host + 
            daum_url
        )

        response = requests.get(
            url, 
            json=query_params, 
            headers=headers)
        
        return response.json()