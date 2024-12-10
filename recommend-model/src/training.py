import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# src 패키지에서 필요한 모듈 가져오기
from src.model import CocktailRecommendationModel
from torch.utils.data import DataLoader

def train_model(model, train_loader, num_epochs, criterion, optimizer):
    """
    모델 학습 루프
    Args:
        model: 학습할 모델
        train_loader: 학습 데이터 로더
        num_epochs: 학습 반복 횟수
        criterion: 손실 함수
        optimizer: 최적화 알고리즘
    """
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0

        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()  # 기존의 그라디언트를 초기화
            outputs = model(batch_X)  # 순전파
            loss = criterion(outputs, batch_y)  # 손실 계산
            loss.backward()  # 역전파
            optimizer.step()  # 가중치 업데이트

            running_loss += loss.item()

        print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {running_loss / len(train_loader):.4f}")
