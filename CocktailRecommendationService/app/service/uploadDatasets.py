from datasets import load_dataset
import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL 연결
engine = create_engine('postgresql://postgres:7539@localhost:5432/cocktail')

# 데이터셋 로드 (예시 - 실제 데이터셋 이름으로 변경 필요)
dataset = load_dataset("AdonisVainglory/Cocktailer")

# DataFrame으로 변환
df = pd.DataFrame(dataset['train'])  # 또는 적절한 split 사용

# CSV로 저장 (UTF-8 인코딩 사용)
df.to_csv('cocktails.csv', index=False, encoding='utf-8')

# PostgreSQL에 저장
df.to_sql('cocktail', engine, if_exists='replace', index=False)