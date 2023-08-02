from flask import Flask
from flask_restx import Resource, Api # Api 구현을 위한 Api 객체 import
from flask_cors import CORS

from route.hello import Hello
from route.todo import Todo
from route.flower import Flower
from route.naver import Naver
from route.learning import Learning
from route.stock import Stock
from route.crontab import cron
from route.daum import Daum
from route.investing import Investing
from route.krx import Krx
from route.holiday import Holiday

import sys
import os

# 타임존 설정
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TZ'] = 'Asia/Seoul'
sys.path.append(os.path.abspath("./models"))

# Initialize the flask class and specify the templates directory
app = Flask(__name__, template_folder="templates")
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app)

# Flask 객체에 Api 객체 등록
api = Api(app)

# api 라우터 연결
api.add_namespace(Hello, '/hello')
api.add_namespace(Todo, '/todo')
api.add_namespace(Naver, '/naver')
api.add_namespace(Stock, '/stock')
api.add_namespace(Learning, '/learning')
api.add_namespace(Daum, '/daum')
api.add_namespace(Investing, '/investing')
api.add_namespace(Krx, '/krx')
api.add_namespace(Holiday, '/holiday')

# html 라우터 연결
app.register_blueprint(Flower)

# 배치 시작
#cron.start()

# Run the Flask server
if(__name__=='__main__'):
    app.run(host='0.0.0.0', port=5000)