

```markdown:OSS_Project/AI/text-model/models/README.md
# 술 추천 시스템 BERT 모델

이 모델은 사용자의 입력 문장을 분석하여 도수, 술종류, 맛을 예측하는 BERT 기반 멀티라벨 분류기입니다.

## 설치 요구사항

```bash
pip install -r requirements.txt
```

## 모델 구조
- 기반 모델: klue/bert-base
- 출력: 도수(4클래스), 술종류(5클래스), 맛(6클래스) 분류

## 사용 방법

1. 모델 초기화 및 로드:
```python
import torch
from transformers import AutoTokenizer
from model_training import MultiLabelClassifier

# 모델 초기화
model = MultiLabelClassifier(tokenizer_name="klue/bert-base")
checkpoint = torch.load("bert_model/best_model.pt", map_location=torch.device('cpu'))
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained("klue/bert-base")
```

2. 예측 실행:
```python
def predict(sentence):
    # 입력 문장 전처리
    inputs = tokenizer(
        sentence,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt"
    )
    
    # 예측
    with torch.no_grad():
        outputs = model(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask']
        )
    
    # 결과 반환
    도수_pred = torch.argmax(outputs['도수'], dim=1).item()
    술종류_pred = torch.argmax(outputs['술종류'], dim=1).item()
    맛_pred = torch.argmax(outputs['맛'], dim=1).item()
    
    return {
        '도수': 도수_매핑[도수_pred],
        '술종류': 술종류_매핑[술종류_pred],
        '맛': 맛_매핑[맛_pred]
    }
```

## 예시 코드

```python
# 예시 문장으로 테스트
sentence = "도수가 낮고 상큼한 칵테일 추천해줘"
result = predict(sentence)
print(result)
# 출력: {'도수': '낮은', '술종류': '칵테일', '맛': '상큼한'}
```

## 레이블 매핑
```python
도수_매핑 = {0: '낮은', 1: '중간', 2: '높은', 3: '알 수 없음'}
술종류_매핑 = {0: '칵테일', 1: '럼', 2: '위스키', 3: '보드카', 4: '알 수 없음'}
맛_매핑 = {0: '달달한', 1: '쓴맛', 2: '상큼한', 3: '신맛', 4: '부드러운', 5: '알 수 없음'}
```

## 웹 서버 실행 방법

1. Flask 서버 실행:
```bash
python predict.py
```

2. 웹 브라우저에서 접속:
```
http://localhost:5000
```

## 참고 사항
- CPU에서도 실행 가능하도록 설계되었습니다
- 입력 문장은 최대 512 토큰으로 제한됩니다
- 모델 가중치 파일(best_model.pt)이 필요합니다
```