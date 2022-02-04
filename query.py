import pymysql
import csv
import pandas as pd


def insert_movie_info(conn, curs):
    sql = 'insert into movie (`movie_id`, `title`, `genre`, `duration`, `release`, `maturity_rating`, `director`, `cast`, `plot`) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    korean_movie_info = pd.read_csv('./naver_korean_movie_info.csv', encoding='utf-8', sep=',', on_bad_lines='skip') # csv파일 불러오기
    for i, info in enumerate(korean_movie_info.values):
        print(f'##### {i+1} ##### {info[0]} {info[1]}')
        curs.execute(sql, (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8]))
        conn.commit()
    

conn = pymysql.connect(host='database-1.cfkksyjwetuh.ap-northeast-2.rds.amazonaws.com', user='admin', password='qwer1234', db='sys', charset='utf8')
curs = conn.cursor()
insert_movie_info(conn, curs)

conn.close()        
'''
1. 중복으로 들어있는 영화 데이터가 있다아아!! (같은 영화인데, 다른 타이틀 - 띄어쓰기, 영어타이틀, 부제, 가제 등)
2. 개봉 예정 작도 들어 있다.
'''