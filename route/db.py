import json
from flask import jsonify
from flask_restx import Resource, Namespace
from utils.db_utils import get_latest_date_from_financials, fetch_data_by_latest_date

Db = Namespace('db', description='db 데이터를 조회합니다.')

global_financials = None

@Db.route('/financials')
@Db.doc(
    responses={
    }
)
class crawlingIndustries(Resource):
    def get(self):
        """financials 테이블에서 데이터를 조회함"""

        global global_financials

        if global_financials is None:
            print("global_var is None")

            # financials 에서 최신 날짜를 조회
            latest_date = get_latest_date_from_financials()

            # 최신 날짜로 데이터를 조회
            latest_date_data = fetch_data_by_latest_date(latest_date)

            # 데이터를 JSON 객체로 변환
            latest_date_data_json = jsonify(latest_date_data)

            global_var = latest_date_data_json
        else:
            print("global_var is not None")

        return global_financials