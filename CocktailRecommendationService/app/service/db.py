import openai
import pandas as pd
from sqlalchemy import create_engine, text

class CocktailDBService:

    def __init__(self):
        # PostgreSQL 데이터베이스 연결 설정
        self.engine = create_engine('postgresql://cocktail_v6qs_user:yGWXxLGbU6lkLEb2YD7MMlAHkEkN48l2@dpg-ct1cda3tq21c73enh4v0-a.oregon-postgres.render.com/cocktail_v6qs')


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

    # 로그인 할 때의 유저 조회
    def get_user(self, email, password):
        try:
            print(f"로그인 시도 - 이메일: {email}")
            query = "SELECT * FROM users WHERE email = %s AND password = %s"
            df = pd.read_sql(query, self.engine, params=(email, password))

            print(f"쿼리 결과: {len(df)} 레코드")

            if not df.empty:
                return df.to_dict('records')[0]
            return None
        except Exception as e:
            print(f"데이터베이스 오류: {str(e)}")
            return None

    #회원가입 메서드
    def register_user(self, email, password):
        try:
            with self.engine.connect() as connection:
                # 트랜잭션 시작
                transaction = connection.begin()

                query = text("INSERT INTO users (email, password) VALUES (:email, :password)")
                connection.execute(query, {'email': email, 'password': password})

                # 트랜잭션 커밋
                transaction.commit()

                #with self.engine.connect() as connection:
                    #query = text("INSERT INTO users (email, password) VALUES (:email, :password)")
                    #connection.execute(query, {'email': email, 'password': password})


            return True
        except Exception as e:
            print(f"데이터베이스 오류: {str(e)}")
            return False



