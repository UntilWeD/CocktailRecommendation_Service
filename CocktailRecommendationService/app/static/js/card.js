// DB와 연결하여 작성할 예정, GPT 출력으로 만들어진 칵테일 카드 , + detail로 이동하는 <a> 태그 삭제
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
    cardTitle.textContent = "";

    const cardSummary = document.createElement("div");
    cardSummary.className = "card__summary";
    cardSummary.textContent = "";

    list.appendChild(card);
    card.appendChild(cardImg);
    card.appendChild(cardTitle);
    card.appendChild(cardSummary);
  });
