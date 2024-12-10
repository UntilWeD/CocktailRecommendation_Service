# 필요한 라이브러리 임포트
import os
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE
from torch.utils.data import DataLoader, TensorDataset
from sklearn.metrics import classification_report, confusion_matrix

# 칵테일 추천 모델 정의
class CocktailRecommendationModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(CocktailRecommendationModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.batch_norm1 = nn.BatchNorm1d(hidden_size)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.batch_norm2 = nn.BatchNorm1d(hidden_size // 2)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.3)
        self.fc3 = nn.Linear(hidden_size // 2, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.batch_norm1(x)
        x = self.relu1(x)
        x = self.dropout1(x)
        x = self.fc2(x)
        x = self.batch_norm2(x)
        x = self.relu2(x)
        x = self.dropout2(x)
        x = self.fc3(x)
        return x

# GPU 사용 여부 확인 및 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# 데이터 로드 및 전처리
file_path = "final_cocktails.csv"
data = pd.read_csv(file_path)

# 'ingredients' 데이터를 리스트로 변환하고 텍스트로 병합
import ast
data['ingredients'] = data['ingredients'].apply(ast.literal_eval)
data['ingredients_text'] = data['ingredients'].apply(lambda x: ' '.join(x))

# TF-IDF 벡터화
vectorizer = TfidfVectorizer(max_features=100)
X = vectorizer.fit_transform(data['ingredients_text']).toarray()

# 'category' 레이블 인코딩
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(data['category'])

# 클래스 불균형 해결 (SMOTE)
smote = SMOTE(random_state=42, k_neighbors=2)
X_resampled, y_resampled = smote.fit_resample(X, y)

# 데이터 정규화
scaler = StandardScaler()
X_resampled = scaler.fit_transform(X_resampled)

# 학습/테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# 텐서 변환 및 DataLoader 생성
X_train_tensor = torch.tensor(X_train, dtype=torch.float32).to(device)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32).to(device)
y_train_tensor = torch.tensor(y_train, dtype=torch.long).to(device)
y_test_tensor = torch.tensor(y_test, dtype=torch.long).to(device)

train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)

# 모델 초기화
input_size = X_train.shape[1]
hidden_size = 128
output_size = len(np.unique(y))

model = CocktailRecommendationModel(input_size, hidden_size, output_size).to(device)

# 손실 함수와 최적화기
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0005)

# 학습 루프
num_epochs = 100
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for batch_X, batch_y in train_loader:
        # 순전파
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)

        # 역전파 및 가중치 업데이트
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss / len(train_loader):.4f}")

# 평가 루프
model.eval()
with torch.no_grad():
    outputs = model(X_test_tensor)
    predictions = torch.argmax(outputs, dim=1)
    accuracy = (predictions == y_test_tensor).sum().item() / y_test_tensor.size(0)
    print(f"Test Accuracy: {accuracy * 100:.2f}%")

# 혼동 행렬 및 분류 리포트 출력
print("Confusion Matrix:")
print(confusion_matrix(y_test_tensor.cpu(), predictions.cpu()))
print("\nClassification Report:")
print(classification_report(y_test_tensor.cpu(), predictions.cpu(), target_names=label_encoder.classes_))

# 모델 저장
save_dir = "models"
os.makedirs(save_dir, exist_ok=True)
save_path = os.path.join(save_dir, "cocktail_model.pth")
torch.save(model.state_dict(), save_path)
print(f"Model saved to {save_path}")
