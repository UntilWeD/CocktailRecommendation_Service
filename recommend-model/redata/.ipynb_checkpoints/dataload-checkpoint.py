import pandas as pd
import ast
from sklearn.preprocessing import OneHotEncoder

# 데이터 로드
data = pd.read_csv("final_cocktails.csv")

# JSON 문자열을 파싱
data['ingredients'] = data['ingredients'].apply(ast.literal_eval)
data['ingredientMeasures'] = data['ingredientMeasures'].apply(ast.literal_eval)

# One-Hot Encoding
encoder = OneHotEncoder()
encoded_categories = encoder.fit_transform(data[['category']]).toarray()

# 데이터프레임에 추가
categories_df = pd.DataFrame(encoded_categories, columns=encoder.get_feature_names_out(['category']))
data = pd.concat([data, categories_df], axis=1)
