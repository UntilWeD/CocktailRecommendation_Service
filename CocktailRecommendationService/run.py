import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder="app/static",template_folder='app/templates')
CORS(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/detail/<id>')
def detail(id):
    return render_template('detail.html')

@app.route('/gpt', methods=['POST'])
def gpt_request():
    data = request.json
    question = data.get('question')

    headers = {"Content-Type": "application/json"}
    payload = {
        "service": "gpt",
        "question": question,
        "hash": "a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0"
    }
    try:
        response = requests.post("https://cesrv.hknu.ac.kr/srv/gpt", json=payload, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())  # GPT API 응답 반환
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)