rom datasets import load_dataset
import pandas as pd
from sqlalchemy import create_engine

def upload_to_database():
    """
    Hugging Face 데이터셋을 다운로드하고 PostgreSQL에 업로드하는 함수
    - 데이터셋을 CSV로 저장
    - PostgreSQL 데이터베이스에 데이터 적재
    """
    # PostgreSQL 데이터베이스 연결 설정
    engine = create_engine('postgresql://postgres:7539@localhost:5432/cocktail')

    # Hugging Face에서 칵테일 데이터셋 로드
    dataset = load_dataset("AdonisVainglory/Cocktailer")

    # 데이터셋을 DataFrame으로 변환
    df = pd.DataFrame(dataset['train'])

    # 데이터를 CSV 파일로 저장 (UTF-8 인코딩 사용)
    df.to_csv('cocktails.csv', index=False, encoding='utf-8')

    # DataFrame을 PostgreSQL 데이터베이스에 저장
    # if_exists='replace': 기존 테이블이 있으면 덮어쓰기
    df.to_sql('cocktail', engine, if_exists='replace', index=False)

if __name__ == "__main__":
    upload_to_database()