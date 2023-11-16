# 가상환경 활성화
# source venv3.9/bin/activate 

from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import urllib.request
import requests
from urllib.parse import quote
import pandas as pd
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

app = Flask(__name__)
CORS(app) 

crawled_count = 0

def naver_crawler(html) :
    # 전역변수 사용해서 크롤링한 개수 누적
    global crawled_count
    idx = 0

    # 데이터를 저장할 dataframe
    post_df = pd.DataFrame(columns = ("Title", "Post URL",
                                      "Post" , "Post length", "Keyword(내돈내산)", 
                                      "Sponsered word"))

    #html 파서 객체 생성
    soup = BeautifulSoup(html, 'html.parser')

    # 포스트 링크, 포스트 제목 가져오기
    posts = soup.find_all('div', {'class':'detail_box'})
    #print(posts)

    # 이전에 크롤링된 post 를 제외하고 크롤링할 수 있도록 인덱스 설정
    for post in posts[crawled_count: ] :
        title = post.find('a', {'class': 'title_link'}).text
        # 제목에 내돈내산 키워드 여부 검사
        if ('내돈' in title) or ('내돈내산' in title):
            keyword = 1
        else : 
            keyword = 0
        #링크 가져오기
        post_url = post.find('a', {'class': 'title_link'})['href']
        #requests 모듈로 post_url의 text 데이터를 가져오기
        post_text = requests.get(post_url).text
        #bs4로 html 문서를 파싱하여 포스트 안의 내용을 접근, 추출할 수 있게 변환
        post_html = BeautifulSoup(post_text, "html.parser")

        # 각 post는 iframe태그로 감싸져 있기 때문에 이를 제거하고 데이터 추출
        for main_frame in post_html.select("iframe#mainFrame"):
            frame_url = "https://blog.naver.com" + main_frame.get('src')
            post_text = requests.get(frame_url).text
            post_html = BeautifulSoup(post_text, 'html.parser')

            # 포스트 텍스트 크롤링
            post_content_text = ''
            for post_content in post_html.find_all('div', {'class' : 'se-main-container'}):
                post_content_text = post_content.get_text()
                # 개행문자 삭제
                post_content_text = post_content_text.replace("\n", "")
                post_content_text = post_content_text.replace("\t", "")
                
                #포스터 내돈내산 키워드 여부 검사
                if ('내돈내산' in post_content_text or '내돈' in post_content_text) and (keyword==0) :
                    keyword = 1 
                else :
                    keyword = 0
                
                # 협찬 문구 키워드 여부 검사 (이미지 문구 인식까지 디벨롭시켜야함)
                if '원고' in post_content_text or '제공받아' in post_content_text or '수익' in post_content_text or '수수료' in post_content_text:
                    sponsered = 1
                else :
                    sponsered = 0
                
                # 포스터 길이
                post_content_length = len(post_content_text)

            post_df.loc[idx] = [title, post_url, post_content_text, post_content_length, 
                                keyword, sponsered]
            idx += 1

    crawled_count += 30
    return post_df

def make_prediction(post_df) :

    X = post_df.drop(['Title', 'Post URL', 'Post'], axis=1)

    # 데이터 스케일링
    std = StandardScaler()
    X_scaled = std.fit_transform(X)

    predict = model.predict(X_scaled)

    return predict


@app.route("/naverblog", methods=['POST'])
def recieve_data() :
    data_from_js = request.get_json()
    html = data_from_js['source'] 
    post_df = naver_crawler(html)
    #print(post_df)

    #모델 예측
    prediction = make_prediction(post_df)
    prediction = prediction.tolist()
    print(prediction)
    return prediction

# 스크롤 했을 때 응답하는 서버
@app.route("/naverblog/scroll", methods=['POST'])
def scroll_handler():
    data_from_js = request.get_json()
    html = data_from_js['source']
    post_df = naver_crawler(html)
    #print(post_df)
    
    #모델 예측
    prediction = make_prediction(post_df)
    prediction = prediction.tolist()
    print(prediction)
    return prediction


if __name__ == '__main__':
    model = joblib.load('rf_model.pkl')
    app.run(host='0.0.0.0',port=443, debug=True)
