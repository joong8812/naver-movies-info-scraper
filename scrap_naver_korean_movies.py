import requests
from bs4 import BeautifulSoup
import pandas as pd

naver_movie_title_list = []
naver_movie_code_list = []

# 월별 한국 영화 제목과 영화 코드를 얻는다
def get_naver_movie_title_code(search_date):
    title_list = []
    code_list = []

    url = f'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cnt&tg=0&date={search_date}' # 해당 날짜 랭킹 정보 url
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    movies = soup.select('.title .tit3 a')

    for i, movie in enumerate(movies):
        movie_title = movie.text # 영화 제목
        movie_code = movie['href'].split('=')[-1] # 영화 코드
        
        movie_detail_url = f'https://movie.naver.com/movie/bi/mi/basic.naver?code={movie_code}' # 영화코드로 해당 영화의 정보를 볼 수 있는 url
        result = requests.get(movie_detail_url)
        soup = BeautifulSoup(result.text, "html.parser")
        movie_nationality = soup.select('.info_spec dd p span') # 영화 국적 정보 상위 태그
        if len(movie_nationality) > 1: # 만약 영화 정보 데이터가 있다면
            movie_nationality = soup.select('.info_spec dd p span')[1].text # 영화의 국적을 얻는다
        
            if movie_nationality.strip() == '한국': # 영화의 국적이 '한국' 이라면 제목과 코드를 리턴 리스트에 넣는다
                title_list.append(movie_title)
                code_list.append(movie_code)
    
    return title_list, code_list

# 20050206 - 20220106
search_date = 20050206 # 첫 검색 날짜 이후 다음달로 검색
df = pd.DataFrame()
while search_date < 20220107: # 2022년 1월 6일까지만 검색
    print(f"{search_date} search..")
    naver_movie_title_list, naver_movie_code_list = get_naver_movie_title_code(str(search_date)) # 해당 달의 한국영화 제목,코드 리스트 얻음
    new_df = pd.DataFrame({ # 크롤링한 영화제목, 코드를 Pandas Dataframe에 넣음
        'title': naver_movie_title_list,
        'code': naver_movie_code_list
    })
    df = pd.concat([df, new_df], ignore_index=True) # 기존 크롤링한 데이터에 더한다

    if (search_date % 10000) // 100 == 12: # 만약 12월이라면..? 
        search_date = search_date + 8900 # 다음해 1월로 변경
    else:
        search_date = search_date + 100 # 다음달로 변경
    


df = df.drop_duplicates(['title', 'code']) # 제목, 코드가 겹치는 데이터 삭제
df = df.reset_index(drop=True) # 인덱스를 처음부터 다시 정렬
print(df)
df.to_csv('naver_korean_movie_list.csv', index=False) # csv파일로 저장

'''
년월일별 네이버 영화 랭킹 url: https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cnt&tg=0&date=20050206
영화 상세 페이지 url: https://movie.naver.com/movie/bi/mi/basic.naver?code=39436
'''

'''
[진행 시 고려했던 점]
- 브라우저에서는 보이는 데 requests로 정보를 못가져오는 경우가 있음
- 국적정보 취득후 공백 삭제 필요
- 년월일 순차적으로 잘 바뀌도록
'''