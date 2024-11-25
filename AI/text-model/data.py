import os
import pandas as pd
import random

# 원본 데이터
data = {
    "입력 문장": [
        "나는 달달한 칵테일을 마시고 싶어.",
        "도수가 낮은 상큼한 칵테일을 추천해줘.",
        "강한 도수의 쓴맛 나는 보드카 추천해줘.",
        "부드럽고 달달한 위스키를 마셔보고 싶어.",
        "상큼하고 도수가 낮은 럼주를 소개해줘.",
        "도수가 중간이고 달달한 보드카가 있나요?",
        "신맛이 나고 도수가 강한 술을 찾고 있어요.",
        "도수가 약하고 부드러운 칵테일 추천 부탁해요.",
        "쓴맛 나는 위스키를 마셔보고 싶어.",
        "달달하고 상큼한 럼을 마시고 싶어요.",
        "가볍고 부드러운 칵테일이 필요해요.",
        "진하고 쓴 럼을 추천해줄래?",
        "부드럽고 달달한 술이 있었으면 좋겠어요.",
        "상큼한 맛이 나는 도수가 높은 보드카를 마셔보고 싶어요.",
        "쓴맛이 강한 위스키를 소개해주세요.",
        "도수가 낮고 달달한 술을 마시고 싶어요.",
        "도수가 높은 럼 중에서 신맛 나는 술을 찾고 있어요.",
        "가볍고 상큼한 칵테일 추천 부탁드립니다.",
        "쓴맛이 적고 부드러운 보드카를 원해요.",
        "달달한 맛이 나는 위스키를 찾고 있어요.",
        "신맛이 강하고 도수가 낮은 술 추천 부탁드려요.",
        "강한 도수의 부드러운 위스키를 추천해줘.",
        "쓴맛과 상큼함이 공존하는 칵테일이 있나요?",
        "달달하면서 도수가 높은 보드카를 찾고 있어요.",
        "가볍고 신맛 나는 럼을 추천해주세요."
    ],
    "도수": [
        "중간", "낮은", "높은", "높은", "낮은",
        "중간", "높은", "낮은", "높은", "중간",
        "낮은", "높은", "중간", "높은", "높은",
        "낮은", "높은", "낮은", "중간", "높은",
        "낮은", "높은", "중간", "높은", "낮은"
    ],
    "술 종류": [
        "칵테일", "칵테일", "보드카", "위스키", "럼",
        "보드카", "칵테일", "칵테일", "위스키", "럼",
        "칵테일", "럼", "칵테일", "보드카", "위스키",
        "칵테일", "럼", "칵테일", "보드카", "위스키",
        "칵테일", "위스키", "칵테일", "보드카", "럼"
    ],
    "맛": [
        "달달한", "상큼한", "쓴맛", "부드러운", "상큼한",
        "달달한", "신맛", "부드러운", "쓴맛", "달달한",
        "부드러운", "쓴맛", "달달한", "상큼한", "쓴맛",
        "달달한", "신맛", "상큼한", "부드러운", "달달한",
        "신맛", "부드러운", "쓴맛", "달달한", "신맛"
    ]
}

# 증강 데이터 생성 함수
def augment_data(data, num_samples=100):
    augmented_data = {"입력 문장": [], "도수": [], "술 종류": [], "맛": []}

    for _ in range(num_samples):
        도수 = random.choice(data["도수"])
        술_종류 = random.choice(data["술 종류"])
        맛 = random.choice(data["맛"])

        # 입력 문장 생성
        input_sentence = f"나는 {도수} 도수의 {맛} {술_종류}을(를) 마시고 싶어."
        augmented_data["입력 문장"].append(input_sentence)
        augmented_data["도수"].append(도수)
        augmented_data["술 종류"].append(술_종류)
        augmented_data["맛"].append(맛)

    return augmented_data

# 증강 데이터 생성
augmented_data = augment_data(data, num_samples=200)

# 기존 데이터와 병합
df_original = pd.DataFrame(data)
df_augmented = pd.DataFrame(augmented_data)
df_combined = pd.concat([df_original, df_augmented], ignore_index=True)

# 디렉토리 생성
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# CSV 파일 저장
output_path = os.path.join(output_dir, "raw_data.csv")
df_combined.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"증강된 데이터가 '{output_path}'에 저장되었습니다!")
