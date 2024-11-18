// 상단 메뉴 바 조작

const mainTitle = document.querySelector(".nav__main-title");
const menuIcon = document.querySelector(".nav__menu-icon");

const moveToTop = () => {
  window.scrollTo({
    top: 0, // 화면의 최상단으로 위치
    behavior: "smooth", // 스크롤 애니메이션 (smooth: 부드럽게 이동, auto: 즉시 이동)
  });
};

mainTitle.addEventListener("click", moveToTop);
