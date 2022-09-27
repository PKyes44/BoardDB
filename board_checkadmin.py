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

def admin(userno):
    sql = """
        select ad.aoru 관리자여부
        from `user` u
        inner join `admin` ad
        on u.adno = ad.adno
        where u.uno = {};""".format(userno)
    cur.execute(sql)
    result = cur.fetchone()
    return result

def artadmin(userno, artno):
    sql = """
        select a.uno 작성자번호
        from `user` u
        inner join `admin` ad
        on u.adno = ad.adno
        inner join article a
        on u.uno = a.uno
        where artno = {};""".format(artno)
    cur.execute(sql)
    writer = cur.fetchone()
    
    result = admin(userno)
    
    if writer['작성자번호'] == userno:
        return True
    elif result['관리자여부'] == '관리자':
        return True
    else:
        return False

def replyadmin(userno, replyno):
    sql = """
        select u.uno 작성자번호
        from `user` u
        inner join `comment` c
        on u.uno = c.uno
        where c.cno = {};""".format(replyno)
    cur.execute(sql)
    writer = cur.fetchone()
    result = admin(userno)
    
    if writer['작성자번호'] == userno:
        return True
    elif result['관리자여부'] == '관리자':
        return True
    else:
        return False