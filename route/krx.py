from flask import request, render_template, Blueprint
from flask_restx import Resource, Namespace
import pandas as pd

import requests

Krx = Namespace('krx', description='krx 증권사이트의 데이터를 조회합니다.')
host = 'http://data.krx.co.kr'
headers = {
    'Host': 'data.krx.co.kr',
    'User-Agent': 'PostmanRuntime/7.32.3'
}

@Krx.route('/currentPrice')
class currentPrice(Resource):
    def get(self):
        """크롤링을 하여 krx 의 모든 한국 주식의 현재 시세를 조회합니다. swagger에서는 데이터가 렌더링이 안되니 조회는 postman 등에서 하세요."""

        # Query Params
        bld = 'dbms/MDC/STAT/standard/MDCSTAT01501'
        locale = 'ko_KR'
        mktId = 'ALL'
        trdDd = '20230802'
        share = '1'
        money = '1'
        csvxls_isNo = 'false'

        url_path = '/comm/bldAttendant/getJsonData.cmd'

        query_params = {
            bld: bld,
            locale: locale,
            mktId: mktId,
            trdDd: trdDd,
            share: share,
            money: money,
            csvxls_isNo: csvxls_isNo,
        }

        url = host + url_path

        response = requests.get('http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd?bld=dbms/MDC/STAT/standard/MDCSTAT01501&locale=ko_KR&mktId=ALL&trdDd=20230802&share=1&money=1&csvxls_isNo=false')
        
        return response.json()['OutBlock_1']