# 학습

from flask_restx import Resource, Namespace

import ifinance
import pandas as pd

from utils.db_utils import save_trained_model
from dart import get_data
from utils.db.error import save_error

ifinance.set_api_key('9264c9a7d0da3f3ab83b509033a337722b5c329f')

Ai = Namespace('ai', description='ai')

@Ai.route('/learning')
class learning(Resource):
    def get(self):
        """dart 조회하여 학습을 합니다."""

        try:
            df = get_data()
        except Exception as e:
            save_error(f"learning > get_data", "", e)

        try:
            # 딥러닝 모델 생성
            model = ifinance.ai.deep_learning(df)
        except Exception as e:
            save_error(f"learning > deep_learning", df.to_string(), e)

        try:
            save_trained_model(model, 'deep learning', 0)
        except Exception as e:
            save_error(f"learning > save_trained_model", model.to_string(), e)

        return '학습을 완료했습니다.'