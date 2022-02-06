import requests
from bs4 import BeautifulSoup
import pandas as pd

# 명대사 인기순으로 10개 리턴
def get_movie_quotes(movie_code, movie_title):
    qoute_list = []
    role_list = []
    actor_list = []

    url = f"https://movie.naver.com/movie/bi/mi/script.naver?code={movie_code}&order=best"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    
    quotes_info = soup.select('.lines_area2')
    for info in quotes_info:
        qoute_list.append(info.select_one('.one_line').text.strip())
        try:
            role_list.append(info.select_one('.char_part span').text.strip())
            actor_list.append(info.select_one('.char_part a').text.strip())
        except AttributeError as e:
            print(e)
            role_list.append('None')
            actor_list.append(info.select_one('.one_line + p a').text.strip())
        
    code_list = [movie_code] * len(quotes_info)
    title_list = [movie_title] * len(quotes_info)
    df = pd.DataFrame({ # 크롤링한 영화제목, 코드를 Pandas Dataframe에 넣음
        'code': code_list,
        'title': title_list,
        'role': role_list,
        'actor': actor_list,
        'quote': qoute_list,
    })    
    return df


korean_movie_table = pd.read_csv('./naver_korean_movie_list.csv', encoding='utf-8', sep=',') # 해당 csv파일은 'scrap_naver_korean_movies.py 에서 생성
for i, movie in enumerate(korean_movie_table.values):
    movie_title = movie[0]
    movie_code = movie[1]
    print(f'##### {i+1} ##### {movie_code} {movie_title}')

    df_movie_qoute = get_movie_quotes(movie_code, movie_title)
    df_movie_qoute.to_csv('naver_korean_movie_qoute.csv', mode='a', index=False, header=True if i == 0 else None)

'''
네이버영화 명대사 url: https://movie.naver.com/movie/bi/mi/script.naver?code=39436&order=best
'''