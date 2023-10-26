'''
CORS(교차출처자원공유) 오류 재현 및 테스트
'''

from flask import Flask, jsonify
from flask_cors import CORS
from flask import render_template

app1 = Flask(__name__)

# Access-Control-Allow-Origin 설정
CORS(app1, resources={
    r'*': {'origin':'http://localhost:5000/'}
    })
CORS(app1)

@app1.route('/')
def index():
    data = {'message': 'CORS 문제가 없는 데이터 입니다.'}
    return jsonify(data)

@app1.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app1.run(host='0.0.0.0', port=5000, debug=True)
