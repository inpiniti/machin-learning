from flask import request, render_template, Blueprint
from flask_restx import Resource, Namespace
import pandas as pd

import requests

Krx = Namespace('krx', description='krx 증권사이트의 데이터를 조회합니다.')
host = 'http://data.krx.co.kr'
url_path = '/comm/bldAttendant/getJsonData.cmd'
headers = {
    'Host': 'data.krx.co.kr',
    'User-Agent': 'PostmanRuntime/7.32.3'
}

# 현재 시세
@Krx.route('/currentPrice')
class currentPrice(Resource):
    def get(self):
        """크롤링을 하여 krx 의 모든 한국 주식의 현재 시세를 조회합니다. swagger에서는 데이터가 렌더링이 안되니 조회는 postman 등에서 하세요."""

        response = requests.get(host + url_path + '?bld=dbms/MDC/STAT/standard/MDCSTAT01501&locale=ko_KR&mktId=ALL&trdDd=20230802&share=1&money=1&csvxls_isNo=false')
        
        return response.json()['OutBlock_1']

# 월별 종목 시세
@Krx.route('/currentPrice/<string:isuCd>/<string:strtYymm>/<string:endYymm>')
@Krx.doc(params={'isuCd': '종목 코드 ex) KR7005930003'})
@Krx.doc(params={'strtYymm': '시작년월 ex) 202301'})
@Krx.doc(params={'endYymm': '종료년월 ex) 202307'})
class currentPrice(Resource):
    def get(self, isuCd, strtYymm, endYymm):
        """크롤링을 하여 krx 의 월별 종목의 주식의 현재 시세를 조회합니다."""

        url = (
            host + url_path + 
            f"?bld=dbms/MDC/STAT/standard/MDCSTAT01802" +
            f"&isuCd={isuCd}" +
            f"&strtYymm={strtYymm}" +
            f"&endYymm={endYymm}"
        )

        response = requests.get(url)
        
        return response.json()['OutBlock_1']