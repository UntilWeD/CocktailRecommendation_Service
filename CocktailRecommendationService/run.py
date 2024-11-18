from flask import Flask, render_template
from app.service.service import CocktailService


app = Flask(__name__, template_folder='app/templates')

cocktail_service = CocktailService()


@app.route('/')
def index():
    try:
        data = cocktail_service.get_cocktails()

        if data is not None:
            return render_template('index.html', data=data)
        else:
            return "데이터를 가져오는데 실패하였습니다."

    except Exception as e:
        return f"에러 발생: {str(e)}"



if __name__ == '__main__':
    app.run(debug=True)