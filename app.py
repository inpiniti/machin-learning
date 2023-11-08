from flask import Flask # Flask 객체 import
from flask_restx import Resource, Api # Api 구현을 위한 Api 객체 import
from flask_cors import CORS # CORS 처리를 위한 모듈 import

from route.naver import Naver
from route.daum import Daum
from route.investing import Investing
from route.krx import Krx
from route.db import Db

app = Flask(__name__, template_folder="templates")
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app)

# Flask 객체에 Api 객체 등록
api = Api(app)

api.add_namespace(Naver, '/naver')
api.add_namespace(Daum, '/daum')
api.add_namespace(Investing, '/investing')
api.add_namespace(Krx, '/krx')
api.add_namespace(Db, '/db')

if(__name__=='__main__'):
    app.run(host='0.0.0.0', port=5001)