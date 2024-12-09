const menu = document.querySelector(".nav__menu");
const menuSidebar = document.querySelector(".nav__menu-sidebar");
let isMenuOpend = false;

menu.addEventListener("mouseover", () => {
  menuSidebar.style.display = "block";
});

menuSidebar.addEventListener("mouseout", () => {
  menuSidebar.style.display = "none";
});
