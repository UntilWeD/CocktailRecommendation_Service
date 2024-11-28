import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer

class MultiLabelClassifier(nn.Module):
    def __init__(self, tokenizer_name=None):
        super().__init__()
        if tokenizer_name is None:
            tokenizer_name = "klue/bert-base"
            
        self.bert = AutoModel.from_pretrained(tokenizer_name)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        
        # 중간 레이어
        self.intermediate = nn.Sequential(
            nn.Linear(768, 512),
            nn.ReLU(),
            nn.BatchNorm1d(512),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.Dropout(0.3)
        )
        
        # 분류기 레이어들 수정
        self.classifier_도수 = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 4)  # 4개 클래스
        )
        
        self.classifier_술종류 = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 5)  # 5개 클래스
        )
        
        self.classifier_맛 = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 6)  # 6개 클래스
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs[0][:, 0, :]  # CLS 토큰의 출력
        intermediate_output = self.intermediate(pooled_output)
        
        return {
            '도수': self.classifier_도수(intermediate_output),
            '술종류': self.classifier_술종류(intermediate_output),
            '맛': self.classifier_맛(intermediate_output)
        }
