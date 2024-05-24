from flask import Flask, request, jsonify
from flask_cors import CORS

from bs4 import BeautifulSoup
import urllib.request
import requests
from urllib.parse import quote
import pandas as pd
import numpy as np

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer
import joblib
import sklearn
from catboost import CatBoostClassifier

# 크롤링 모듈
import naver_crawler

app = Flask(__name__)
CORS(app) 

# 모델 예측을 위한 전처리
def make_prediction(post_df) :
    X = post_df.drop(['Title', 'Post URL', 'Post'], axis=1)

    # 결측값 처리 (평균 값 대체)
    imputer = SimpleImputer(strategy='mean')
    X = imputer.fit_transform(X)

    # 데이터 스케일링
    rbs = RobustScaler()
    X_scaled = rbs.fit_transform(X)
    predict = model.predict(X_scaled)
    return predict

@app.route("/naverblog", methods=['POST'])
def recieve_data() :
    data = request.get_json()
    html = data['source']
    post_df = naver_crawler.crawler(html)
    print(post_df)
    #모델 예측
    prediction = make_prediction(post_df)
    prediction = prediction.tolist()
    print(prediction)
    return prediction

blog_post = 30

# 스크롤 시 엔드포인트
@app.route("/naverblog/scroll", methods=['POST'])
def scroll_handler():
    global blog_post
    data_from_js = request.get_json()
    html = data_from_js['source']
    post_df = naver_crawler.crawler_scroll(html) 
    print(post_df)
    
    #모델 예측
    prediction = make_prediction(post_df)
    prediction = prediction.tolist()
    print(prediction)
    return prediction

if __name__ == '__main__':
    model = joblib.load('model/catboost.pkl')        
    app.run(host='0.0.0.0', port=8080, debug=True)

