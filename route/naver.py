from flask_restx import Resource, Namespace
import config

Naver = Namespace('naver')

@Naver.route('/popular')
class Popular(Resource):
    def get(self):
        return config.stockPredictResult

@Naver.route('/discussion')
class Discussion(Resource):
    def get(self):
        return config.discussionPredictResult

@Naver.route('/news')
class News(Resource):
    def get(self):
        return config.newsPredictResult