from flask import request, render_template, Blueprint
from flask_restx import Resource, Namespace

Home = Blueprint("home", __name__, url_prefix="/home")
Hello = Namespace('hello')

@Home.route('')
def HomePage():
    return render_template('home.html') # Render home.html

@Hello.route('/hello')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class HelloWorld(Resource):
    def get(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        return {"hello": "world!"}

@Hello.route('/hello/<string:name>')  # url pattern으로 name 설정
class Welcome(Resource):
    def get(self, name):  # 멤버 함수의 파라미터로 name 설정
        return {"message" : "Welcome, %s!" % name}