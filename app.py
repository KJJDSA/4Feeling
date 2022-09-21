import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb://43.201.21.84', 27017, username="test", password="test")
db = client.forfeeling

@app.route('/')
def main():
    return render_template("index.html")
#joy페이지로 이동
@app.route('/joy')
def joy():
    return render_template("joy.html")
#happy 페이지로 이동
@app.route('/happy')
def happy():
    return render_template("happy.html")
#angry 페이지로 이동
@app.route('/angry')
def angry():
    return render_template("angry.html")

#포스팅 루트
@app.route("/posting", methods=["POST"])
def music_post():
    url_receive = request.form['url_give']
    feeling_receive = request.form['feeling_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[itemprop="name"][content]')['content']
    # 제목 뽑아오는 코드

    doc = {
        'title': title,
        'url': url_receive,
        'feeling': feeling_receive,
        'comment': comment_receive
    }
    db.posts.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})

#sad 페이지 GET
@app.route("/sad_get", methods=["GET"])
def post_get():
    post_list = list(db.posts.find({'feeling':'슬픔'}, {'_id': False}))
    return jsonify({'posts': post_list})

#joy 페이지 GET
@app.route("/joy_get", methods=["GET"])
def joy_get():
    post_list = list(db.posts.find({'feeling':'즐거움'}, {'_id': False}))
    return jsonify({'posts':post_list})

#happy 페이지 GET
@app.route("/happy_get", methods=["GET"])
def happy_get():
    post_list = list(db.posts.find({'feeling':'기쁨'}, {'_id': False}))
    return jsonify({'posts':post_list})
#angry 페이지 GET
@app.route("/angry_get", methods=["GET"])
def angry_get():
    post_list = list(db.posts.find({'feeling':'분노'}, {'_id': False}))
    return jsonify({'posts':post_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)