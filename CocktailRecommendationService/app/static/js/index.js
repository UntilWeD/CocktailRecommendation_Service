document.addEventListener("DOMContentLoaded", () => {
  const recommendForm = document.getElementById("recommend-form");
  const cocktailOutput = document.getElementById("cocktail-output");

  recommendForm.addEventListener("submit", async (e) => {
    e.preventDefault(); // 기본 폼 제출 방지

    const userDescription = recommendForm.user_description.value;

    // 추천 결과 초기화
    cocktailOutput.innerHTML = "<h1>칵테일 추천</h1><p>추천 중...</p>";

    try {
      const response = await axios.post("/recommend", {
        description: userDescription,
      });

      if (
        response.data.recommendations &&
        response.data.recommendations.length > 0
      ) {
        let outputHTML = "<h1>칵테일 추천</h1>";
        response.data.recommendations.forEach((item) => {
          outputHTML += `
              <div class="cocktail-card">
                <h2>원본 칵테일: ${item.original.name}</h2>
                <p><strong>재료:</strong> ${item.original.ingredients}</p>
                <div class="recommendation">
                  <h3>GPT 추천:</h3>
                  <p>${item.recommendation}</p>
                </div>
              </div>
            `;
        });
        cocktailOutput.innerHTML = outputHTML;
      } else {
        cocktailOutput.innerHTML =
          "<h1>칵테일 추천</h1><p>추천 결과가 없습니다. 원하는 칵테일을 입력해주세요.</p>";
      }
    } catch (error) {
      console.error(error);
      cocktailOutput.innerHTML =
        "<h1>칵테일 추천</h1><p>추천을 불러오는데 실패했습니다. 다시 시도해주세요.</p>";
    }
  });
});
