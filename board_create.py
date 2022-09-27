#
import pymysql as my
from pymysql import cursors
# DB 연결
conn = my.connect(host = 'localhost', user = 'root',
                    password = '060404',cursorclass = cursors.DictCursor,
                    database='boards',
                    autocommit = True)
# 커서 지정
cur = conn.cursor()

def artcreate(userno, artkind, title, body):
    sql = """
        insert into article(uno, bno, title, body, `view`, regDate)
        values ({},{},'{}','{}',0,now());""".format(userno, artkind, title, body)
    cur.execute(sql)
    print("등록완료")
    
def replycreate(userno, artno, cbody):
    sql = """
        insert into `comment`(artno,uno,cbody,regDate)
        values ({},{},'{}',now());""".format(artno, userno, cbody)
    cur.execute(sql)
    print("등록완료")