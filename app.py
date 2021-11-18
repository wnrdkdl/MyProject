import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('mongodb://test:test@localhost',27017)
# client = MongoClient('localhost', 27017)
db = client.dbsparta

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('pminfo.html')

@app.route('/default')
def pminfo():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/pmscrap', methods=['POST'])
def scrap_pminfo():
    db.pminfos.drop()
    # 1. 클라이언트로부터 데이터를 받기
    url_receive = request.form.get('url_give')

    # 2. meta tag를 스크래핑하기
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    items = soup.select('body > div > div > div.col-md-12.col-lg-8 > div.row > div.col-md-6 > a > div')

    for item in items:
        store = item.select_one('div.card-header > small:nth-child(1)').text
        img = item.select_one('div.card-body > div.prod_img_div > img')['src']
        info = item.select_one('div.card-body > div:nth-child(2)').text.split()

        doc = {
            "store" : store,
            "img" : img,
            "itemName" : info[0],
            "price" : info[1] + info[2] + " " + info[3],
            "pmtype" : info[4]
        }

        db.pminfos.insert_one(doc)

    if len(items) >= 1:
        result = 'success'
        msg = '해당 상품의 행사 정보입니다'
    else:
        result = 'fail'
        msg = '해당 상품의 행사 정보를 가져오지 못했습니다'

    return jsonify({'result': result, 'msg': msg})

@app.route('/pmscrap', methods=['GET'])
def showInfo():
    pminfos = list(db.pminfos.find({}, {"_id": False}))
    return jsonify({'result': 'success', 'pminfos': pminfos})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)