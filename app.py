import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session

from model.model_board import select_board, select_bo_one, \
    write_board, delete_board, update_board
from model.model_member import getconn, select_member, select_one, \
    join_member, login_member, delete_member, update_member

app = Flask(__name__)

app.secret_key = "#abcde"


# index 페이지
@app.route('/')
def index():
    return render_template('index.html')
    # return "Hello~ flask"


# 회원 목록 페이지
@app.route('/memberlist/')
def memberlist():
    rs = select_member()
    return render_template('memberlist.html', rs=rs)


# 회원 상세 페이지
@app.route('/member_view/<string:id>/')
def member_view(id):
    rs = select_one(id)
    return render_template('member_view.html', rs=rs)


# 회원 가입 페이지
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        rs = join_member()
        # 세션 발급
        if rs:
            session['userID'] = rs[0]
            session['userName'] = rs[2]
            # redirect - 페이지 이동 함수
            return redirect(url_for('memberlist'))
    else:
        return render_template('register.html')


# 로그인 페이지
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        rs = login_member()
        if rs:
            # 아이디로 세션 발급
            session['userID'] = rs[0]
            session['userName'] = rs[2]
            # 로그인 후 인덱스페이지로 이동
            return redirect(url_for('index'))
        else:
            error = "아이디나 비밀번호를 확인해주세요."
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


# 로그아웃 페이지
@app.route('/logout/')
def logout():
    # 세션 삭제
    # session.pop("userID")
    # session.pop("userName")
    session.clear()
    return redirect(url_for('index'))


# 회원 삭제
@app.route('/member_del/<string:id>/')
def member_del(id):
    delete_member(id)
    return redirect(url_for('memberlist'))


# 회원 수정
@app.route('/member_edit/<string:id>/', methods=['GET', 'POST'])
def member_edit(id):
    if request.method == 'POST':
        update_member(id)
        return redirect(url_for('member_view', id=id))
    else:
        rs = select_one(id)
        return render_template('member_edit.html', rs=rs)


# 게시글 목록 페이지
@app.route('/boardlist/')
def boardlist():
    rs = select_board()
    return render_template('boardlist.html', rs=rs)


# 게시글 상세 페이지
@app.route('/board_view/<int:bno>/')
def board_view(bno):
    rs = select_bo_one(bno)
    return render_template('board_view.html', rs=rs)


# 게시글 작성 페이지
@app.route('/writing/', methods=['GET', 'POST'])
def writing():
    if request.method == 'POST':
        write_board()
        return redirect(url_for('boardlist'))
    else:
        return render_template('writing.html')


# 게시글 삭제
@app.route('/board_del/<int:bno>/')
def board_del(bno):
    delete_board(bno)
    return redirect(url_for('boardlist'))


# 게시글 수정
@app.route('/board_edit/<int:bno>/', methods=['GET', 'POST'])
def board_edit(bno):
    if request.method == 'POST':
        update_board(bno)
        return redirect(url_for('board_view', bno=bno))
    else:
        rs = select_bo_one(bno)
        return render_template('board_edit.html', rs=rs)


app.run(debug=True)
