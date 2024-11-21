import torch
import torch.nn as nn
from transformers import AutoModel

class MultiLabelClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = AutoModel.from_pretrained("bert-base-uncased")
        self.dropout = nn.Dropout(0.1)
        self.classifier_도수 = nn.Linear(768, 3)  # 낮은, 중간, 높은
        self.classifier_술종류 = nn.Linear(768, 4)  # 칵테일, 럼, 위스키, 보드카
        self.classifier_맛 = nn.Linear(768, 5)  # 달달한, 쓴, 상큼한, 신맛, 부드러운

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs[0][:, 0, :]  # CLS 토큰의 출력
        pooled_output = self.dropout(pooled_output)
        
        return {
            '도수': self.classifier_도수(pooled_output),
            '술종류': self.classifier_술종류(pooled_output),
            '맛': self.classifier_맛(pooled_output)
        }