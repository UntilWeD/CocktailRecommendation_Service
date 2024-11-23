// 각 칵테일 카드 클릭 시 상세 모달 창을 화면에 띄우고 닫는 모듈, GPT 값 데이터베이스 저장 시 id값 부여해 카드 식별할 예정
const modal = document.querySelector(".modal");
const cardList = document.querySelector(".cocktail-list");
const closeBtn = document.querySelector(".modal__close-btn");

cardList.addEventListener("click", (e) => {
  // 카트 클릭시 모달 창 띄우기
  const card = e.target.closest(".cocktail-list__card"); // 선택자와 일치하는 가장 가까운 조상 요소(자기 자신 포함)를 반환
  if (card) {
    isModalOpen = true;
    console.log("Card is Clicked!");
    modal.style.display = "block";
  }
});

closeBtn.addEventListener("click", () => {
  // X 버튼 클릭 시 모달 창 닫기
  modal.style.display = "none";
});

modal.addEventListener("click", (e) => {
  // 모달 창 밖 클릭 시 창 닫기
  if (e.target === modal) {
    // 모달 레이아웃 자체를 클릭했을 때만 닫기
    console.log("Overlay is Clicked!");
    modal.style.display = "none";
  }
});
