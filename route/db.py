import json
from flask import jsonify,request
from flask_restx import Resource, Namespace, fields
from utils.db_utils import get_latest_date_from_financials, fetch_data_by_latest_date

Db = Namespace('db', description='db 데이터를 조회합니다.')

global_financials = None

# 요청의 형식을 정의하는 모델을 생성
financials_model = Db.model('Financials', {
    'year': fields.String(description='날짜 ex) 2023.09'),
    'mktNm': fields.String(description='시장명 ex) KOSPI, KOSDAQ'),
    'name': fields.String(description='종목명 ex) 삼성전자'),
    'sectorCode': fields.String(description='섹터코드 ex) G151010'),
    'symbolCode': fields.String(description='종목코드 ex) A900290'),
    # 페이징 처리를 위한 파라미터
    'page': fields.Integer(description='페이지 번호'),
})

@Db.route('/financials', methods=['POST'])
@Db.doc(
)
@Db.expect(financials_model)  # 요청의 예상되는 형식을 지정
class fetch_data_by_date(Resource):
    def post(self):
        """financials 테이블에서 데이터를 조회함"""

        # POST 요청의 body 데이터를 받음
        data = request.get_json()

        # 클라이언트가 보낸 요청이 JSON 형식이 아닌 경우
        if data is None:
            return jsonify({'error': 'Invalid JSON format'}), 400

        # body 데이터에서 mktNm, name 등의 값을 받음
        year = data.get('year')
        mktNm = data.get('mktNm')
        name = data.get('name')
        sectorCode = data.get('sectorCode')
        symbolCode = data.get('symbolCode')
        page = data.get('page')

        # 최신 날짜로 데이터를 조회
        latest_date_data = fetch_data_by_latest_date(year,mktNm, name, sectorCode, symbolCode, page)

        return json.loads(latest_date_data)