import pymysql as my
from pymysql import cursors
import pandas as pd

def enter():
    # DB 연결
    conn = my.connect(host = 'localhost', user = 'root',
                        password = '060404',cursorclass = cursors.DictCursor,
                        database='boards',
                        autocommit = True)
    # 커서 지정
    cur = conn.cursor()
    while(True):
        Check_new = int(input("1.로그인 2.회원가입 : "))
        if Check_new == 1:
                logid = input("아이디 : ")
                logpw = input("비밀번호 : ")
                sql = """
                    select *
                    from `user`
                    where logid = '{}' and logpw = '{}';""".format(logid,logpw)
                cur.execute(sql)
                Ch_success = cur.fetchall()
                
                if Ch_success:
                    print("로그인 완료")
                    break
                elif not Ch_success:
                    print("잘못입력하셨습니다.\n다시시도해주세요")
        elif Check_new == 2:
            admin = input("관리자로 로그인하시겠습니까?\nY/N : ")
            logid = input("아이디 : ")
            logpw = input("비밀번호 : ")
            realname = input("실명 : ")
            nickname = input("닉네임 : ")
            if admin == 'Y':
                sql = """
                insert into `user`(adno,logid,logpw,realname,nickname,regDate)
                values (0,'{}','{}','{}','{}',now());
                """.format(logid,logpw,realname,nickname)
            elif admin == 'N':
                sql = """
                insert into `user`(adno,logid,logpw,realname,nickname,regDate)
                values (1,'{}','{}','{}','{}',now());
                """.format(logid,logpw,realname,nickname)
            cur.execute(sql)
            print("등록되었습니다.")
            sql = """
                select logid 아이디, logpw 패스워드, nickname 닉네임, regDate 등록날짜
                from `user`
                where logid = '{}'
                    and logpw = '{}'
                    and realname = '{}'
                    and nickname = '{}';""".format(logid,logpw,realname,nickname)
            cur.execute(sql)
            out_success = cur.fetchall()
            df = pd.DataFrame(out_success)
            print(df.to_markdown())
            break
        else : 
            print("다시 입력하세요")
    sql = """
        select uno
        from `user`
        where logid = '{}' and logpw = '{}';""".format(logid,logpw)
    cur.execute(sql)
    userno = cur.fetchone()

    return userno['uno']