import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = "#abcde"


# DB 접속
def getconn():
    conn = sqlite3.connect('./members.db')
    return conn


# index 페이지
@app.route('/')
def index():
    return render_template('index.html')
    # return "Hello~ flask"


# 회원 목록 페이지
@app.route('/memberlist/')
def memberlist():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member ORDER BY regDate DESC"
    cur.execute(sql)
    rs = cur.fetchall()
    conn.close()
    return render_template('memberlist.html', rs=rs)


# 회원 상세 페이지
@app.route('/member_view/<string:id>/')
def member_view(id):
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE mid = '%s'" % (id)
    cur.execute(sql)
    rs = cur.fetchone()
    conn.close()
    return render_template('member_view.html', rs=rs)


# 회원 가입 페이지
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 데이터 가져오기
        id = request.form['mid']
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']

        # DB에 저장 - 회원 가입 완료
        conn = getconn()
        cur = conn.cursor()
        sql = "INSERT INTO member(mid, passwd, name, age) " \
              "VALUES('%s', '%s', '%s', '%s')" % (id, pwd, name, age)
        cur.execute(sql)
        conn.commit()

        # 자동 로그인
        sql = "SELECT * FROM member WHERE mid = '%s' AND passwd = '%s'" % (id, pwd)
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()

        # 세션 발급
        if rs:
            session['userID'] = rs[0]
            # redirect - 페이지 이동 함수
            return redirect(url_for('memberlist'))
    else:
        return render_template('register.html')


# 로그인 페이지
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # 입력된 아이디, 비밀번호 가져오기
        id = request.form['mid']
        pwd = request.form['passwd']

        # DB 연동
        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s' AND passwd = '%s'" % (id, pwd)
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()
        if rs:
            # 아이디로 세션 발급
            session['userID'] = rs[0]
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
    session.pop("userID")
    return redirect(url_for('index'))


# 회원 삭제
@app.route('/member_del/<string:id>/')
def member_del(id):
    conn = getconn()
    cur = conn.cursor()
    sql = "DELETE FROM member WHERE mid = '%s'" % (id)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return redirect(url_for('memberlist'))


# 회원 수정
@app.route('/member_edit/<string:id>/', methods=['GET', 'POST'])
def member_edit(id):
    if request.method == 'POST':
        # 데이터 가져오기
        mid = request.form['mid']
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']

        # DB 수정
        conn = getconn()
        cur = conn.cursor()
        sql = "UPDATE member SET passwd = '%s', name = '%s', age = '%s' " \
              "WHERE mid = '%s'" % (pwd, name, age, mid)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect(url_for('member_view', id=id))
    else:
        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s'" % (id)
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()
        return render_template('member_edit.html', rs=rs)


@app.route('/boardlist/')
def boardlist():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board ORDER BY bno DESC"
    cur.execute(sql)
    rs = cur.fetchall()
    conn.close()
    return render_template('boardlist.html', rs=rs)


@app.route('/board_view/<int:id>/')
def board_view(id):
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board WHERE bno = '%s'" % (id)
    cur.execute(sql)
    rs = cur.fetchone()
    conn.close()
    return render_template('board_view.html', rs=rs)


app.run(debug=True)
