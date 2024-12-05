import pandas as pd
import torch
from remodels.model import CocktailRecommendationModel

# 데이터 로드
file_path = "redata/processed/processed_cocktails.csv"
data = pd.read_csv(file_path)

# 데이터 준비
X = data.drop(columns=['id', 'name', 'category'])  # 입력 데이터
y = data['category']  # 출력 레이블

# 텐서 변환
X_tensor = torch.tensor(X.values, dtype=torch.float32)
y_tensor = torch.tensor(y.values, dtype=torch.long)

# 모델 로드
input_size = X.shape[1]
hidden_size = 128
output_size = len(y.unique())
model = CocktailRecommendationModel(input_size, hidden_size, output_size)
model.load_state_dict(torch.load("remodels/cocktail_model.pth"))
model.eval()

# 평가
outputs = model(X_tensor)
_, predicted = torch.max(outputs, 1)
accuracy = (predicted == y_tensor).sum().item() / y_tensor.size(0)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
