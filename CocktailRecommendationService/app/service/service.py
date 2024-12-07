import openai
import pandas as pd
from sqlalchemy import create_engine
import json
import requests

import os
from dotenv import load_dotenv

from app.service.db import CocktailDBService

db_service = CocktailDBService()

class CocktailService:
    """
    칵테일 추천 서비스를 제공하는 클래스
    - 데이터베이스 연결 및 조회
    - GPT 기반 추천 기능 제공
    """
    def __init__(self):
        self.api_key = os.getenv("GPT_API_KEY")
        openai.api_key = self.api_key
        self.db_service = CocktailDBService()

        # 기존 GPT코드 API 키 에러 이슈로 추가
        self.api_url = "https://cesrv.hknu.ac.kr/srv/gpt"
        self.headers = {
            "Content-Type": "application/json"
        }
       
    # def get_gpt_recommendation(self, cocktail_info):
    #     """
    #     GPT를 사용하여 칵테일 추천을 생성하는 메서드
    #     Args:
    #         cocktail_info (dict): 원본 칵테일 정보
    #     Returns:
    #         str: GPT가 생성한 추천 텍스트
    #     """
    #     try:
    #         # GPT API를 호출하여 추천 생성
    #         response = openai.ChatCompletion.create(
    #             model="gpt-4",
    #             messages=[
    #                 {"role": "system", "content": "당신은 전문 칵테일 추천 전문가입니다."},
    #                 {"role": "user", "content": f"{cocktail_info['name']}와 비슷한 칵테일을 재료와 제조방법과 함께 추천해주세요."}
    #             ]
    #         )
    #         return response.choices[0].message['content']
    #     except Exception as e:
    #         print(f"GPT 추천 오류: {str(e)}")
    #         return None
    
    # 기존 GPT코드 API 키 에러 이슈로 코드 아래와 같이 수정
    def get_gpt_recommendation(self, cocktail_info):
        """
        자체 GPT API를 사용하여 칵테일 추천을 생성하는 메서드
        Args:
            cocktail_info (dict): 원본 칵테일 정보
        Returns:
            str: GPT가 생성한 추천 텍스트
        """
        question = f"{cocktail_info['name']}와 비슷한 칵테일을 재료와 제조방법과 함께 추천해주세요."
        payload = {
            "service": "gpt",
            "question": question,
            "hash": self.api_key
        }
        
        try:
            response = requests.post(self.api_url, data=json.dumps(payload), headers=self.headers)
            response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
            
            data = response.json()
            # 응답 형식에 따라 적절히 데이터 추출
            return data.get("answer", "추천을 생성할 수 없습니다.")
        except Exception as e:
            print(f"Unexpected error: {e}")  # 디버그용
            return None

    def get_gpt_recommendation_from_prompt(self, prompt):
        """
        자체 GPT API를 사용하여 주어진 프롬프트에 대한 추천을 생성하는 메서드
        Args:
            prompt (str): 사용자로부터 받은 프롬프트
        Returns:
            str: GPT가 생성한 추천 텍스트
        """
        payload = {
            "service": "gpt",
            "question": prompt,
            "hash": self.api_key
        }
        try:
            response = requests.post(self.api_url, data=json.dumps(payload), headers=self.headers)
            response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
            
            data = response.json()
            return data.get("answer", "추천을 생성할 수 없습니다.")
        except Exception as e:
            print(f"Unexpected error: {e}")  # 디버그용
            return None

class UserService:
    """
    사용자 관리 서비스를 제공하는 클래스
    - 데이터베이스 연결 및 조회
    - 사용자 인증 기능 제공
    """
    def __init__(self):
        self.db = CocktailDBService()


    def get_user(self, email, password):
        """
        사용자 정보를 조회하는 메서드
        Args:
            email (str): 사용자 이메일
            password (str): 사용자 비밀번호
        Returns:
            User: 사용자 정보를 담은 User 객체
        """
        return db_service.get_user(email, password)

    def register_user(self, email, password):
        """
        사용자 정보를 등록하는 메서드
        Args:
            email (str): 사용자 이메일
            password (str): 사용자 비밀번호
        Returns:
            bool: 사용자 등록 성공 여부
        """
        return db_service.register_user(email, password)



