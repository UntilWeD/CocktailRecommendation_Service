// DB와 연결하여 작성할 예정, GPT 출력으로 만들어진 칵테일 카드 , + detail로 이동하는 <a> 태그 삭제
// GPT 값 데이터베이스 저장 시 id값 부여해 카드 식별할 예정
const list = document.querySelector(".cocktail-list");

document
  .querySelector(".cocktail-in-output")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    const card = document.createElement("div");
    card.className = "cocktail-list__card";
    card.textContent = ""; // 변수 들어갈 예정

    const cardImg = document.createElement("img");
    cardImg.className = "card__image";
    cardImg.src = "";
    cardImg.alt = "칵테일 대표 이미지";

    const cardTitle = document.createElement("div");
    cardTitle.className = "card__title";
    cardTitle.textContent = "칵테일 이름";

    const cardSummary = document.createElement("div");
    cardSummary.className = "card__summary";
    cardSummary.textContent = "칵테일 간략한 설명";

    list.appendChild(card);
    card.appendChild(cardImg);
    card.appendChild(cardTitle);
    card.appendChild(cardSummary);
  });
