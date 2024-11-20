import pandas as pd
from sqlalchemy import create_engine

class CocktailService:
    def __init__(self):
        self.engine = create_engine('postgresql://postgres:7539@localhost:5432/Cocktail')

    def get_cocktails(self):
        try:
            query = "SELECT * FROM cocktail"
            df = pd.read_sql(query, self.engine)

            # df의 첫 번째 행을 딕셔너리로 변환
            if not df.empty:
                return df.to_dict('records')
            None

        except Exception as e:
            print(f"Database error: {str(e)}")
            return None


