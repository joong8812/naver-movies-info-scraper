from queue import Empty
import requests
from bs4 import BeautifulSoup
import pandas as pd


# 영화 정보를 크롤링 하여 리턴
def get_movie_info(movie_code, movie_title):
    # sc_ : 스크랩한 데이터

    url = f"https://movie.naver.com/movie/bi/mi/basic.naver?code={movie_code}"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")

    # 장르(Genre)
    sc_genres = soup.select_one('.info_spec dd p span').select('a')
    genre = ''
    for sc_genre in sc_genres:
        sc_genre = sc_genre.text
        genre += sc_genre if genre == '' else f"|{sc_genre}"

    try:
        # 개봉날짜(Release, 년월일)
        release = soup.select_one('.info_spec dd p span:nth-of-type(4) a:nth-of-type(2)')['href'].split('=')[-1]

        # 상영시간(Duration, 단위:분)
        duration = soup.select_one('.info_spec dd p span:nth-of-type(3)').text.strip()[:-1]
    except TypeError as e:
        print(e)
        try:
            release = soup.select_one('.info_spec dd p span:nth-of-type(3) a:nth-of-type(2)')['href'].split('=')[-1]
        except TypeError as e:
            print(e)
            release = 'None'
        duration = 'None'

    try:
        # 관람가 등급(Maturity rating)
        maturity_rating = soup.select_one('.step4 + dd p a').text.replace("관람가", "").replace("세", "").strip()
    except AttributeError as e:
        print(e)
        maturity_rating = 'None'

    # 감독(Director)
    sc_directors = soup.select('.step2 + dd p a')
    director = ''
    for sc_director in sc_directors:
        sc_director = sc_director.text
        director += sc_director if director == '' else f"|{sc_director}"

    # 배우(Cast)
    sc_actors = soup.select('.step3 + dd p a')
    cast = ''
    for sc_actor in sc_actors:
        sc_actor = sc_actor.text
        cast += sc_actor if cast == '' else f"|{sc_actor}"

    # 줄거리(Plot)
    try:
        plot = soup.select_one('.con_tx').text.strip()
    except AttributeError as e:
        print(e)
        plot = 'None'

    df = pd.DataFrame({
                'code': movie_code,
                'title': movie_title,
                'genre': genre,
                'duration': duration,
                'release': release,
                'maturity_rating': maturity_rating,
                'director': director,
                'cast': cast,
                'plot': plot,
    }, index=[0])
    return df


korean_movie_table = pd.read_csv('./naver_korean_movie_list.csv', encoding='utf-8', sep=',') # 해당 csv파일은 'scrap_naver_korean_movies.py 에서 생성
for i, movie in enumerate(korean_movie_table.values):
    movie_title = movie[0]
    movie_code = movie[1]
    print(f'##### {i+1} ##### {movie_code} {movie_title}')

    df_movie_info = get_movie_info(movie_code, movie_title)
    df_movie_info.to_csv('naver_korean_movie_info.csv', mode='a', index=False, header=True if i == 0 else None)

