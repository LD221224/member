import sqlite3

from flask import request


def getconn():
    conn = sqlite3.connect('./members.db')
    return conn


def select_member():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member ORDER BY regDate DESC"
    cur.execute(sql)
    rs = cur.fetchall()
    conn.close()
    return rs


def select_one(id):
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE mid = '%s'" % (id)
    cur.execute(sql)
    rs = cur.fetchone()
    conn.close()
    return rs


def join_member():
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
    return rs


def login_member():
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
    return rs


def delete_member(id):
    conn = getconn()
    cur = conn.cursor()
    sql = "PRAGMA foreign_keys = ON"
    cur.execute(sql)
    sql = "DELETE FROM member WHERE mid = '%s'" % (id)
    cur.execute(sql)
    conn.commit()
    conn.close()


def update_member(id):
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

