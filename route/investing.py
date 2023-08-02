# https://kr.investing.com/equities/StocksFilter?noconstruct=1&smlID=694&sid=&tabletype=price&index_id=all


from flask import request, render_template, Blueprint
from flask_restx import Resource, Namespace
import pandas as pd

import requests

Investing = Namespace('investing', description='investing 증권사이트의 데이터를 조회합니다.')
host = 'https://kr.investing.com'
headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': '',
    'Host': 'kr.investing.com',
    'Cache-Control': 'no-cache',
    'Referer': 'https://kr.investing.com/equities/StocksFilter',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

@Investing.route('currentPrice')
class currentPrice(Resource):
    def get(self):
        """크롤링을 하여 investing 의 모든 한국 주식의 현재 시세를 조회합니다. (지금은 Forbidden 이 뜸)"""

        # Query Params
        noconstruct = '1'
        smlID = '694'
        tabletype = 'price'
        index_id = 'all'

        url_path = '/equities/StocksFilter'

        query_params = {
            'noconstruct' : noconstruct,
            'smlID' : smlID,
            'sid' : '',
            'tabletype' : tabletype,
            'index_id' : index_id,
        }

        url = host + url_path

        response = requests.get(
            url,
            json=query_params,
            headers=headers)
        
        print(response)
        print('status : ' + str(response.raise_for_status))
        print('headers : ' + str(response.request.headers))
        print('url : ' + str(response.request.url))
        print('body : ' + str(response.request.body))
        print('path_url : ' + str(response.request.path_url))
        print('reason : ' + str(response.reason))
        print('cookies : ' + str(response.cookies))
        print('raw : ' + str(response.raw))
        print('elapsed : ' + str(response.elapsed))

        #df = pd.read_html(response)

        #print(df)

        return ''