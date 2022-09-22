import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)

import jwt
import datetime
import hashlib
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

from pymongo import MongoClient
client = MongoClient('43.200.172.68', 27017, username="test", password="test")
db = client.forfeeling
# client = MongoClient('mongodb://43.201.21.84', 27017, username="test", password="test")
# db = client.forfeeling

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'



@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # jwt토큰을 해독한다
        user_info = db.users.find_one({"username": payload["id"]})
        mypage = "sad"
        return render_template('sad.html', user_info=user_info, page=mypage)
        # 요청한 유저정보를 html에 던져준다!
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

#joy페이지로 이동
@app.route('/joy')
def joy():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # jwt토큰을 해독한다
        user_info = db.users.find_one({"username": payload["id"]})
        mypage = "joy"
        return render_template('joy.html', user_info=user_info, page=mypage)
        # 요청한 유저정보를 html에 던져준다!
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
#happy 페이지로 이동
@app.route('/happy')
def happy():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # jwt토큰을 해독한다
        user_info = db.users.find_one({"username": payload["id"]})
        mypage = "happy"
        return render_template('happy.html', user_info=user_info, page=mypage)
        # 요청한 유저정보를 html에 던져준다!
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
#angry 페이지로 이동
@app.route('/angry')
def angry():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # jwt토큰을 해독한다
        user_info = db.users.find_one({"username": payload["id"]})
        mypage = "angry"
        return render_template('angry.html', user_info=user_info, page=mypage)
        # 요청한 유저정보를 html에 던져준다!
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

############################################### 로그인 기능 시작
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

    # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
@app.route('/user/<username>')
def user(username):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (username == payload["id"])
        # 내 프로필이면 True, 다른 사람 프로필 페이지면 False

        user_info = db.users.find_one({"username": username}, {"_id": False})
        return render_template('user.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # 로그인할때도 암호화를 진행한다 (랜덤이 아니구나!!!)
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        # result가 있다면 이라는 뜻이다..
        payload = {
        # 이게 곧 토큰이 됨.
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지| 60초X60X24
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')  # .decode('utf-8') 왠진몰라도 없으니 잘된다.
        #이건 토큰을 암호화 하는 것. 그대로 던져준다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    # 회원가입
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # 패스워드는 해쉬해준 뒤 저장한다!
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        "profile_pic": "",                                          # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
        "profile_info": ""                                          # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    # ID 중복확인
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    # username을 받아서 find_one으로 대조해보고 없으면 success, 있으면 bool로 exists로 바꿔줌.
    # bool 연산자는 참이라면 뱉고 거짓이면 뱉지 않는다. 거짓이면 자동적으로 result:success만 남겠지만
    # 만약 참이라면? exsist:exsist 가 뱉어질것이다.
    return jsonify({'result': 'success', 'exists': exists})

######################### 로그인기능 끝


#포스팅 루트
@app.route("/posting", methods=["POST"])
def music_post():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})

        url_receive = request.form['url_give']
        feeling_receive = request.form['feeling_give']
        comment_receive = request.form['comment_give']


        date_receive = request.form["date_give"]

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(url_receive, headers=headers)

        soup = BeautifulSoup(data.text, 'html.parser')

        title = soup.select_one('meta[itemprop="name"][content]')['content']
        # 제목 뽑아오는 코드

        doc = {
            "username": user_info["username"],
            "profile_name": user_info["profile_name"],
            "profile_pic_real": user_info["profile_pic_real"],
            'title': title,
            'url': url_receive,
            'feeling': feeling_receive,
            'comment': comment_receive,
            "date": date_receive
        }
        db.posts.insert_one(doc)
        return jsonify({"result": "success", 'msg': '저장 완료!'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        name_receive = request.form["name_give"]
        about_receive = request.form["about_give"]
        new_doc = {
            "profile_name": name_receive,
            "profile_info": about_receive
        }
        if 'file_give' in request.files:
            # request.files = 플라스크 에서 파일을 가져오는 방식 중 하나.
            # 'file_give'라는 키를 제시했으므로 그 밸류값에 있는 파일 링크를 가져온다.
            file = request.files["file_give"]

            filename = secure_filename(file.filename)
            # = 파일 경로를 보안 작업 하는거.
            extension = filename.split(".")[-1]
            # split()[-1] 은 쪼갠 값의 마지막 값을 요구 하는것.
            file_path = f"profile_pics/{username}.{extension}"
            # f string 이라는 건데
            file.save("./static/"+file_path)
            new_doc["profile_pic"] = filename
            new_doc["profile_pic_real"] = file_path
            # 느낌상 뭉쳐서 한번에 하려고 이러는거 같은데.
        db.users.update_one({'username': payload['id']}, {'$set':new_doc})
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

#sad 페이지 GET
@app.route("/getsad", methods=["GET"])
def post_get_sad():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # ############### 메인과 마이 페이지 구분을 위한 함수 #########
        username_receive = request.args.get("username_give")
        # url 파라미터로 받았기 때문에 request.args.get 을 쓴다고.
        if username_receive == "":
            posts = list(db.posts.find({'feeling':'슬픔'}).sort("date", -1).limit(20))
        else:
            posts = list(db.posts.find({"username": username_receive}).sort("date", -1).limit(20))
        for post in posts:
            post["_id"] = str(post["_id"])
        return jsonify({"result": "success", 'posts': posts})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))
# 밑은 일단 제쳐두고 sad만 합시다.
#joy 페이지 GET
@app.route("/gethappy", methods=["GET"])
def post_get_happy():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # ############### 메인과 마이 페이지 구분을 위한 함수 #########
        username_receive = request.args.get("username_give")
        # url 파라미터로 받았기 때문에 request.args.get 을 쓴다고.
        if username_receive == "":
            posts = list(db.posts.find({'feeling':'기쁨'}).sort("date", -1).limit(20))
        else:
            posts = list(db.posts.find({"username": username_receive}).sort("date", -1).limit(20))
        for post in posts:
            post["_id"] = str(post["_id"])
        return jsonify({"result": "success", 'posts': posts})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route("/getjoy", methods=["GET"])
def post_get_joy():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # ############### 메인과 마이 페이지 구분을 위한 함수 #########
        username_receive = request.args.get("username_give")
        # url 파라미터로 받았기 때문에 request.args.get 을 쓴다고.
        if username_receive == "":
            posts = list(db.posts.find({'feeling':'즐거움'}).sort("date", -1).limit(20))
        else:
            posts = list(db.posts.find({"username": username_receive}).sort("date", -1).limit(20))
        for post in posts:
            post["_id"] = str(post["_id"])
        return jsonify({"result": "success", 'posts': posts})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route("/getangry", methods=["GET"])
def post_get_angry():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # ############### 메인과 마이 페이지 구분을 위한 함수 #########
        username_receive = request.args.get("username_give")
        # url 파라미터로 받았기 때문에 request.args.get 을 쓴다고.
        if username_receive == "":
            posts = list(db.posts.find({'feeling':'분노'}).sort("date", -1).limit(20))
        else:
            posts = list(db.posts.find({"username": username_receive}).sort("date", -1).limit(20))
        for post in posts:
            post["_id"] = str(post["_id"])
        return jsonify({"result": "success", 'posts': posts})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)