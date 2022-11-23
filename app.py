from flask import Flask, request, render_template,jsonify # Import flask libraries
from flask_restx import Resource, Api # Api 구현을 위한 Api 객체 import
from route.hello import Hello
from route.todo import Todo
from route.flower import Flower
from route.naver import Naver
from route.crontab import cron
from flask_cors import CORS

import sys
import os
import blank_test
import manager
import Predict
import config

# 타임존 설정
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TZ'] = 'Asia/Seoul'
sys.path.append(os.path.abspath("./models"))

# Initialize the flask class and specify the templates directory
app = Flask(__name__,template_folder="templates")
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app)

# Flask 객체에 Api 객체 등록
api = Api(app)

# api 라우터 연결
api.add_namespace(Hello, '/hello')
api.add_namespace(Todo, '/todos')
api.add_namespace(Naver, '/naver')

# html 라우터 연결
app.register_blueprint(Flower)

# 배치 시작
cron.start()

#model, graph = init()

@api.route('/test2')
class test2(Resource):
    def get(self):
        #df = blank_test.getResult()
        #df = allPredict.getResult()
        df = config.allPredictResult

        if df is None:
            return {}
        else :
            return df.to_json(force_ascii=False, orient = 'records', indent=4)

@api.route('/interesting')
class Interesting(Resource):
    def post(self):
        if len(request.json["data"]) != 0:
            return Predict.Predict().start2(request.json["data"]).to_json(force_ascii=False, orient = 'records', indent=4)
        else:
            return []

@app.route('/test3')
def test3():
    df = blank_test.getResult()
    if df is None:
        return {}
    else :
        return df.to_html()

# 학습된 파일 리스트
@api.route('/learnedFiles')
class learnedFiles(Resource):
    def get(self):
        return manager.learned_file()

# Run the Flask server
if(__name__=='__main__'):
    app.run(host='0.0.0.0', port=5000)