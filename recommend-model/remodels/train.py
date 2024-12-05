import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from remodels.model import CocktailRecommendationModel

# 데이터 로드
file_path = "redata/processed/processed_cocktails.csv"
data = pd.read_csv(file_path)

# 데이터 준비
X = data.drop(columns=['id', 'name', 'category'])  # 입력 데이터
y = data['category']  # 출력 레이블

# 학습/테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 텐서 변환
X_train_tensor = torch.tensor(X_train.values, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test.values, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.long)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.long)

# 모델 초기화
input_size = X_train.shape[1]
hidden_size = 128
output_size = len(y.unique())
model = CocktailRecommendationModel(input_size, hidden_size, output_size)

# 손실 함수와 최적화기
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 학습 루프
num_epochs = 50
for epoch in range(num_epochs):
    # 순전파
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)

    # 역전파 및 가중치 업데이트
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item()}")

# 모델 저장
torch.save(model.state_dict(), "remodels/cocktail_model.pth")
print("Model saved to remodels/cocktail_model.pth")
