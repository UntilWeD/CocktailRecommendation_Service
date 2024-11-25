import openai
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

class CocktailService:
    """
    칵테일 추천 서비스를 제공하는 클래스
    - 데이터베이스 연결 및 조회
    - GPT 기반 추천 기능 제공
    """
    def __init__(self):
        # PostgreSQL 데이터베이스 연결 설정
        self.engine = create_engine('postgresql://cocktail_v6qs_user:yGWXxLGbU6lkLEb2YD7MMlAHkEkN48l2@dpg-ct1cda3tq21c73enh4v0-a.oregon-postgres.render.com/cocktail_v6qs')
        # OpenAI API 키 설정
        load_dotenv()
        openai.api_key = os.getenv("GPT_API_KEY")

    def get_cocktails(self):
        """
        데이터베이스에서 모든 칵테일 정보를 조회하는 메서드
        Returns:
            list: 칵테일 정보가 담긴 딕셔너리 리스트
        """
        try:
            # 모든 칵테일 데이터 조회 쿼리
            query = "SELECT * FROM cocktail"
            df = pd.read_sql(query, self.engine)

            if not df.empty:
                return df.to_dict('records')  # DataFrame을 딕셔너리 리스트로 변환
            return None
        except Exception as e:
            print(f"데이터베이스 오류: {str(e)}")
            return None

    def get_gpt_recommendation(self, cocktail_info):
        """
        GPT를 사용하여 칵테일 추천을 생성하는 메서드
        Args:
            cocktail_info (dict): 원본 칵테일 정보
        Returns:
            str: GPT가 생성한 추천 텍스트
        """
        try:
            # GPT API를 호출하여 추천 생성
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 전문 칵테일 추천 전문가입니다."},
                    {"role": "user", "content": f"{cocktail_info['name']}와 비슷한 칵테일을 재료와 제조방법과 함께 추천해주세요."}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"GPT 추천 오류: {str(e)}")
            return None