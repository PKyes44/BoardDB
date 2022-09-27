import pymysql as my
from pymysql import cursors
import pandas as pd

# DB 연결
conn = my.connect(host = 'localhost', user = 'root',
                    password = '060404',cursorclass = cursors.DictCursor,
                    database='boards',
                    autocommit = True)
# 커서 지정
cur = conn.cursor()

def printlist(sql):
    cur.execute(sql)
    art = cur.fetchall()
    if not art:
        print("검색할 게시물이 없습니다")
        return True
    artdf = pd.DataFrame(art)
    print(artdf.to_markdown())
    return False

def specific(target):
    sql = """
        select a.artno as 게시물번호, a.title as 제목, 
        u.nickname as 닉네임, a.`view` as 조회수, a.regDate as 등록날짜
        from article as a
        inner join `user` as u
        on a.uno = u.uno
        where a.bno = {}
        order by a.regDate desc;
        """.format(target)
    ifnone = printlist(sql)
    if ifnone:
        return True
    elif not ifnone:
        return False
    
def u_artall(userno):
    sql = """
        select a.artno 게시물번호, a.title 제목, u.nickname 작성자, a.regDate 등록날짜
        from article a
        inner join `user` u
        on a.uno = u.uno
        where u.uno = {}
        order by a.regDate desc""".format(userno)
    ifnone = printlist(sql)
    if ifnone:
        return True
    elif not ifnone:
        return False
        
def artall():
    sql = """
        select a.artno 게시물번호, b.bname 게시판종류, a.title 게시물제목,
        u.nickname 작성자, a.regDate 작성일
        from article a
        inner join `user` u
        on a.uno = u.uno
        inner join `board` b
        on a.bno = b.bno
        order by a.bno asc, a.regDate desc;"""
    ifnone = printlist(sql)
    if ifnone:
        return True
    elif not ifnone:
        return False
    
def u_replyall(userno):
    sql = """
        select a.title 게시물제목, c.cno 댓글번호, c.cbody 댓글내용, c.regDate 작성일
        from `comment` c
        inner join article a
        on a.artno = c.artno
        where c.uno = {}
        order by c.regDate desc;""".format(userno)
    ifnone = printlist(sql)
    if ifnone:
        return True
    elif not ifnone:
        return False