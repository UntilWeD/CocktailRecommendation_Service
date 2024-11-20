import chardet
import pandas as pd

# 파일의 실제 인코딩 확인
with open('cocktails.csv', 'rb') as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    print(f"Detected encoding: {result['encoding']}")

# 감지된 인코딩으로 읽기
df = pd.read_csv('cocktails.csv', encoding=result['encoding'])