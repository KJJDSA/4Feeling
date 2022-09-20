
from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.i6a0slt.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta_plus_week4

import requests
from bs4 import BeautifulSoup

@app.route('/')
def main():
    return render_template("index.html")

@app.route("/post", methods=["POST"])
def music_post():
    url_receive = request.form['url_give']
    feeling_receive = request.form['feeling_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[itemprop="name"][content]')['content']

    doc = {
        'title': title,
        'url': url_receive,
        'feeling': feeling_receive,
        'comment': comment_receive
    }
    db.posts.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})

@app.route("/post_get", methods=["GET"])
def post_get():
    post_list = list(db.posts.find({}, {'_id': False}))
    return jsonify({'posts':post_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)