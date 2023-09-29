from flask import request, render_template, Blueprint
from flask_restx import Resource, Namespace

import pandas as pd
import requests
import json

from route.naver import crawlingFinancial
from utils.db_utils import save_financials_to_db

Daum = Namespace('daum', description='daum 증권사이트의 데이터를 조회합니다.')
daum_host = 'https://finance.daum.net'
headers = {
    'Referer': 'https://finance.daum.net/domestic/sectors',
    'User-Agent': 'PostmanRuntime/7.32.3'
}

@Daum.route('/crawling/Industries')
@Daum.doc(
    responses={
        "sectorCode": "업종코드",
        "sectorName": "업종명",
    }
)
class crawlingIndustries(Resource):
    def get(self):
        """크롤링을 하여 업종리스트(Industry list)를 조회합니다."""

        daum_url = '/api/sector/wics/masters'

        url = (
            daum_host + 
            daum_url
        )
        
        response = requests.get(
            url, 
            headers=headers)
        
        return response.json()

@Daum.route('/crawling/Stocks/<string:sector>')
@Daum.doc(
    params={'sector': '업종코드를 입력해주세요. ex) G101010'},
    responses={
        "code": '종목코드',
        "symbolCode": '업종코드',
        "name": '종목명',
    }
)
class crawlingStocks(Resource):
    def get(self, sector):
        """업종코드를 기반으로 종목(Stock)을 조회합니다."""

        # Query Params
        page = '1'
        perPage = '100'
        fieldName = 'changeRate'
        order = 'desc'
        pagination = 'true'

        daum_url = '/api/sector/wics/' + sector + '/stocks'

        query_params = {
            'symbolCode' : sector,
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

        response = requests.get(url, json=query_params, headers=headers)
        
        # 첫 번째 페이지 데이터 추출
        data = response.json()['data']
        
        # 전체 페이지 수 추출
        total_pages = response.json()['totalPages']

        # 전체 페이지 수가 1 이상인 경우, 추가 데이터 추출
        if total_pages > 1:
            for _page in range(2, total_pages+1):
                query_params = {
                    'symbolCode' : sector,
                    'page' : _page,
                    'perPage' : perPage,
                    'fieldName' : fieldName,
                    'order' : order,
                    'pagination' : pagination
                }
                response = requests.get(url, json=query_params, headers=headers)
                data += response.json()['data']
        
        result = []
        for item in data:
            result.append({
                'code': item['code'],
                'symbolCode': item['symbolCode'],
                'name': item['name']
            })
        json_str = json.dumps(result, ensure_ascii=False, indent=2)
        
        return json.loads(json_str)

@Daum.route('/crawling/Financials')
class crawlingFinancials(Resource):
    def get(self):
        """크롤링을 하여 업종(Industry) -> 종목(Stock) -> 재무재표(Financial) 조회를 합니다."""

        industries = crawlingIndustries().get();

        new_financials = []
        for industry in industries:
            stocks = crawlingStocks().get(industry['sectorCode'])
            for stock in stocks:
                try:
                    stock['sectorCode'] = industry['sectorCode']
                    stock['sectorName'] = industry['sectorName']
                    financials = crawlingFinancial().get(stock['symbolCode'])
                    for financial in financials:
                        try:
                            financial.update(stock)
                            new_financials.append(financial)
                            save_financials_to_db(financial)
                        except Exception as e:
                            print(f"Error occurred: {e}")
                            continue
                except Exception as e:
                    print(f"Error occurred: {e}")
                    continue
        
        # save_financials_to_db(new_financials)

        return new_financials
