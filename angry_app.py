from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.oqxmexp.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/angry')
def index():
    return render_template('angry.html')


@app.route("/angry", methods=["POST"])
def angry_post():
    url_receive = request.form['url_give']
    title_receive = request.form['title_give']
    name_receive = request.form['name_give']
    feeling_receive = request.form['feeling_give']
    comment_receive = request.form['comment_give']

    doc = {
        'url': url_receive,
        'title': title_receive,
        'name': name_receive,
        'feeling': feeling_receive,
        'comment': comment_receive
    }
    db.angrys.insert_one(doc)

    return jsonify({'msg':'추천 완료!'})

@app.route("/angry", methods=["GET"])
def angry_get():
    angry_list = list(db.angrys.find({}, {'_id': False}))
    return jsonify({'angrys': angry_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)