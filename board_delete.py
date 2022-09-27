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

def art_del(artno) :
    sql = """
        delete from article
        where artno = {};""".format(artno)
    cur.execute(sql)
    
    sql = """
    delete from c, a
        using `comment` c
        inner join article a
        on c.artno = a.artno
    where c.artno = {};""".format(artno)
    cur.execute(sql)
        
    print("삭제되었습니다.")
    
def reply_del(userno, replyno):
    sql = """
        delete from `comment`
        where cno = {};""".format(replyno)
    cur.execute(sql)
    print("삭제되었습니다.")