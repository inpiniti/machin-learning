from flask import request
from flask_restx import Resource, Namespace
import config
import Predict

Stock = Namespace('stock')

@Stock.route('/all')
class all(Resource):
    def get(self):
        if config.allPredictResult is None:
            return {}
        else :
            return config.allPredictResult.to_json(force_ascii=False, orient='records', indent=4)

@Stock.route('/interesting')
class interesting(Resource):
    def post(self):
        if len(request.json["data"]) != 0:
            return Predict.Predict().start2(request.json["data"]).to_json(force_ascii=False, orient = 'records', indent=4)
        else:
            return []