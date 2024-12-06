import openai
import pandas as pd
from sqlalchemy import create_engine
import json

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
        # OpenAI API 키 설정
        load_dotenv()
        openai.api_key = os.getenv("GPT_API_KEY")
        self.db_service = CocktailDBService()
        # OpenAI API 키 확인
        if not openai.api_key:
            raise ValueError("OpenAI API key is not set. Please set GPT_API_KEY in your environment variables.")
        print(f"Loaded OpenAI API Key: {openai.api_key}")  # 디버그용, 배포 시 제거 필요

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
            return response.choices[0].message['content']
        except Exception as e:
            print(f"GPT 추천 오류: {str(e)}")
            return None
    
    def get_gpt_recommendation_from_prompt(self, prompt):
        """
        GPT에 프롬프트를 직접 전달하여 추천을 받는 메서드
        Args:
            prompt (str): GPT에 전달할 프롬프트
        Returns:
            str: GPT가 생성한 추천 텍스트
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 전문 칵테일 추천 전문가입니다."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message['content']
        except Exception as e:
            print(f"GPT 추천 오류: {str(e)}")
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



