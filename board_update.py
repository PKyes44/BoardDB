import pymysql as my
from pymysql import cursors
import board_detail as bdetail

# DB 연결
conn = my.connect(host = 'localhost', user = 'root',
                    password = '060404',cursorclass = cursors.DictCursor,
                    database='boards',
                    autocommit = True)
# 커서 지정
cur = conn.cursor()

def title(target, title):
    sql = """
        UPDATE article 
        SET title = '{}'
        WHERE artno = {};""".format(title, target)
    cur.execute(sql)
    print("수정완료")
    
    bdetail.onlyart(target)
    
def body(target, body):
    sql = """
        UPDATE article
        SET body = '{}'
        WHERE artno = {};""".format(body,target)
    cur.execute(sql)
    print("수정완료")
    
    bdetail.withreply(target)
    
def reply(cno, cbody):
    sql = """ 
        update `comment`
        set cbody = '{}'
        where cno = {};
        """.format(cbody, cno)
    cur.execute(sql)
    print('수정완료')
    
    sql = """
        select a.artno 게시물번호
        from `comment` c
        inner join article a
        on c.artno = a.artno
        where c.cno = {};""".format(cno)
    cur.execute(sql)
    artno = cur.fetchone()
    
    bdetail.withreply(artno['게시물번호'])