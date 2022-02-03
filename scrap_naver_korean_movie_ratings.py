import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

def get_ratings_info(movie_code, page):
    rating_list = []
    userid_list = []
    timestamp_list = []
    try: 
        url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&onlyActualPointYn=N&onlySpoilerPointYn=N&order=newest&page={page}' 
        result = requests.get(url)
        soup = BeautifulSoup(result.text, "html.parser")
        score_list = soup.select('.score_result ul li')
        for score_info in score_list:
            score = int(score_info.select('.star_score em')[0].text)
            userid = score_info.select('.score_reple dl dt em a span')[0].text
            timestamp = score_info.select('.score_reple dl dt em')[1].text.replace('.', "").replace(" ", "").replace(':', "")
            rating_list.append(score)
            userid_list.append(userid)
            timestamp_list.append(timestamp)
    except Exception as e:
        print(e)
    
    return rating_list, userid_list, timestamp_list


def get_total_rating_pages(movie_code):
    try:
        url = f"https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&onlyActualPointYn=N&onlySpoilerPointYn=N&order=newest"
        result = requests.get(url)
        soup = BeautifulSoup(result.text, "html.parser")
        total_ratings = int(soup.select('.score_total .total em')[0].text.replace(',', ''))
    except Exception as e:
        print(e)
        return 0, 0
    return total_ratings, math.ceil(total_ratings / 10)


rating_list = []
userid_list = []
timestamp_list = []
korean_movie_table = pd.read_csv('./naver_korean_movie_list.csv', encoding='utf-8', sep=',') # csv파일 불러오기
for i, movie in enumerate(korean_movie_table.values):
    print(f'##### {i+1} ##### {movie[1]}')
    movie_code = movie[1] # 영화코드
    total_ratings, total_rating_pages = get_total_rating_pages(movie_code)
    for page in range(1, (49 if total_rating_pages > 49 else total_rating_pages)+1):
        rating_list, userid_list, timestamp_list = get_ratings_info(movie_code, page)
        df = pd.DataFrame({
            'code': [movie_code] * len(rating_list),
            'userid': userid_list,
            'rating': rating_list,
            'timestamp': timestamp_list
        })
        df.to_csv('naver_korean_movie_ratings500.csv', mode='a', index=False, header=True if i == 0 and page == 1 else None)