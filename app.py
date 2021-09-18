from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

SECRET_KEY = 'TEAM19'

# client = MongoClient('localhost', 27017) # db 로컬
client = MongoClient('mongodb://test:test@localhost', 27017) # db aws
db = client.hh99_nickname # db연결
# db = client.nickname


###### html 연결하기 ###########

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])               # 로그인된 jwt 토큰 디코드하여 payload 설정
        user_info = db.usersdb.find_one({"username": payload["id"]})                        # 로그인 정보를 토대로 user_info 설정
        return render_template('index.html', user_info=user_info)                           # index.html에 user_info 전달
    except jwt.ExpiredSignatureError:                                                       # 토큰이 만료되면 에러대신 login으로 이동
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))                   # 만료 !
    except jwt.exceptions.DecodeError:                                                      # 복호화에 실패하면 에러대신 login으로 이동
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))                # 토큰 복호화 실패 !

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/myPage')
def get_myname():
    return render_template('myPage.html')


@app.route('/sign_in', methods=['POST'])
def sign_in():                                                                              # <로그인>
    username_receive = request.form['username_give']                                        # login.html에서 보내준 로그인 입력 정보 변수에 담기
    password_receive = request.form['password_give']


    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()                  # 비밀번호 해싱
    result = db.usersdb.find_one({'username': username_receive, 'password': pw_hash})       # 유저정보 DB 검색하여 T/F

    if result is not None:                                                                  # 유저정보가 True면(db에 있으면)
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')          # 토큰에 정보를 담아서

        return jsonify({'result': 'success', 'token': token})                               # 결과 성공과 토큰 보내주기
    else:                                                                                   # 유저정보가 False면(db에 없으면)
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})         # 결과 실패와 실패문구 보내주기


@app.route('/sign_up/save', methods=['POST'])
def sign_up():                                                                              # <회원가입>
    username_receive = request.form['username_give']                                        # login.html에서 보내준 회원가입 정보 변수에 담기
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()            # 비밀번호 해싱
    doc = {
            'username': username_receive,
            'password': password_hash
    }

    db.usersdb.insert_one(doc)                                                              # username과 password 를 db에 저장

    return jsonify({'result': 'success'})                                                   # 결과 성공

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():                                                                            # <아이디 중복 확인>
    username_receive = request.form['username_give']                                        # username을 받아 옴
    exists = bool(db.usersdb.find_one({"username": username_receive}))                      # username이 DB에 존재 유무를 T/F
    # print(value_receive, type_receive, exists)
    return jsonify({'result': 'success', 'exists': exists})                                 # 중복이면 T/ 아니면 F 를 전송


@app.route('/get_mynick', methods=['GET'])
def get_mynick():                                                                           # <닉네임 생성하기>
    nickname = list(db.wordsdb.find({}, {'_id': False}))
    return jsonify({'all_nickname': nickname})

@app.route('/save_mynick', methods=['POST', 'GET'])
def save_nick():                                                                            # <닉네임 저장하기>
    nick_receive = request.form['nick_give']                                                # 생성된 닉네임과 아이디 받기
    cookieId_receive = request.form['cookieId_give']

    id_list = list(db.mynick.find({'cookieId': cookieId_receive}, {'_id': False}))          # 받아온 아이디가 같은 닉네임 찾아서 리스트에 담기(닉네임 저장 개수)

    id_count = len(id_list)

    print(id_count)


    if id_count < 8:                                                                        # 저장된 닉네임이 8개 미만이면
        doc = {
            'cookieId': cookieId_receive,
            'nick': nick_receive
        }
        db.mynick.insert_one(doc)                                                           # 닉네임 DB에 저장하기
    else:                                                                                   # 저장된 닉네임이 8개 이상 있다면
        delete_nick = id_list[0]
        db.mynick.delete_one(delete_nick)                                                   # 첫번째 닉네임을 삭제하고
        doc = {
            'cookieId': cookieId_receive,
            'nick': nick_receive
        }
        db.mynick.insert_one(doc)                                                           # 새로 받은 닉네임 저장

@app.route('/view_mynick', methods=['GET'])
def view_nick():                                                                            # <마이페이지 닉네임 출력>

    mynicks = list(db.mynick.find({                                                         # 로그인된 아이디와 같은 값을 가지는 닉네임들 리스트 변수에 담기
        'cookieId': request.cookies.get('id')},
        {'_id': False}))

    return jsonify({'mynicks': mynicks})                                                    # 변수 보내주기



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)