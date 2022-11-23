from flask_restx import Resource, Namespace
import os

Learning = Namespace('learning')

# 학습된 파일 리스트
@Learning.route('/learnedFiles')
class learnedFiles(Resource):
    def get(self):
        return os.listdir('./classifier')