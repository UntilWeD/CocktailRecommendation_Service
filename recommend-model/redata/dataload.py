import pandas as pd
import ast
from sklearn.preprocessing import OneHotEncoder

# 데이터 로드
file_path = "redata/final_cocktails.csv"
data = pd.read_csv(file_path)

# JSON 문자열 파싱
data['ingredients'] = data['ingredients'].apply(ast.literal_eval)
data['ingredientMeasures'] = data['ingredientMeasures'].apply(ast.literal_eval)

# One-Hot Encoding
encoder = OneHotEncoder()
encoded_categories = encoder.fit_transform(data[['category']]).toarray()

# 데이터프레임에 추가
categories_df = pd.DataFrame(encoded_categories, columns=encoder.get_feature_names_out(['category']))
data = pd.concat([data, categories_df], axis=1)

# 전처리된 데이터 저장
processed_file_path = "redata/processed/processed_cocktails.csv"
data.to_csv(processed_file_path, index=False)
print(f"Processed data saved to {processed_file_path}")
