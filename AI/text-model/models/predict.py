import torch
from transformers import AutoTokenizer
from model_training import MultiLabelClassifier
import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 모델과 토크나이저 로드
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "bert_model")
model = MultiLabelClassifier(tokenizer_name="klue/bert-base")
checkpoint = torch.load(os.path.join(model_path, "best_model.pt"), map_location=torch.device('cpu'))
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()
tokenizer = AutoTokenizer.from_pretrained("klue/bert-base")

# 레이블 매핑
도수_매핑 = {0: '낮은', 1: '중간', 2: '높은', 3: '알 수 없음'}
술종류_매핑 = {0: '칵테일', 1: '럼', 2: '위스키', 3: '보드카', 4: '알 수 없음'}
맛_매핑 = {0: '달달한', 1: '쓴맛', 2: '상큼한', 3: '신맛', 4: '부드러운', 5: '알 수 없음'}

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        sentence = data['text']
        
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
        
        # 예측값 계산
        도수_pred = torch.argmax(outputs['도수'], dim=1).item()
        술종류_pred = torch.argmax(outputs['술종류'], dim=1).item()
        맛_pred = torch.argmax(outputs['맛'], dim=1).item()
        
        result = {
            '도수': 도수_매핑[도수_pred],
            '술종류': 술종류_매핑[술종류_pred],
            '맛': 맛_매핑[맛_pred]
        }
        
        # 프롬프트 생성
        prompt = f"나는 {result['도수']} 도수의 {result['맛']} {result['술종류']}을 마시고 싶어. 추천해줘"
        
        return jsonify({'result': result, 'prompt': prompt})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)