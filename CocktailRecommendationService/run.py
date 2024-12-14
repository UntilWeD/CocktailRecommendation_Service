import os
import requests
from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from app.service.service import CocktailService, UserService
from flask_cors import CORS
from dotenv import load_dotenv
from app.service.models.textExtraction.predict import Predict
from app.service.models.recommend.recommender import CocktailRecommender
from flask_login import LoginManager, login_user
from app.service.db import CocktailDBService

import json
import sys




# .env 파일 로드
load_dotenv()
api_key = os.getenv("GPT_API_KEY")  # .env 파일에서 GPT API 키 가져오기
if not api_key:
    raise ValueError("GPT_API_KEY is not set in the environment variables.")

app = Flask(__name__, static_folder="app/static",template_folder='app/templates')

# 서비스 객체 생성
db_service = CocktailDBService()
cocktail_service = CocktailService()
user_service = UserService()
# 모델 객체 생성
predict_service = Predict()
# Recommender 객체 생성

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vectorizer_path = os.path.join(current_dir, "CocktailRecommendationService", "app", "service", "models", "recommend", "model", "vectorizer.pkl")

print("File Exists:", os.path.exists(vectorizer_path))

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cocktail_recommender_service = CocktailRecommender(
    model_path=os.path.join(current_dir, "CocktailRecommendationService", "app", "service", "models", "recommend", "model", "multi_label_model.pt"),
    vectorizer_path=os.path.join(current_dir, "CocktailRecommendationService", "app", "service", "models", "recommend", "model", "vectorizer.pkl"),
    data_path=os.path.join(current_dir, "CocktailRecommendationService", "app", "service", "models", "recommend", "data", "final_cocktails.csv")
)
# 세션 암호화 키
app.secret_key = 'your_secret_key_here'


CORS(app)

# 후에 세션에서 사용자의 이메일 값을 알기위해서는
# user_email = session.get('email') 로 사용하면 됨

@app.route('/') 
def index():
    if 'email' in session:
        return render_template("index.html", email = session.get('email'), login = True)
    else:
        return render_template("index.html", login = False)

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
        설명: {predict_service.predict(description)['prompt']}
        
        데이터베이스에 있는 칵테일 목록 (최대 100개):
        {', '.join([cocktail['name'] for cocktail in cocktails[:100]])}
        
        각 추천에 대해 칵테일 이름, 재료(재료는 영어로), 제조 방법을 JSON 형식으로 반환해 주세요.
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

        print(f"GPT 프롬프트: {prompt}")  # 프롬프트 로그

        # GPT API 호출하여 추천 생성
        gpt_response = cocktail_service.get_gpt_recommendation_from_prompt(prompt)
        print(f"GPT 응답: {gpt_response}")  # GPT 응답 로그

        if not gpt_response:
            return jsonify({'error': '추천 생성에 실패했습니다.'}), 500

        # GPT의 JSON 응답을 파싱
        try:
            recommendations = json.loads(gpt_response)
            print(f"추천 결과: {recommendations}")  # 추천 결과 로그
        except json.JSONDecodeError:
            print("GPT 응답 형식 오류:", gpt_response)  # 서버 로그에 출력
            return jsonify({'error': '추천 데이터를 파싱하는데 실패했습니다.'}), 500

        # 재료 추출 및 중복 제거
        ingredients_list = set()
        for cocktail in recommendations:
            # 'ingredients' 키에서 재료 문자열 추출
            ingredients = cocktail.get('ingredients', '')

            # 문자열을 재료 리스트로 분리
            cocktail_ingredients = [ingredient.strip() for ingredient in ingredients.split(',') if ingredient.strip()]

            # 중복 제거를 위해 set에 추가
            ingredients_list.update(cocktail_ingredients)

        # set을 list로 변환하여 출력
        ingredients_list = list(ingredients_list)
        print(ingredients_list)

        try:
            # 디버깅을 위해 입력 재료 출력
            print("입력 재료:", ingredients_list)

            # recommend 메서드 호출 전 타입과 내용 확인
            recommender_result = cocktail_recommender_service.recommend(ingredients_list)

            # 결과 출력
            print(f"재료를 기반으로한 칵테일 추천: {recommender_result}")

        except AttributeError as e:
            print(f"AttributeError 발생: {e}")
            print("recommend 메서드가 존재하지 않거나 호출할 수 없습니다.")
        except TypeError as e:
            print(f"TypeError 발생: {e}")
            print("입력 타입이 맞지 않습니다. 입력 재료 리스트의 형식을 확인해주세요.")
        except Exception as e:
            print(f"예상치 못한 오류 발생: {e}")

        # 추천 결과 반환
        # 아직 재료에 따른 추천결과는 포함하지 않았습니다.
        return jsonify({'recommendations': recommendations})

    except Exception as e:
        print(f"추천 라우트 오류: {str(e)}")  # 서버 로그에 출력
        return jsonify({'error': str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)