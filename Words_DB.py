import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient


# client = MongoClient('localhost', 27017) # db 로컬
client = MongoClient('mongodb://test:test@localhost', 27017) # db aws

db = client.hh99_nickname # db연결

# db = client.nickname

# 나무위키 명사 크롤러
def wiki_words_noun_crawler(page):                                                      # 현재 페이지의 https://ko.wiktionary.org 를 제외한 부분을 받는다.
    url = f'https://ko.wiktionary.org{page}'                                            # 현재 페이지의 링크를 url 변수에 저장
    count = 0
    for re in range(150):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(f'{url}', headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        trs = soup.select('#mw-pages')
        try:
            for tr in trs:                                                              # tr은 #mw-pages 리스트 만큼 반복
                rink = tr.select_one('a:nth-child(4)')['href']                          # 다음 페이지 링크를 rink 변수에 저장
                words = soup.select('#mw-pages > div > div > div > ul > li')            # 현재 페이지 명사를 words 변수에 저장
                url = f'https://ko.wiktionary.org{rink}'                                # 다음 페이지 링크를 url 로 넘겨준다.
                for word in words:                                                      # word는 현재 페이지 명사 리스트 만큼 반복
                    all_words = word.select_one('a').text                               # 명사 텍스트 추출
                    if len(all_words) > 1:                                              # 2글자 이상 텍스트만 구함
                        count += 1
                        # print(all_words)

                        doc = {
                            'word': all_words,
                            'class': 'noun'
                        }
                        db.wordsdb.insert_one(doc)                                      # 크롤링한 명사 데이터 DB에 저장
        except:                                                                         # 오류가 나와도 메시지 출력 안함 (ㄱ,ㄲ,ㄳ,다음페이지 없음 등 필요없는 데이터)
            ('')
    print(str(count) + '항목 Noun DB Upload Successes!')                                 # 완료 메시지 출력


# 나무위키 형용사 크롤러
def wiki_words_adj_crawler():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://ko.wiktionary.org/wiki/%EB%B6%84%EB%A5%98:%ED%95%9C%EA%B5%AD%EC%96%B4_%EA%B4%80%ED%98%95%EC%82%AC%ED%98%95(%ED%98%95%EC%9A%A9%EC%82%AC)', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    trs = soup.select('#mw-pages > div > div > div > ul > li')     # li 태그 안에 있는 리스트 추출
    count = 0
    for tr in trs:
        count += 1
        words = tr.select_one('a').text                            # a태그 안에 있는 형용사 리스트 텍스트만 추출
        doc = {
            'word': words,
            'class': 'adj'
        }
        db.wordsdb.insert_one(doc)                                 # 크롤링한 형용사 데이터 DB에 저장
    print(str(count) + '항목 Adj DB Upload Successes!')             # 완료 메시지 출력


# 나무위키 동물 크롤러
def wiki_animal_crawler():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://ko.wiktionary.org/wiki/%EB%B6%84%EB%A5%98:%ED%95%9C%EA%B5%AD%EC%96%B4_%ED%8F%AC%EC%9C%A0%EB%A5%98', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    trs = soup.select('#mw-pages > div > div > div > ul > li')     # li 태그 안에 있는 리스트 추출
    count = 0
    for tr in trs:
        count += 1
        animal = tr.select_one('a').text                           # a태그 안에 있는 동물 리스트 텍스트만 추출
        doc = {
            'word': animal,
            'class': 'animal'  # 동물
        }
        db.wordsdb.insert_one(doc)                                 # 크롤링한 동물 데이터 DB에 저장

    print(str(count) + '항목 Animal DB Upload Successes!')          # 완료 메시지 출력


# 나무위키 과일 크롤러
def wiki_fruits_crawler():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://ko.wikipedia.org/wiki/%EB%B6%84%EB%A5%98:%EA%B3%BC%EC%9D%BC', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    trs = soup.select('#mw-pages > div > div > div > ul > li')     # li 태그 안에 있는 리스트 추출
    count = 0
    for tr in trs:
        fruits = tr.select_one('a').text                           # a태그 안에 있는 과일 리스트 텍스트만 추출
        if len(fruits) < 5:
            if fruits != '과식주의':
                count += 1
                doc = {
                    'word': fruits,
                    'class': 'fruits'
                }
                db.wordsdb.insert_one(doc)                         # 크롤링한 과일 데이터 DB에 저장

    print(str(count) + '항목 Fruits DB Upload Successes!')          # 완료 메시지 출력





wiki_words_adj_crawler()  # 형용사

wiki_animal_crawler()  # 동물

wiki_fruits_crawler()  # 과일

wiki_words_noun_crawler('/w/index.php?title=%EB%B6%84%EB%A5%98:%ED%95%9C%EA%B5%AD%EC%96%B4_%EB%AA%85%EC%82%AC&from=%EA%B0%80')  # 명사

