from flask import request, session

from model.model_member import getconn


def select_board():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board ORDER BY bno DESC"
    cur.execute(sql)
    rs = cur.fetchall()
    conn.close()
    return rs


def select_bo_one(bno):
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board WHERE bno = '%s'" % (bno)
    cur.execute(sql)
    rs = cur.fetchone()

    # 조회수 + 1
    hit = rs[4] + 1
    sql = "UPDATE board SET hit = '%s' " \
          "WHERE bno = '%s'" % (hit, bno)
    cur.execute(sql)
    conn.commit()

    conn.close()
    return rs


def write_board():
    # 데이터 가져오기
    title = request.form['title']
    content = request.form['content']
    hit = 0
    # mid = 로그인 되어있는 name
    mid = session.get('userName')

    # DB 연동
    conn = getconn()
    cur = conn.cursor()
    sql = "INSERT INTO board(title, content, hit, mid) " \
          "VALUES('%s', '%s', '%s', '%s')" % (title, content, hit, mid)
    cur.execute(sql)
    conn.commit()
    conn.close()


def delete_board(bno):
    conn = getconn()
    cur = conn.cursor()
    sql = "DELETE FROM board WHERE bno = '%s'" % (bno)
    cur.execute(sql)
    conn.commit()
    conn.close()


def update_board(bno):
    # 데이터 가져오기
    title = request.form['title']
    content = request.form['content']
    mid = session.get('userName')
    # DB 연동
    conn = getconn()
    cur = conn.cursor()
    sql = "UPDATE board SET title = '%s', content = '%s', mid = '%s' " \
          "WHERE bno = '%s'" % (title, content, mid, bno)
    cur.execute(sql)
    conn.commit()
    conn.close()