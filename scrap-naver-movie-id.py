import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# naver movie (filter - title & release)
def find_naver_movie_code2(title, release, naver_movie_code):
    url = f'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={release}' # 개봉일로 영화 검색
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    movies = soup.select('.directory_list > li > a')

    for movie in movies:
        movie_title = movie.text.replace(" ", "")
        movie_title = re.sub(r"[!@#$%^&*():.-]", "", movie_title) # 영화제목에서 특수문자 제거
        movie_title = re.sub(r"[0-9]", "", movie_title) # 영화제목에서 숫자 제거

        if title in movie_title: # 네이버 영화 검색 결과 중 확인하려는 영화 제목이 있다면
            naver_movie_code.append(movie['href'].split('=')[-1]) # a태그에서 영화코드만 필터
            break
    else: # 요청 개봉일에 조건에 맞는 영화가 없다면
        print(title)


# extract movie titles from csv
naver_movie_code = []
boxoffice_table = pd.read_csv('./KOBIS_boxoffice_rank.csv', encoding='utf-8', sep=',') # csv파일 불러오기
for i, movie in enumerate(boxoffice_table.values):
    print(f'##### {i+1} #####')
    release = movie[2].replace('-', '') # 개봉일
    title = movie[1].replace(" ", "") # 영화 제목
    title = re.sub(r"[!@#$%^&*():.-]", "", title) # 영화제목에서 특수 문자 제거
    title = re.sub(r"[0-9]", "", title) # 영화제목에서 숫자 제거
    find_naver_movie_code2(title, release, naver_movie_code)


boxoffice_table['네이버코드'] = naver_movie_code # '네이버코드' 컬럼 생성
print(boxoffice_table.sample)
boxoffice_table.to_csv('KOBIS_boxoffice_rank_plus_naver_code.csv', index=False) # csv파일로 저장