import requests

from bs4 import BeautifulSoup
import urllib.request
import requests
from urllib.parse import quote
import pandas as pd
import numpy as np

def crawler(html) :
    idx = 0
    post_df = pd.DataFrame(columns = ("Title", "Post URL",
                                        "Post", "Post length", "Keyword(내돈내산)", "Sponsered word",
                                        "Post Count","Review Count","Image Count","Link Count"))
    #html 파서 객체 생성
    soup = BeautifulSoup(html, 'html.parser')
            
    # 포스트 링크, 포스트 제목 가져오기
    posts = soup.find_all('div', {'class':'detail_box'})
    for post in posts :
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

            # 게시글 수
            post_count_element = post_html.find('h4', {'class': 'category_title pcol2'})
            post_count = ''.join(filter(str.isdigit, post_count_element.text.strip())) if post_count_element else 0
            post_count = int(post_count) if post_count else 0 
            
            #댓글 수
            review_count_element = post_html.find('em', {'id': 'floating_bottom_commentCount'})
            review_count = review_count_element.text.strip() if review_count_element else 0
            review_count = int(review_count) if review_count else 0
            
            #이미지 개수
            image_count = len(post_html.find_all('a', {'class' : 'se-module-image-link __se_image_link __se_link'}))
            
            # 외부 링크 연결 개수
            link_count = len(post_html.find_all('div', {'class' : 'se-module se-module-oglink'}))

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
                
                # 협찬 문구 키워드 여부 검사
                if '원고' in post_content_text or '제공받아' in post_content_text or '수익' in post_content_text or '수수료' in post_content_text or '협찬' in post_content_text:
                    sponsered = 1
                else :
                    sponsered = 0

                # 포스터 길이
                post_content_length = len(post_content_text)


            post_df.loc[idx] = [title, post_url, post_content_text, post_content_length, 
                                keyword, sponsered, post_count, review_count, image_count, link_count]
            idx += 1
    return post_df

blog_post = 30

def crawler_scroll(html):
    global blog_post
    idx = 0
    post_df = pd.DataFrame(columns=("Title", "Post URL",
                                    "Post", "Post length", "Keyword(내돈내산)", "Sponsered word",
                                    "Post Count", "Review Count", "Image Count", "Link Count"))
    
    # html 파서 객체 생성
    soup = BeautifulSoup(html, 'html.parser')
            
    # 포스트 링크, 포스트 제목 가져오기
    posts = soup.find_all('div', {'class':'detail_box'})
    for post in posts[blog_post:]:
        title = post.find('a', {'class': 'title_link'}).text
        # 제목에 내돈내산 키워드 여부 검사
        if ('내돈' in title) or ('내돈내산' in title):
            keyword = 1
        else: 
            keyword = 0
        # 링크 가져오기
        post_url = post.find('a', {'class': 'title_link'})['href']
        # requests 모듈로 post_url의 text 데이터를 가져오기
        post_text = requests.get(post_url).text
        # bs4로 html 문서를 파싱하여 포스트 안의 내용을 접근, 추출할 수 있게 변환
        post_html = BeautifulSoup(post_text, "html.parser")

        # 각 post는 iframe 태그로 감싸져 있기 때문에 이를 제거하고 데이터 추출
        for main_frame in post_html.select("iframe#mainFrame"):
            frame_url = "https://blog.naver.com" + main_frame.get('src')
            post_text = requests.get(frame_url).text
            post_html = BeautifulSoup(post_text, 'html.parser')

            # 게시글 수
            post_count_element = post_html.find('h4', {'class': 'category_title pcol2'})
            post_count = ''.join(filter(str.isdigit, post_count_element.text.strip())) if post_count_element else 0
            post_count = int(post_count) if post_count else 0 

            # 댓글 수
            review_count_element = post_html.find('em', {'id': 'floating_bottom_commentCount'})
            review_count = review_count_element.text.strip() if review_count_element else 0
            review_count = int(review_count) if review_count else 0 
            
            # 이미지 개수
            image_count = len(post_html.find_all('a', {'class': 'se-module-image-link __se_image_link __se_link'}))
            
            # 외부 링크 연결 개수
            link_count = len(post_html.find_all('div', {'class': 'se-module se-module-oglink'}))

            # 포스트 텍스트 크롤링
            post_content_text = ''
            for post_content in post_html.find_all('div', {'class': 'se-main-container'}):
                post_content_text = post_content.get_text()
                # 개행문자 삭제
                post_content_text = post_content_text.replace("\n", "")
                post_content_text = post_content_text.replace("\t", "")
                
                # 포스터 내돈내산 키워드 여부 검사
                if ('내돈내산' in post_content_text or '내돈' in post_content_text) and (keyword == 0):
                    keyword = 1 
                else:
                    keyword = 0
                
                # 협찬 문구 키워드 여부 검사
                if '원고' in post_content_text or '제공받아' in post_content_text or '수익' in post_content_text or '수수료' in post_content_text or '협찬' in post_content_text:
                    sponsered = 1
                else:
                    sponsered = 0

                # 포스터 길이
                post_content_length = len(post_content_text)

            post_df.loc[idx] = [title, post_url, post_content_text, post_content_length, 
                                keyword, sponsered, post_count, review_count, image_count, link_count]
            idx += 1   
    blog_post += 30
    return post_df
