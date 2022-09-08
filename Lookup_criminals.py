from tabnanny import check
import pymysql as my
from pymysql import cursors
import pandas as pd
from pandas import DataFrame
import os

# 쿼리 DB에 적용
def applySQL(sql,read):
    cur.execute(sql)
    if read :
        content = cur.fetchall()
        return content

# DB 연결
conn = my.connect(host = 'localhost', user = 'root',
                    password = '060404', cursorclass = cursors.DictCursor,
                    autocommit = True)
# 커서 지정
cur = conn.cursor()   

# DB에 crime 데이터베이스가 있는지 확인
sql = "SHOW DATABASES LIKE 'crime';"
DBCheck = applySQL(sql,True)

# 없을경우 생성
if not DBCheck:
    sql = """
    CREATE DATABASE crime;
    """
    applySQL(sql,False)
    sql = "USE crime;"
    applySQL(sql,False)
    sql = """
    CREATE TABLE criminal (
	crimeid INT PRIMARY KEY,
	crimename VARCHAR(10),
	guilt VARCHAR(10),
	crimescore INT(255)
);"""
    applySQL(sql,False)
    sql = """
    ALTER TABLE criminal
    MODIFY crimeid INT AUTO_INCREMENT;"""
    applySQL(sql,False)
# 있을 경우 DB 선택
else:
    sql = "USE crime;"
    applySQL(sql,False)

while(1):
    print("범죄자 조회 프로그램")
    menu = int(input("1.기록 2.조회 3.삭제 4.종료 : "))

    # 기록
    if menu == 1:
        name = input("이름을 입력해주세요 : ")
        crime = input("범죄명을 입력해주세요 : ")
        
        if crime == '사기':
            score = 1
        elif crime == '절도': 
            score = 2
        elif crime == '살인':
            score = 3
        else:
            score = 4
        
        # insert 쿼리
        sql = """
        INSERT INTO criminal (crimename, guilt, crimescore)
        VALUE ('{}','{}',{});""".format(name,crime,score)
        applySQL(sql,False)
        
        print("저장완료")
    # 조회   
    elif menu == 2:
        segment = int(input("1. 범죄점수 조회 2. 범죄이력 조회 3. 전체데이터 조회 : "))
                
        # 데이터 없는지 체크 ( 에러방지 )
        sql = "SELECT COUNT(crimeid) FROM criminal;"
        cur.execute(sql)
        Empty = cur.fetchall()
        if Empty == '0':
            print("값이 없습니다.")
            continue
        
        # 대상 지정
        if segment != 3:
            target = input("조회할 대상의 이름을 입력해주세요\n모든 유저를 조회하려면 all을 입력해주세요 : ")
            
        # 범죄점수 조회
        if segment == 1 :
            if target == 'all' :
                sql = """
                SELECT crimename AS '이름', SUM(crimescore) AS '범죄점수'
                FROM criminal
                GROUP BY crimename;"""
            else :
                sql = """
                SELECT crimename AS '이름', SUM(crimescore) AS '범죄점수'
                FROM criminal
                WHERE crimename = '{}'
                GROUP BY crimename;""".format(target)
        # 범죄이력 조회
        elif segment == 2 :
            if target == 'all':
                sql = """
                SELECT crimeid as '번호', crimename as '이름', guilt as '범죄명'
                FROM criminal
                ORDER BY crimeid ASC;"""
            else :
                sql = """
                SELECT crimeid as '번호', crimename as '이름', guilt as '범죄명'
                FROM criminal
                WHERE crimename = '{}'
                ORDER BY crimeid ASC;""".format(target)
        # 모든 데이터 조회
        else :
            sql = """
            SELECT crimeid as '번호', crimename as '이름', guilt as '범죄명', crimescore as '범죄점수'
            FROM criminal;"""
        tmp_out = applySQL(sql,True)
        
        # 데이터프레임으로 출력
        df = pd.DataFrame(tmp_out)
        print(df.to_markdown())
    # 데이터 삭제
    elif menu == 3:
        target = input("삭제할 데이터의 번호를 입력해주세요\n전체 삭제하려면 all을 입력해주세요 : ")
        if target == 'all':
            check_delete = int(input("정말로 데이터 전체 삭제하시겠습니까 ?\n1.YES 2.NO : "))
            if check_delete == 1:
                sql = """
                DELETE FROM criminal"""
            elif check_delete == 2:
                print("메뉴로 돌아갑니다")
        else:
            sql = """
            DELETE FROM criminal
            WHERE crimeid = {};""".format(target)
        applySQL(sql,False)
    elif menu == 4:
        break
    
quit()