import pymongo

from flask import Flask, render_template

app = Flask(__name__)

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
