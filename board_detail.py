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

def print_detail(article, replies, pr_com) :
    print("================== 게시물 상세보기 ===================")
    print("번호 : {}".format(article["artno"])) 
    print("제목 : {}".format(article["title"]))
    print("내용 : {}".format(article["body"]))
    print("작성자 : {}".format(article["nickname"]))
    print("작성일 : {}".format(article["regDate"]))      
    print("------------------------------------------------------")
    if pr_com:
        print("댓글 {}".format(len(replies)))
        print("------------------------------------------------------")
        for reply in replies :
            print("내용 : {}".format(reply["cbody"]))
            print("작성자 : {}".format(reply["nickname"]))
            print("작성일 : {}".format(reply["regDate"]))
            print("--------------------------------------------------------")
        
def onlyart(target):           
    # 상세보기 하고싶은 게시물 정보 가져오기
    sql = """select a.artno, a.title, a.body, a.`view`, a.regDate, u.nickname
            from article as a
            inner join `user` as u
            on u.uno = a.uno
            where a.artno = {};""".format(target)
    cur.execute(sql)
    art_list = cur.fetchone()
    print_detail(art_list,0,False)

def withreply(target):
    sql = """select a.artno, a.title, a.body, a.`view`, a.regDate, u.nickname
        from article as a
        inner join `user` as u
        on u.uno = a.uno
        where a.artno = {};""".format(target)
    cur.execute(sql)
    art_list = cur.fetchone()
    sql = """
        select *
        from `comment` as c
        inner join article as a
        on c.artno = a.artno
        inner join `user` as u
        on u.uno = c.uno
        where a.artno = {};
            """.format(target)
    cur.execute(sql)
    reply_list = cur.fetchall()
    print_detail(art_list,reply_list,True)