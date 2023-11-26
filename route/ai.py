import base64
import pickle
import ifinance
import pandas as pd

from flask_restx import Resource, Namespace
from utils.db_utils import get_dart_to_dataframe, save_trained_model, select_model
from utils.db.trained_model import get_trained_model#, save_trained_model
from utils.db.error import save_error
from flask import jsonify

from keras.models import load_model, model_from_json

ifinance.set_api_key('9264c9a7d0da3f3ab83b509033a337722b5c329f')

Ai = Namespace('ai', description='ai')

@Ai.route('/learning/<string:algorithm>/<string:market>/<string:analysis_period>')
@Ai.doc(params={'algorithm': '알고리즘 ex) Deep Learning'})
@Ai.doc(params={'market': '마켓 ex) KOSPI'})
@Ai.doc(params={'analysis_period': '기간 ex) 3'})
class learning(Resource):
    def get(self, algorithm, market, analysis_period):
        """dart 조회하여 학습을 합니다."""
        try:
            # dart 조회하여 데이터를 수집합니다.
            # 인자로 시장, 기간을 넣어줘야 합니다.
            
            df = get_dart_to_dataframe(market, analysis_period)
            if not isinstance(df, pd.DataFrame):
                raise ValueError("get_dart_data function should return a pandas DataFrame.")
        except Exception as e:
            save_error(f"learning > get_data", "", e)
            return str(e)

        try:
            # 딥러닝 모델 생성
            #Linear
            #Ridge
            #Lasso
            #ElasticNet
            #Decision Tree
            #Random Forest
            if algorithm == 'Deep Learning':
                model = ifinance.ai.deep_learning(df)
            elif algorithm == 'Linear':
                model = ifinance.ai.regressor(df)
            elif algorithm == 'Ridge':
                model = ifinance.ai.ridge(df)
            elif algorithm == 'Lasso':
                model = ifinance.ai.lasso(df)
            elif algorithm == 'ElasticNet':
                model = ifinance.ai.elastic_net(df)
            elif algorithm == 'Decision Tree':
                model = ifinance.ai.decision_tree(df)
            elif algorithm == 'Random Forest':
                model = ifinance.ai.random_forest(df)
        except Exception as e:
            save_error(f"learning > deep_learning", df.to_string() if isinstance(df, pd.DataFrame) else str(df), e)
            return str(e)

        try:
            save_trained_model(model, algorithm, market, analysis_period)
        except Exception as e:
            save_error(f"learning > save_trained_model", model.summary(), e)
            return str(e)

        return '학습을 완료했습니다.'

@Ai.route('/predict/<string:algorithm>/<string:market>/<string:analysis_period>')
@Ai.doc(params={'algorithm': '알고리즘 ex) Deep Learning'})
@Ai.doc(params={'market': '마켓 ex) KOSPI'})
@Ai.doc(params={'analysis_period': '기간 ex) 3'})
class predict(Resource):
    def get(self, algorithm, market, analysis_period):
        """저장된 모델을 불러와서 예측합니다."""

        # 학습된 모델을 불러옵니다.
        model = select_model(algorithm, market, analysis_period)

        # 예측할 데이터를 가져옵니다.
        df = get_dart_to_dataframe(market, analysis_period, True)

        # df를 루프돌면서 예측해서 df로 저장해야 하는데, 
        # df의 sales_change_3, sales_change_6, sales_change_9, sales_change_12, 
        # operating_profit_change_3, operating_profit_change_6, operating_profit_change_9, operating_profit_change_12, 
        # net_profit_change_3, net_profit_change_6, net_profit_change_9, net_profit_change_12, 
        # mmend_clsprc_change_3, mmend_clsprc_change_6, mmend_clsprc_change_9, mmend_clsprc_change_12
        # 의 값을 넣어서, next_mmend_clsprc_change 이걸 예측하되
        # 나머지 `year`, `month`, isu_abbrv, isu_srt_cd, mkt_nm, sales,
        # 'mmend_clsprc', 'net_profit' 'operating_profit' 이 필드들은 안지워지고 유지해야 함

        # 예측에 사용할 특성들
        features = ['sales_change_3', 'sales_change_6', 'sales_change_9', 'sales_change_12', 
            'operating_profit_change_3', 'operating_profit_change_6', 'operating_profit_change_9', 'operating_profit_change_12', 
            'net_profit_change_3', 'net_profit_change_6', 'net_profit_change_9', 'net_profit_change_12', 
            'mmend_clsprc_change_3', 'mmend_clsprc_change_6', 'mmend_clsprc_change_9', 'mmend_clsprc_change_12']

        # DataFrame을 복사하여 원본 데이터를 보존
        df_copy = df.copy()

        # 각 행에 대해 예측 수행
        for i in range(len(df)):
            # 특성 값 추출
            feature_values = df.loc[i, features]

            # feature_values를 2차원 배열로 변환합니다.
            feature_values = feature_values.values.astype('float32').reshape(1, -1)

            # 모델 예측
            prediction = model.predict(feature_values)
            
            # 예측 결과를 새로운 열에 저장
            df_copy.loc[i, 'next_mmend_clsprc_change'] = prediction

        # 예측 결과를 api 결과값 json 으로 반환
        return jsonify(df_copy.to_dict(orient='records'))