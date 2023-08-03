from flask import request, render_template, Blueprint
from flask_restx import Resource, Namespace
from datetime import datetime
from config import pysql

from db.dbconn import select, history

import requests

Holiday = Namespace('holiday', description='공휴일 체크')
host = 'http://apis.data.go.kr'
url_path = '/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'
headers = {
    'Host': 'data.krx.co.kr',
    'User-Agent': 'PostmanRuntime/7.32.3'
}

# 오늘이 공휴일인지 확인
@Holiday.route('/isHoliday')
class isHoliday(Resource):
    def get():
        """오늘이 공휴일인지 확인"""
        if datetime.today().weekday() >= 5: # 5(토요일), 6(일요일)
            return {
                'holiday' : 'true'
            }
        else :
            url = (
                host + url_path +
                f"?serviceKey=Js10J2bn%2B03d15sWQ6w2qep%2B3QWjnpJeOhm9N%2FzhRxVRngOLJsxVZ6ApZMHVFRlOj5zwGilQXZju8HVYTH0IXA%3D%3D" +
                f"&solYear={datetime.today().year}" +
                f"&solMonth={str(datetime.today().month).zfill(2)}" +
                f"&_type=json" +
                f"&numOfRows=20"
            )

            response = requests.get(url)

            today = datetime.today().strftime("%Y%m%d")

            result = 'false'

            items = response.json()['response']['body']['items']['item']

            # items 이 object 일때
            if type(items) == dict:
                if str(items['locdate']) == today:
                    result = 'true'

            # items 이 array 일때
            else:
                for item in items:
                    if str(item['locdate']) == today:
                        result = 'true'

            select(history(host=pysql["host"], url_path="/holiday/isHoliday", result=result))

            return {
                'holiday' : result
            }
