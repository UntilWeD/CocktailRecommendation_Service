import os
import requests
from flask import Flask, render_template, request, jsonify
from app.service.service import CocktailService
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__, template_folder='app/templates')

cocktail_service = CocktailService()


load_dotenv()  # .env 파일 로드
api_key = os.getenv("GPT_API_KEY")

app = Flask(__name__, static_folder="app/static",template_folder='app/templates')
CORS(app)

@app.route('/')
def index():
    return render_template("index.html")

# def get_db_data():
#     try:
#         data = cocktail_service.get_cocktails()
#
#         if data is not None:
#             return render_template('index.html', data=data)
#         else:
#             return "데이터를 가져오는데 실패하였습니다."
#
#     except Exception as e:
#         return f"에러 발생: {str(e)}"

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
        "hash": api_key
    }
    try:
        response = requests.post("https://cesrv.hknu.ac.kr/srv/gpt", json=payload, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())  # GPT API 응답 반환
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)