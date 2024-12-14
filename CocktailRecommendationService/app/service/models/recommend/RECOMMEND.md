### **실행 방법**

1. **Python 패키지 설치**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Flask 서버 실행**:
   ```bash
   python src/recommender.py
   ```

3. **API 테스트**:
   - POST 요청을 통해 `/recommend` 엔드포인트를 호출.
   - JSON 형식으로 재료 리스트를 전달하여 추천 결과를 받습니다.

---

### **API 요청/응답 예제**

#### **요청**

- **URL**:
  ```
  http://localhost:5000/recommend
  ```

- **Headers**:
  ```json
  {
    "Content-Type": "application/json"
  }
  ```

- **Body**:
  ```json
  {
    "ingredients": ["gin", "lemonjuice", "grenadine"]
  }
  ```

#### **응답**

- **성공**:
  ```json
  {
    "recommendations": [
      ["Gin Daisy", 0.95],
      ["Tom Collins", 0.85],
      ["French 75", 0.80],
      ["Gin Fizz", 0.75],
      ["Aviation", 0.70]
    ]
  }
  ```

- **실패**:
  ```json
  {
    "error": "Invalid input format. Expected a list of ingredients."
  }
  ```

---

### **테스트 코드**

```python
import requests

# API URL
url = "http://localhost:5000/predict"

# 입력 데이터
data = {
    "ingredients": ["gin", "lemonjuice", "grenadine"]
}

# POST 요청
response = requests.post(url, json=data)

# 응답 처리
if response.status_code == 200:
    recommendations = response.json().get("recommendations", [])
    print("Top 5 Recommended Cocktails:")
    for name, score in recommendations:
        print(f"{name}: {score:.2f}")
else:
    print("Error:", response.json().get("error"))
```

---

### **결론**

이 코드는 학습된 `multi_label_model`을 기반으로 Flask를 사용하여 간단한 API를 제공합니다. 필요한 경우 API를 확장하거나 다른 기능을 추가할 수 있습니다. 추가로 궁금한 사항이 있다면 말씀해 주세요! 😊