import random
import pandas as pd

# 데이터 구성 요소
templates = [
    "나는 {맛} {술종류}이(가) 좋아.",
    "도수가 {도수} {맛} {술종류} 추천해줘.",
    "{술종류} 중에서 {맛} 맛이 나는 걸 찾고 있어.",
    "친구랑 마실 {맛} {술종류} 추천 부탁해.",
    "가볍고 {맛} {술종류} 한 잔 하고 싶어요.",
    "{도수} {술종류} 중에서 {맛} 맛이 최고야."
]

# 문맥과 키워드 매핑 (문맥에 따라 기본값 설정)
context_rules = {
    "친구랑 마실": {"도수": "낮은", "맛": "달달한"},
    "혼자 즐기는": {"도수": "중간", "맛": "쓴맛"},
    "기분 내고 싶을 때": {"도수": "높은", "맛": "강렬한"},
    "상쾌한 기분을 원할 때": {"도수": "중간", "맛": "상쾌한"},
}

# 술 종류
alcohol_types = ["칵테일", "럼", "보드카"]

# 데이터 생성
data = []
for _ in range(1000):  # 1000개의 문장을 생성합니다.
    # 템플릿 선택
    template = random.choice(templates)
    context = random.choice(list(context_rules.keys()))
    
    # 문맥에 따른 기본값 설정
    rules = context_rules[context]
    taste = rules.get("맛", "없음")
    strength = rules.get("도수", "없음")
    
    # 랜덤으로 술 종류 선택 (50% 확률로 "없음" 포함)
    alcohol_type = random.choice(alcohol_types + ["없음"])
    
    # 템플릿에 값 채우기
    sentence = template.format(
        맛=taste if "맛" in template else "없음",
        도수=strength if "도수" in template else "없음",
        술종류=alcohol_type if "술종류" in template else "없음"
    )
    
    # 데이터 추가
    data.append({
        "입력 문장": f"{context} {sentence}",
        "도수": strength if strength != "없음" else "없음",
        "술 종류": alcohol_type,
        "맛": taste if taste != "없음" else "없음"
    })

# 데이터프레임 생성
df = pd.DataFrame(data)

# 데이터 저장
output_path = "data/context_based_data_with_defaults.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"규칙 기반 데이터셋이 '{output_path}'에 저장되었습니다!")
