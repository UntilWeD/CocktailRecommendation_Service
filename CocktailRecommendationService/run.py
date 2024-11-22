import os
import requests
from flask import Flask, render_template, request, jsonify
from app.service.service import CocktailService
from flask_cors import CORS
from dotenv import load_dotenv

cocktail_service = CocktailService()

load_dotenv()  # .env 파일 로드
api_key = os.getenv("GPT_API_KEY") # .env 파일에서 gpt api값 가져옴

app = Flask(__name__, static_folder="app/static",template_folder='app/templates')
CORS(app)

# @app.route('/') 
# def index():
#     return render_template("index.html")

@app.route('/')
def index():
    """
    메인 페이지 라우트
    - 데이터베이스에서 칵테일 정보 조회
    - GPT를 사용하여 각 칵테일에 대한 추천 생성
    - 결과를 웹 페이지로 표시
    """
    try:
        # 데이터베이스에서 칵테일 정보 조회
        cocktails = cocktail_service.get_cocktails()

        if cocktails is not None:
            recommendations = []

            # 각 칵테일에 대해 GPT 추천 생성
            for cocktail in cocktails[:5]:  # 테스트를 위해 처음 5개만 처리
                recommendation = cocktail_service.get_gpt_recommendation(cocktail)
                recommendations.append({
                    'original': cocktail,
                    'recommendation': recommendation
                })

            return render_template('gptRecommendations.html', recommendations=recommendations)
        else:
            return "데이터를 가져오는데 실패하였습니다."

    except Exception as e:
        return f"오류 발생: {str(e)}"

# @app.route('/gpt', methods=['POST']) # 이후 모달 추가 위해 @app.route('/detail/<id>') 삭제 
# def gpt_request():
#     data = request.json
#     question = data.get('question')

#     headers = {"Content-Type": "application/json"}
#     payload = {
#         "service": "gpt",
#         "question": question,
#         "hash": api_key
#     }
#     try:
#         response = requests.post("https://cesrv.hknu.ac.kr/srv/gpt", json=payload, headers=headers)
#         response.raise_for_status()
#         return jsonify(response.json())  # GPT API 응답 반환
#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)