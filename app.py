
from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb://43.201.21.84', 27017, username="test", password="test")
db = client.forfeeling

import requests
from bs4 import BeautifulSoup

@app.route('/')
def happy():
    return render_template("happy.html")

@app.route('/joy')
def joy():
    return render_template("joy.html")

@app.route("/post", methods=["POST"])
def post():
    url_receive = request.form['url_give']
    feeling_receive = request.form['feeling_give']
    comment_receive = request.form['comment_give']

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
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



@app.route("/happy_get", methods=["GET"])
def happy_get():
    post_list = list(db.posts.find({'feeling':'기쁨'}, {'_id': False}))
    return jsonify({'posts':post_list})

@app.route("/joy_get", methods=["GET"])
def joy_get():
    post_list = list(db.posts.find({'feeling':'즐거움'}, {'_id': False}))
    return jsonify({'posts':post_list})

# @app.route("/joy_post", methods=["POST"])
# def joy_post():
#     url_receive = request.form['url_give']
#     feeling_receive = request.form['feeling_give']
#     comment_receive = request.form['comment_give']
#
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#     data = requests.get(url_receive, headers=headers)
#
#     soup = BeautifulSoup(data.text, 'html.parser')
#
#     title = soup.select_one('meta[itemprop="name"][content]')['content']
#     # 제목 뽑아오는 코드
#
#     doc = {
#         'title': title,
#         'url': url_receive,
#         'feeling': feeling_receive,
#         'comment': comment_receive
#     }
#     db.joys.insert_one(doc)
#     return jsonify({'msg': '저장 완료!'})

# @app.route("/joy_get", methods=["GET"])
# def joy_get():
#     post_list = list(db.joys.find({}, {'_id': False}))
#     return jsonify({'posts':post_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)