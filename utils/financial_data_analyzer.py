from db_utils import get_financials_dataframe, save_trained_model, predict_with_saved_model

import numpy as np
import pandas as pd

from sklearn.model_selection import cross_val_score

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, r2_score, mean_squared_error

from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

# 딥러닝을 위해서
from keras.models import Sequential
from keras.layers import Dense

best_accuracy = 0 # 가장 좋은 알고리즘
best_model = None # 가장 좋은 모델
classifier_types = [ "Decision Tree", "Gradient Boost", "Random Forest", "Support Vector Machine", "Neural Network",] # 알고리즘 리스트

def deep_learning():
    # 최신 날짜로 데이터를 조회
    latest_date_data = get_financials_dataframe()

    # 데이터 전처리
    X = latest_date_data.drop('mmendclsprcchange', axis=1)
    y = latest_date_data['mmendclsprcchange']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=11)

    # float 타입으로 변환
    X_train = X_train.astype('float32')
    y_train = y_train.astype('float32')
    X_test = X_test.astype('float32')
    y_test = y_test.astype('float32')

    # NaN 값을 포함하는 행을 삭제
    X_train = X_train.dropna()
    y_train = y_train.dropna()
    X_test = X_test.dropna()
    y_test = y_test.dropna()

    # 모델 구성
    model = Sequential()
    #model.add(Dense(32, activation='relu', input_dim=X_train.shape[1]))
    #model.add(Dense(1))

    # 2개의 Dense 레이어 추가하고, 64개의 뉴런을 사용
    model.add(Dense(64, activation='relu', input_dim=X_train.shape[1]))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1))

    # 모델 컴파일
    model.compile(optimizer='adam', loss='mean_squared_error')

    # 모델 학습
    model.fit(X_train, y_train, epochs=10, batch_size=32)

    # 예측
    pred = model.predict(X_test)

    # NaN 값이 있는지 확인
    print(y_test.isnull().sum())
    print(np.isnan(pred).sum())
    print('==========================================\n')

    # 성능 평가
    mse = mean_squared_error(y_test, pred)
    print(f'Deep Learning MSE: {mse:.4f}')

    # 실제 값과 예측 값 비교
    comparison = pd.DataFrame({'Actual': y_test, 'Predicted': pred.flatten()})
    pd.set_option('display.max_rows', None)
    print(comparison)
    pd.reset_option('display.max_rows')


def financial_analyzer():
    global best_accuracy, best_model

    # 최신 날짜로 데이터를 조회
    latest_date_data = get_financials_dataframe()

    # 데이터 전처리
    X = latest_date_data.drop('mmendclsprcchange', axis=1)
    y = latest_date_data['mmendclsprcchange']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=11)

    # 회귀 모델 생성
    regressor = LinearRegression()
    ridge = Ridge()
    lasso = Lasso()
    elastic_net = ElasticNet()
    decision_tree = DecisionTreeRegressor()
    random_forest = RandomForestRegressor()

    models = [regressor, ridge, lasso, elastic_net, decision_tree, random_forest]
    model_names = ['regressor', 'Ridge', 'Lasso', 'ElasticNet', 'DecisionTreeRegressor', 'RandomForestRegressor']

    for i, model in enumerate(models):
        # 학습
        model.fit(X_train, y_train)

        # 예측
        pred = model.predict(X_test)

        # 성능 평가
        mse = mean_squared_error(y_test, pred)
        print(f'{model_names[i]} MSE: {mse:.4f}')

        # 실제 값과 예측 값 비교
        comparison = pd.DataFrame({'Actual': y_test, 'Predicted': pred})

        print(comparison)

        print('==========================================\n')
    

    # 모델 저장
    #if accuracy is not None:
    #    save_trained_model(classifier, type, accuracy)

def financial_predict():

    # 최신 날짜로 데이터를 조회
    latest_date_data = get_financials_dataframe()
    latest_date_data = latest_date_data.drop('mmendclsprcchange', axis=1)

    # 행 하나만 예측
    #data = latest_date_data.iloc[0:1, :]

    #prediction = predict_with_saved_model(data, 19)
    #print(prediction)

    # 전체 행 예측
    for i in range(len(latest_date_data)):
        data = latest_date_data.iloc[i:i+1, :]
        prediction = predict_with_saved_model(data, 21)
        print(prediction)
        print('==========================================\n')


if __name__ == "__main__":
    # 학습
    #for classifier_type in classifier_types:
        #financial_analyzer()
        deep_learning()
    # 예측
    #financial_predict()