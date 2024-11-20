from flask import Flask, render_template
from app.service.service import CocktailService

# Flask 애플리케이션 초기화
app = Flask(__name__, template_folder='app/templates')

# 칵테일 서비스 인스턴스 생성
cocktail_service = CocktailService()

@app.route('/')
def index():
    """
    메인 페이지 라우트
    - 데이터베이스에서 칵테일 정보 조회
    - GPT를 사용하여 각 칵테일에 대한 추천 생성
    - 결과를 웹 페이지로 표시
    """
    try:
        # 데이터베이스에서 칵테일 정보 조회
        cocktails = cocktail_service.get_cocktails()
        
        if cocktails is not None:
            recommendations = []
            
            # 각 칵테일에 대해 GPT 추천 생성
            for cocktail in cocktails[:5]:  # 테스트를 위해 처음 5개만 처리
                recommendation = cocktail_service.get_gpt_recommendation(cocktail)
                recommendations.append({
                    'original': cocktail,
                    'recommendation': recommendation
                })
            
            return render_template('index.html', recommendations=recommendations)
        else:
            return "데이터를 가져오는데 실패하였습니다."
            
    except Exception as e:
        return f"오류 발생: {str(e)}"

if __name__ == '__main__':
    # 디버그 모드로 Flask 애플리케이션 실행
    app.run(debug=True)