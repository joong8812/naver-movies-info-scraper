import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request

korean_movie_table = pd.read_csv('./naver_korean_movie_list.csv', encoding='utf-8', sep=',') # 해당 csv파일은 'scrap_naver_korean_movies.py 에서 생성
for i, movie in enumerate(korean_movie_table.values):
    movie_title = movie[0]
    movie_code = movie[1]
    print(f'##### {i+1} ##### {movie_code} {movie_title}')

    url = f"https://movie.naver.com/movie/bi/mi/photoViewPopup.naver?movieCode={movie_code}"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    image_source = soup.select('#page_content a img')[0]['src']

    # image request & download
    urllib.request.urlretrieve(image_source, f'naver_korean_movie_images/movie_{movie_code}.jpg') # 영화포스터(이미지) 다운로드