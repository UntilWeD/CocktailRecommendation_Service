import os
import requests
from flask import Flask, render_template, request, redirect, session,jsonify, url_for
from app.service.service import CocktailService, UserService
from flask_cors import CORS
from dotenv import load_dotenv
from flask_login import LoginManager, login_user
from app.service.db import CocktailDBService
import json

# .env 파일 로드
load_dotenv()
api_key = os.getenv("GPT_API_KEY")  # .env 파일에서 GPT API 키 가져오기
if not api_key:
    raise ValueError("GPT_API_KEY is not set in the environment variables.")

import openai
openai.api_key = api_key  # OpenAI API 키 설정

app = Flask(__name__, static_folder="app/static",template_folder='app/templates')

# 서비스 객체 생성
db_service = CocktailDBService()
cocktail_service = CocktailService()
user_service = UserService()
# 세션 암호화 키
app.secret_key = 'your_secret_key_here'


CORS(app)

# 후에 세션에서 사용자의 이메일값을 알기위해서는
# user_email = session.get('email') 로 사용하면 됨

@app.route('/') 
def index():
    if 'email' in session:
        return render_template("index.html", email = session.get('email'), login = True)
    else:
        return render_template("index.html",login = False)

# 회원가입
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email is None or password is None:
            return redirect('/register')

        # db에 회원정보 저장
        user_service.register_user(email, password)
        return redirect('/login')

# 로그인
@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'GET':
        return render_template("login.html")

    if request.method == 'POST':
        #form 방식
        email = request.form.get('email')
        password = request.form.get('password')

        if email is None or password is None:
            return redirect('/login')

        # db에서 회원정보 조회
        user = user_service.get_user(email, password)

        # user가 존재한다면 세션에 저장
        if user is not None:
            session['email'] = user['email']
            return redirect('/')
        else:
            # 그렇지 않다면 다시 로그인 페이지로
            return redirect('/login')

# 로그아웃
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

# GPT 생성 및 추천
@app.route('/recommend', methods=['POST'])
def recommend():
    """
    사용자의 입력을 받아 데이터베이스 정보를 기반으로 GPT 추천 결과를 반환.
    """
    try:
        # 클라이언트 요청 데이터 받기
        data = request.get_json()
        description = data.get('description')

        if not description:
            return jsonify({'error': '입력이 필요합니다.'}), 400

        # 데이터베이스에서 모든 칵테일 데이터 조회
        cocktails = db_service.get_cocktails()  # 모든 칵테일 조회

        if not cocktails:
            return jsonify({'error': '데이터베이스에 칵테일 정보가 없습니다.'}), 404

        # GPT에 보낼 프롬프트 생성
        prompt = f"""
        사용자가 다음과 같이 설명한 칵테일을 기반으로 유사한 칵테일을 추천해 주세요.
        설명: {description}
        
        데이터베이스에 있는 칵테일 목록:
        {', '.join([cocktail['name'] for cocktail in cocktails])}
        
        각 추천에 대해 칵테일 이름, 재료, 제조 방법을 JSON 형식으로 반환해 주세요.
        예시:
        [
          {{
            "name": "칵테일 이름",
            "ingredients": "재료 목록",
            "method": "제조 방법"
          }},
          ...
        ]
        """

        # GPT API 호출하여 추천 생성
        gpt_response = cocktail_service.get_gpt_recommendation_from_prompt(prompt)

        if not gpt_response:
            return jsonify({'error': '추천 생성에 실패했습니다.'}), 500

        # GPT의 JSON 응답을 파싱
        try:
            recommendations = json.loads(gpt_response)
        except json.JSONDecodeError:
            return jsonify({'error': '추천 데이터를 파싱하는데 실패했습니다.'}), 500

        # 추천 결과 반환
        return jsonify({'recommendations': recommendations})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @app.route('/')
# def index():
#     """
#     메인 페이지 라우트
#     - 데이터베이스에서 칵테일 정보 조회
#     - GPT를 사용하여 각 칵테일에 대한 추천 생성
#     - 결과를 웹 페이지로 표시
#     """
#     try:
#         # 데이터베이스에서 칵테일 정보 조회
#         cocktails = cocktail_service.get_cocktails()

#         if cocktails is not None:
#             recommendations = []

#             # 각 칵테일에 대해 GPT 추천 생성
#             for cocktail in cocktails[:5]:  # 테스트를 위해 처음 5개만 처리
#                 recommendation = cocktail_service.get_gpt_recommendation(cocktail)
#                 recommendations.append({
#                     'original': cocktail,
#                     'recommendation': recommendation
#                 })

#             return render_template('index.html', recommendations=recommendations)
#         else:
#             return "데이터를 가져오는데 실패하였습니다."

#     except Exception as e:
#         return f"오류 발생: {str(e)}"

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