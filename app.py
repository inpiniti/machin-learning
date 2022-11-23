from flask import Flask, request, render_template,jsonify # Import flask libraries
from flask_restx import Resource, Api # Api 구현을 위한 Api 객체 import
from route.hello import Hello
from route.todo import Todo
from route.flower import Flower
from route.naver import Naver

from flask_cors import CORS

import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TZ'] = 'Asia/Seoul'

sys.path.append(os.path.abspath("./models"))

from datetime import timedelta, datetime, timezone
#time.tzset()
from apscheduler.schedulers.background import BackgroundScheduler

import blank_test
import manager

import Predict
import api.naver as naver

import config

# Initialize the flask class and specify the templates directory
app = Flask(__name__,template_folder="templates")

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app)
api = Api(app)  # Flask 객체에 Api 객체 등록

api.add_namespace(Hello, '/hello')
api.add_namespace(Todo, '/todos')
api.add_namespace(Naver, '/naver')

app.register_blueprint(Flower)

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

def getKstTime():
    datetime_utc = datetime.utcnow()
    timezone_kst = timezone(timedelta(hours=9))
    datetime_kst = datetime_utc.astimezone(timezone_kst)

    print("datetime_utc:", datetime_utc)
    print("datetime_kst:", datetime_kst)

    return datetime_kst

@api.route('/start')
class IntervalStart(Resource):
    def get(self):
        job2()
        return {}

@api.route('/interesting')
class Interesting(Resource):
    def post(self):

        if len(request.json["data"]) != 0:
            return Predict.Predict().start2(request.json["data"]).to_json(force_ascii=False, orient = 'records', indent=4)
        else:
            return []

cron = BackgroundScheduler(daemon=True)

# 60초마다 실행
@cron.scheduled_job('interval', seconds=60, id='test_1')
def job1():
    now = datetime.today().strftime('%H:%M:%S')
    start = '09:00:00' < now
    end = '15:30:00' > now
    if start & end:
        print(f'ok {now}')
        #blank_test.start()
        config.allPredictResult = Predict.Predict().start()
    else:
        print(f'not {now}')

# 5분마다 실행
@cron.scheduled_job('interval', seconds=300, id='test_2')
def job2():
    config.stockPredictResult = Predict.Predict() \
        .start2(naver.stock()) \
        .to_json(force_ascii=False, orient = 'records', indent=4)

    config.discussionPredictResult = Predict.Predict() \
        .start2(naver.discussion()) \
        .to_json(force_ascii=False, orient = 'records', indent=4)

    config.newsPredictResult = Predict.Predict() \
        .start2(naver.news()) \
        .to_json(force_ascii=False, orient = 'records', indent=4)

cron.start()

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