import pymysql as my
from pymysql import cursors
import board_login  as blogin, board_list as blist, board_detail as bdetail
import board_create as bc, board_delete as bdelete, board_update as bu
import board_checkadmin as bca

# mysql 연결
conn = my.connect(host = 'localhost', user = 'root',
                    password = '060404',cursorclass = cursors.DictCursor,
                    database='boards',
                    autocommit = True)
# 커서 지정
cur = conn.cursor()

# 로그인 후 유저번호 반환
userno = blogin.enter()

while(True):
    menu = int(input("1.게시판보기 2.게시물 등록 3.게시물/댓글수정\n4.게시물/댓글삭제 5.로그아웃(재로그인) 6.프로그램종료 : "))
    
    # 게시판보기 /
    if menu == 1:
        kind_of_art = int(input("1.공지사항 2.질문과응답 3.자유 4.전체보기 : "))
        if kind_of_art < 4:
            ifnone = blist.specific(kind_of_art)
        elif kind_of_art == 4:
            ifnone = blist.artall()
        if not ifnone:
            artno = int(input("상세보기할 게시물의 번호를 입력해주세요 : "))
            bdetail.withreply(artno)
            # 댓글 등록
            reply = input("해당 게시물에 댓글을 등록하시겠습니까?\nY/N : ")
            if reply == 'Y':
                cbody = input("댓글 내용을 입력해주세요 : ")
                bc.replycreate(userno,artno,cbody)
        
    # 등록 / 
    elif menu == 2:
        kind_of_art = int(input("게시판 종류를 선택해주세요\n1.공지사항 2.질문과응답 3.자유 : "))
        title = input("게시물 제목 : ")
        body = input("게시물 내용 : ")
        bc.artcreate(userno, kind_of_art, title, body)
        
    # 수정 /
    elif menu == 3:
        update = int(input("1.제목수정 2.내용수정 3.댓글수정 : "))
        if update == 1:
            ifnone = blist.u_artall(userno)
            if not ifnone:
                artno = input("수정할 게시물 번호를 입력해주세요 : ")
                result = bca.artadmin(userno,artno)
                if result:
                    title = input("{}번 게시물 제목수정 : ".format(artno))
                    bu.title(artno, title)
                else :
                    print("작성자가 아니거나 관리자가 아닙니다.")
        elif update == 2:
            ifnone = blist.u_artall(userno)
            if not ifnone:
                artno = input("수정할 게시물 번호를 입력해주세요 : ")
                result = bca.artadmin(userno,artno)
                if result:
                    bdetail.onlyart(artno)
                    body = input("게시물 내용을 수정해주세요 : ")
                    bu.body(artno, body)
                else :
                    print("게시물 작성자가 아니거나 관리자가 아닙니다.")
        elif update == 3:
            ifnone = blist.u_replyall(userno)
            if not ifnone:
                replyno = input("수정할 댓글의 번호를 입력해주세요 : ")
                result = bca.replyadmin(userno,replyno)
                if result:
                    cbody = input("댓글 내용을 수정해주세요 : ")
                    bu.reply(replyno,cbody)
                else :
                    print("댓글 작성자가 아니거나 관리자가 아닙니다.")
        
    # 삭제
    elif menu == 4:
        del_target = int(input("1.게시물삭제 2.댓글삭제 : "))
        if del_target == 1:
            ifnone = blist.u_artall(userno)
            if not ifnone:
                artno = int(input("삭제할 게시물의 번호를 입력해주세요 : "))
                result = bca.artadmin(userno, artno)
                if result:
                    bdelete.art_del(artno)
                else :
                    print("게시물 작성자가 아니거나 관리자가 아닙니다")
        elif del_target == 2:
            ifnone = blist.u_replyall(userno)
            if not ifnone:
                replyno = int(input("삭제할 댓글의 번호를 입력해주세요 : "))
                result = bca.replyadmin(userno, replyno)
                if result:
                    bdelete.reply_del(userno, replyno)
                else :
                    print("댓글 작성자가 아니거나 관리자가 아닙니다")
    
    # 재로그인
    elif menu == 5:
        userno = blogin.enter()
    
    # 종료
    else:
        quit(0)
        
    print("메뉴로 돌아갑니다.")